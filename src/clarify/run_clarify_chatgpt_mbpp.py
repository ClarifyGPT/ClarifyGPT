import json
import copy
from utils import *
from src.parallel_request import parallel_request_openai
from src.prompt.prompt_mbpp import *
import functools
from threading import Thread
from tqdm import tqdm


# 1. run sample codes on tests, get task_id of the unclear prompts
def runTests_getTaskID(sample_code_file, tests_file, save_path=None):
    with open(tests_file, 'r') as f:
        tests_lines = f.readlines()

    with open(sample_code_file, 'r') as f:
        sample_code_lines = f.readlines()

    # sort
    sample_code_lines = sort_parallel_datalines(sample_code_lines)

    if save_path is None:
        save_path = sample_code_file.replace(".jsonl", "_needcq.jsonl")

    with open(save_path, 'w') as w:
        for tests_line, sample_code_line in tqdm(zip(tests_lines, sample_code_lines)):
            tests_line = json.loads(tests_line)
            sample_code_line = json.loads(sample_code_line)

            prompt = tests_line['prompt']
            entry_point = tests_line['entry_point']
            tests = tests_line['tests']
            time_limit_func = 'import signal\nfrom contextlib import contextmanager\nclass TimeoutException(Exception): pass\n\n@contextmanager\ndef time_limit(seconds: float):\n    def signal_handler(signum, frame):\n        raise TimeoutException("Timed out!")\n    signal.setitimer(signal.ITIMER_REAL, seconds)\n    signal.signal(signal.SIGALRM, signal_handler)\n    try:\n        yield\n    finally:\n        signal.setitimer(signal.ITIMER_REAL, 0)\n'

            all_test_results = {}
            for i in range(15):
                generated_raw_code = sample_code_line[2]['choices'][i]["message"]['content']
                complete_code = parse_code_w_prompt_mbpp('gpt-3.5', generated_raw_code, prompt, entry_point)
                test_result = []
                for test in tests:
                    test_list = test.split('\n')
                    test_list[-1] = 'xx = ' + test_list[-1]
                    test = '\n'.join(test_list)

                    code_to_be_test = time_limit_func + '\n' + complete_code + '\n\ntry:\n    with time_limit(0.2):\n        ' + test + '\nexcept Exception:\n    xx = "error!!!"'
                    # print(code_to_be_test)
                    loc = {}
                    try:
                        exec(code_to_be_test, loc)
                        return_value = loc['xx']
                    except Exception:
                        return_value = 'error!!!'
                    test_result.append(return_value)
                    # print(return_value)
                    # print(code_to_be_test)
                    # assert 1 == 2

                if str(test_result) in all_test_results.keys():
                    all_test_results[str(test_result)].append(clean_format(generated_raw_code))
                else:
                    all_test_results[str(test_result)] = [clean_format(generated_raw_code)]

            if len(all_test_results) > 1:
                print(len(all_test_results))
                need_cq_dict = {'task_id': tests_line['task_id'], 'prompt': prompt, 'candidate_codes': []}
                for v_idx, v in enumerate(all_test_results.values()):
                    need_cq_dict['candidate_codes'].append(v[0])
                    if v_idx >= 4:
                        break
                print(len(need_cq_dict['candidate_codes']))
                print('=================================')
                json.dump(need_cq_dict, w)
                w.write('\n')
            elif 'error!!!' in list(all_test_results.keys())[0]:
                print(list(all_test_results.keys())[0])
                need_cq_dict = {'task_id': tests_line['task_id'], 'prompt': prompt, 'candidate_codes': [],
                                'exec_results': list(all_test_results.keys())}
                for v_idx, v in enumerate(all_test_results.values()):
                    need_cq_dict['candidate_codes'].append(v[0])
                    need_cq_dict['candidate_codes'].append(v[1])
                print(len(need_cq_dict['candidate_codes']))
                print('=================================')
                json.dump(need_cq_dict, w)
                w.write('\n')
            # else:
            #     print(task_id, all_test_results.keys())

    return save_path


# 2. submit askcq task & run parallel request
def askcq_runRequest(inference_type, needcq_file, askcq_path=None, askcq_results_path=None):
    with open(needcq_file, 'r') as f:
        data_lines = f.readlines()

    if askcq_path is None:
        askcq_path = needcq_file.replace(".jsonl", "_askcq.jsonl")

    with open(askcq_path, 'w') as w:
        for data_line in data_lines:
            data_line = json.loads(data_line)
            ori_prompt = data_line['prompt']
            candidate_codes = data_line['candidate_codes']

            code_string = ''
            for idx, candidate_c in enumerate(candidate_codes):
                code_string += f'Solution {idx}:\n{candidate_c}\n'
            openai_messages = copy.deepcopy(askcq_prompt[inference_type])

            if inference_type == 'zero_shot':
                openai_messages.append({
                    'role': 'user',
                    'content': f'User Requirement:\n{ori_prompt.strip()}\n{code_string.strip()}'
                               f'\nAnalysis:\n{{insert analysis results here}}'
                               f'\nClarifying Questions:\n{{insert clarifying questions here}}'
                })
            else:
                openai_messages.append({
                    'role': 'user',
                    'content': f'User Requirement:\n{ori_prompt.strip()}\n{code_string.strip()}'
                })
            json_dict = dict(model='gpt-3.5-turbo',
                             messages=openai_messages,
                             temperature=0.0,
                             max_tokens=800,
                             top_p=0.95,
                             frequency_penalty=0,
                             presence_penalty=0,
                             n=1,
                             )
            # print(json_dict['messages'][0]['content'])
            # print(json_dict['messages'][-1]['content'])
            # print('=========================================')
            # assert 1==2
            json_string = json.dumps(json_dict)
            w.write(json_string + "\n")

    if askcq_results_path is None:
        parallel_request_openai(requests_filepath=askcq_path)
        askcq_results_path = askcq_path.replace(".jsonl", "_results.jsonl")
    else:
        parallel_request_openai(requests_filepath=askcq_path, save_filepath=askcq_results_path)

    return askcq_path, askcq_results_path


# 3. submit answercq task & run parallel request
def answercq_runRequest(inference_type, needcq_file, askcq_results_path, answercq_path=None,
                        answercq_results_path=None):
    with open(needcq_file, 'r') as f:
        ori_data_lines = f.readlines()

    with open(askcq_results_path, 'r') as f:
        data_lines = f.readlines()

    # sort
    data_lines = sort_parallel_datalines(data_lines)
    assert len(data_lines) == len(ori_data_lines)

    if answercq_path is None:
        answercq_path = askcq_results_path.replace(".jsonl", "_answercq.jsonl")

    with open(answercq_path, 'w') as w:
        for ori_data_line, data_line in zip(ori_data_lines, data_lines):
            ori_data_line = json.loads(ori_data_line)
            data_line = json.loads(data_line)
            cq = parse_cq_mbpp(data_line[2]['choices'][0]["message"]['content'])
            ori_prompt = ori_data_line['prompt']

            openai_messages = copy.deepcopy(answercq_prompt[inference_type])
            openai_messages.append({
                'role': 'user',
                'content': f'User Requirement:\n{ori_prompt.strip()}'
                           f'\n\n### Clarifying Questions:\n{cq.strip()}'
                           f'\n\n### Answers:\n{{insert answers here}}'
            })

            json_dict = dict(model='gpt-3.5-turbo',
                             messages=openai_messages,
                             temperature=0.0,
                             max_tokens=300,
                             top_p=0.95,
                             frequency_penalty=0,
                             presence_penalty=0,
                             n=1,
                             )
            # print(json_dict['messages'][0]['content'])
            # print(json_dict['messages'][-1]['content'])
            # print('=========================================')
            json_string = json.dumps(json_dict)
            w.write(json_string + "\n")

    if answercq_results_path is None:
        parallel_request_openai(requests_filepath=answercq_path)
        answercq_results_path = answercq_path.replace(".jsonl", "_results.jsonl")
    else:
        parallel_request_openai(requests_filepath=answercq_path, save_filepath=answercq_results_path)

    return answercq_path, answercq_results_path


def answercq_w_test_runRequest(test_file, inference_type, needcq_file, askcq_results_path, answercq_path=None,
                               answercq_results_path=None):
    with open(needcq_file, 'r') as f:
        ori_data_lines = f.readlines()

    with open(askcq_results_path, 'r') as f:
        data_lines = f.readlines()

    with open(test_file, 'r') as f:
        test_lines = f.readlines()

    # sort
    data_lines = sort_parallel_datalines(data_lines)
    assert len(data_lines) == len(ori_data_lines) == len(test_lines)

    if answercq_path is None:
        answercq_path = askcq_results_path.replace(".jsonl", "_answercq.jsonl")

    with open(answercq_path, 'w') as w:
        for ori_data_line, data_line, test_line in zip(ori_data_lines, data_lines, test_lines):
            ori_data_line = json.loads(ori_data_line)
            data_line = json.loads(data_line)
            test_line = json.loads(test_line)
            assert test_line['task_id'] == ori_data_line['task_id']
            cq = parse_cq_mbpp(data_line[2]['choices'][0]["message"]['content'])
            python_func = test_line['solution']
            test_cases = '\n'.join(test_line['test_list'])

            openai_messages = copy.deepcopy(answercq_prompt[inference_type])
            openai_messages.append({
                'role': 'user',
                'content': f'Python Function:\n{python_func.strip()}'
                           f'\nTest Cases:\n{test_cases.strip()}'
                           f'\n\n### Clarifying Questions:\n{cq.strip()}'
                           f'\n\n### Answers:\n{{insert answers here}}'
            })

            json_dict = dict(model='gpt-3.5-turbo',
                             messages=openai_messages,
                             temperature=0.0,
                             max_tokens=300,
                             top_p=0.95,
                             frequency_penalty=0,
                             presence_penalty=0,
                             n=1,
                             )
            # print(json_dict['messages'][0]['content'])
            # print(json_dict['messages'][-3]['content'])
            # print(json_dict['messages'][-2]['content'])
            # print(json_dict['messages'][-1]['content'])
            # print('=========================================')
            json_string = json.dumps(json_dict)
            w.write(json_string + "\n")

    if answercq_results_path is None:
        parallel_request_openai(requests_filepath=answercq_path)
        answercq_results_path = answercq_path.replace(".jsonl", "_results.jsonl")
    else:
        parallel_request_openai(requests_filepath=answercq_path, save_filepath=answercq_results_path)

    return answercq_path, answercq_results_path


# 4. synthesize the prompt with cqs and answers
def synthesize_runRequest(inference_type, needcq_file, askcq_results_path, answercq_results_path,
                          synthesize_path=None, synthesize_results_path=None):
    with open(needcq_file, 'r') as f:
        ori_data_lines = f.readlines()

    with open(askcq_results_path, 'r') as f:
        ask_data_lines = f.readlines()
    ask_data_lines = sort_parallel_datalines(ask_data_lines)

    with open(answercq_results_path, 'r') as f:
        answer_data_lines = f.readlines()
    answer_data_lines = sort_parallel_datalines(answer_data_lines)

    if synthesize_path is None:
        synthesize_path = answercq_results_path.replace(".jsonl", "_synthesize.jsonl")

    with open(synthesize_path, 'w') as w:
        for ori_data_line, ask_data_line, answer_data_line in zip(ori_data_lines, ask_data_lines, answer_data_lines):
            ori_data_line = json.loads(ori_data_line)
            ask_data_line = json.loads(ask_data_line)
            answer_data_line = json.loads(answer_data_line)

            ori_prompt = ori_data_line['prompt']
            ask_cq = ask_data_line[2]['choices'][0]["message"]['content']
            answer_cq = answer_data_line[2]['choices'][0]["message"]['content']
            clarification = parse_clarification_mbpp(ask_cq, answer_cq)
            refined_prompt = refine_prompt_clarify(ori_prompt, clarification)

            openai_messages = copy.deepcopy(synthesize_prompt[inference_type])
            openai_messages.append({
                'role': 'user',
                'content': f'User Requirement:\n{refined_prompt}'
                           # f'\n{clarification}'
            })

            json_dict = dict(model='gpt-3.5-turbo',
                             messages=openai_messages,
                             temperature=0.0,
                             max_tokens=300,
                             top_p=0.95,
                             frequency_penalty=0,
                             presence_penalty=0,
                             n=1,
                             )
            # print(json_dict['messages'][0]['content'])
            # print(json_dict['messages'][1]['content'])
            # print(json_dict['messages'][2]['content'])
            # print(json_dict['messages'][-1]['content'])
            # print('=========================================')
            # assert 1==2
            json_string = json.dumps(json_dict)
            w.write(json_string + "\n")

    if synthesize_results_path is None:
        parallel_request_openai(requests_filepath=synthesize_path)
        synthesize_results_path = synthesize_path.replace(".jsonl", "_results.jsonl")
    else:
        parallel_request_openai(requests_filepath=synthesize_path, save_filepath=synthesize_results_path)
    # assert 1==2
    return synthesize_path, synthesize_results_path


# 5. generate the final humaneval file
def generate_file(humaneval_file, greedy_generate_file, needcq_path, synthesize_results_list, final_path=None):
    with open(humaneval_file, 'r') as f:
        ori_data_lines = f.readlines()
    with open(greedy_generate_file, 'r') as f:
        greedy_data_lines = f.readlines()
    with open(needcq_path, 'r') as f:
        needcq_data_lines = f.readlines()

    n = len(synthesize_results_list)
    modified_code_dict = {'task_id_list': [], 'code_list': []}
    for i in range(n):
        with open(synthesize_results_list[i], 'r') as f:
            synthesize_data_lines = f.readlines()

        synthesize_data_lines = sort_parallel_datalines(synthesize_data_lines)

        modified_code_dict['task_id_list'] = []
        modified_code_dict['code_list'].append([])
        for needcq_data_line, synthesize_data_line in zip(needcq_data_lines, synthesize_data_lines):
            needcq_data_line = json.loads(needcq_data_line)
            synthesize_data_line = json.loads(synthesize_data_line)
            task_id = needcq_data_line['task_id']
            generated_raw_code = synthesize_data_line[2]['choices'][0]["message"]['content']

            modified_code_dict['task_id_list'].append(task_id)
            modified_code_dict['code_list'][i].append(generated_raw_code)
        assert len(modified_code_dict['task_id_list']) == len(modified_code_dict['code_list'][i])

    with open(final_path, 'w') as w:
        for ori_idx, ori_data_line in enumerate(ori_data_lines):
            ori_data_line = json.loads(ori_data_line)
            task_id = ori_data_line['task_id']
            for greedy_idx, greedy_data_line in enumerate(greedy_data_lines[ori_idx * n: (ori_idx + 1) * n]):
                greedy_data_line = json.loads(greedy_data_line)

                if task_id not in modified_code_dict['task_id_list']:
                    json.dump(dict(prompt=ori_data_line['prompt'], samples=greedy_data_line['samples']), w)
                    w.write('\n')
                else:
                    entry_point = ori_data_line['entry_point']
                    idx = modified_code_dict['task_id_list'].index(task_id)
                    generated_raw_code = modified_code_dict['code_list'][greedy_idx][idx]
                    ori_prompt = ori_data_line['prompt']
                    code_completion = parse_code_wo_prompt('gpt-3.5', generated_raw_code, ori_prompt, entry_point)
                    json.dump(dict(prompt=ori_data_line['prompt'], samples=[code_completion]), w)
                    w.write('\n')

    return final_path


if __name__ == '__main__':
    inference_type = 'three_shot'
    sample_code_file = './../data/mbpp_sanitized_microsoft_sample_0.8_15_chatgpt_results.jsonl'
    test_case_file = './../data/mbpp_tests_final.jsonl'
    mbpp_file = './../data/mbpp_sanitized_microsoft.jsonl'
    greedy_generate_file = './../data/mbpp_sanitized_microsoft_greedy_0.0_1_chatgpt_results_final.jsonl'
    # greedy_generate_file = './../data/generated_test_data/test_humaneval_data_results.jsonl'
    n = 1
    synthesize_results_list = []
    # for i in range(n):
    #     synthesize_results_list.append(f'./../data/mbpp_synthesize_{inference_type}_{i}_chatgpt_results.jsonl')

    needcq_path = './../data/mbpp_needcq_chatgpt.jsonl'
    # needcq_path = runTests_getTaskID(sample_code_file, test_case_file,
    #                                  f'./../data/mbpp_needcq_chatgpt.jsonl')
    #
    for i in [0]:
        ask_path, ask_results_path = askcq_runRequest(inference_type, needcq_path,
                                                      f'./../data/mbpp_askcq_{inference_type}_{i}_chatgpt_wo_test.jsonl')  # './../data/parallel_humaneval_data_0.2_25_results_needcq.jsonl'

        answer_path, answer_results_path = answercq_runRequest(inference_type, needcq_path, ask_results_path,
                                                               f'./../data/mbpp_answercq_{inference_type}_{i}_chatgpt_wo_test.jsonl')

        # answer_path, answer_results_path = answercq_w_test_runRequest('./../data/mbpp_test_cases_chatgpt.jsonl',
        #                                                               inference_type + '_w_test', needcq_path,
        #                                                               f'./../data/mbpp_askcq_{inference_type}_{i}_chatgpt_results.jsonl',
        #                                                               f'./../data/mbpp_answercq_{inference_type}_{i}_chatgpt.jsonl')

        synthesize_path, synthesize_results_path = synthesize_runRequest(inference_type, needcq_path,
                                                                         ask_results_path,
                                                                         answer_results_path,
                                                                         f'./../data/mbpp_synthesize_{inference_type}_{i}_chatgpt_wo_test.jsonl')

        # synthesize_results_list.append(synthesize_results_path)

        generate_file(mbpp_file, greedy_generate_file, needcq_path,
                      [synthesize_results_path],
                      f'./../data/mbpp_final_{inference_type}_chatgpt_{i}_wo_test.jsonl')
