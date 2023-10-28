import json
import copy
from utils import *
from src.parallel_request import parallel_request_openai
from src.prompt.prompt_humaneval import *
import functools
from threading import Thread


def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e

            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret

        return wrapper

    return deco


# 1. run sample codes on tests, get task_id of the unclear prompts
def runTests_getTaskID(sample_code_file, tests_file, save_path=None):
    def execute_generated_code(code_to_be_test):
        loc = {}
        exec(code_to_be_test, loc)
        return loc['xx']

    with open(tests_file, 'r') as f:
        tests_lines = f.readlines()

    with open(sample_code_file, 'r') as f:
        sample_code_lines = f.readlines()

    # sort
    sample_code_lines = sort_parallel_datalines(sample_code_lines)

    if save_path is None:
        save_path = sample_code_file.replace(".jsonl", "_needcq.jsonl")

    with open(save_path, 'w') as w:
        for tests_line, sample_code_line in zip(tests_lines, sample_code_lines):
            tests_line = json.loads(tests_line)
            sample_code_line = json.loads(sample_code_line)
            task_id = 'HumanEval/' + str(sample_code_line[0]['task_id'])
            assert task_id == tests_line['task_id']
            prompt = tests_line['prompt']
            entry_point = tests_line['entry_point']
            tests = tests_line['tests']

            all_test_results = {}
            for i in range(25):
                generated_raw_code = sample_code_line[2]['choices'][i]["message"]['content']
                complete_code = parse_code_w_prompt('gpt-3.5', generated_raw_code, prompt, entry_point)
                test_result = []
                for test in tests:
                    test_list = test.split('\n')
                    test_list[-1] = 'xx = ' + test_list[-1]
                    test = '\n'.join(test_list)

                    code_to_be_test = complete_code + '\n\n' + test
                    exec_code_func = timeout(seconds_before_timeout=1)(execute_generated_code)
                    try:
                        return_value = exec_code_func(code_to_be_test)
                    except Exception:
                        return_value = 'error!!!'

                    test_result.append(return_value)

                if str(test_result) in all_test_results.keys():
                    all_test_results[str(test_result)].append(clean_format(generated_raw_code))
                else:
                    all_test_results[str(test_result)] = [clean_format(generated_raw_code)]

            if len(all_test_results) > 1:
                # print(task_id, len(all_test_results))
                need_cq_dict = {'task_id': task_id, 'prompt': prompt, 'candidate_codes': []}
                for v in all_test_results.values():
                    need_cq_dict['candidate_codes'].append(v[0])
                    # print(len(v))
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
                             max_tokens=720,
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
            cq = parse_cq('gpt-3.5', data_line[2]['choices'][0]["message"]['content'])
            ori_prompt = ori_data_line['prompt']

            openai_messages = copy.deepcopy(answercq_prompt[inference_type])
            openai_messages.append({
                'role': 'user',
                'content': f'User Requirement:\n{ori_prompt.strip()}'
                           f'\n\nClarifying Questions:\n{cq.strip()}'
                           f'\n\nAnswers:\n{{insert your answers here}}'
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
    assert len(data_lines) == len(ori_data_lines)

    if answercq_path is None:
        answercq_path = askcq_results_path.replace(".jsonl", "_answercq.jsonl")

    with open(answercq_path, 'w') as w:
        for ori_data_line, data_line, test_line in zip(ori_data_lines, data_lines, test_lines):
            ori_data_line = json.loads(ori_data_line)
            data_line = json.loads(data_line)
            test_line = json.loads(test_line)
            assert ori_data_line['task_id'] == test_line['task_id']
            cq = parse_cq('gpt-3.5', data_line[2]['choices'][0]["message"]['content'])
            python_func = test_line['solution']
            test_func = test_line['test_func']

            openai_messages = copy.deepcopy(answercq_prompt[inference_type])
            openai_messages.append({
                'role': 'user',
                'content': f'Python Function:\n{python_func.strip()}'
                           f'\nTest Cases:\n{test_func.strip()}'
                           f'\n\nClarifying Questions:\n{cq.strip()}'
                           f'\n\nAnswers:\n{{insert answers here}}'
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
    # assert  1== 2
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
            clarification = parse_clarification(ask_cq, answer_cq)

            openai_messages = copy.deepcopy(synthesize_prompt[inference_type])
            openai_messages.append({
                'role': 'user',
                'content': f'User Requirement:\n{ori_prompt.strip()}'
                           f'\n{clarification}'
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
            # assert 1==2
            json_string = json.dumps(json_dict)
            w.write(json_string + "\n")

    if synthesize_results_path is None:
        parallel_request_openai(requests_filepath=synthesize_path)
        synthesize_results_path = synthesize_path.replace(".jsonl", "_results.jsonl")
    else:
        parallel_request_openai(requests_filepath=synthesize_path, save_filepath=synthesize_results_path)

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
                    json.dump(dict(task_id=task_id, completion=greedy_data_line['completion']), w)
                    w.write('\n')
                else:
                    entry_point = ori_data_line['entry_point']
                    idx = modified_code_dict['task_id_list'].index(task_id)
                    generated_raw_code = modified_code_dict['code_list'][greedy_idx][idx]
                    ori_prompt = ori_data_line['prompt']
                    code_completion = parse_code_wo_prompt('gpt-3.5', generated_raw_code, ori_prompt, entry_point)
                    json.dump(dict(task_id=task_id, completion=code_completion), w)
                    w.write('\n')

    return final_path


if __name__ == '__main__':
    inference_type = 'three_shot'
    sample_code_file = './../data/parallel_humaneval_data_0.2_25_results.jsonl'
    test_case_file = './../data/humaneval_tests_final.jsonl'
    humaneval_file = './../data/human-eval-v2-20210705.jsonl'
    # greedy_generate_file = './../data/human-eval-v2-20210705_greedy_0.0_5_results_final.jsonl'
    greedy_generate_file = './../data/generated_test_data/test_humaneval_data_results.jsonl'
    n = 3
    synthesize_results_list = []
    # for i in range(n):
    #     synthesize_results_list.append(f'./../data/humaneval_synthesize_{inference_type}_{i}_chatgpt_results.jsonl')

    needcq_path = './../data/humaneval_needcq_chatgpt.jsonl'
    # needcq_path = runTests_getTaskID(sample_code_file, test_case_file,
    #                                  f'./../data/humaneval_needcq_chatgpt.jsonl')

    # for i in range(n):
    #     # ask_path, ask_results_path = askcq_runRequest(inference_type, needcq_path,
    #     #                                               f'./../data/humaneval_askcq_{inference_type}_{i}_chatgpt.jsonl')  # './../data/parallel_humaneval_data_0.2_25_results_needcq.jsonl'
    #
    #     # answer_path, answer_results_path = answercq_runRequest(inference_type, needcq_path, ask_results_path,
    #     #                                                        f'./../data/humaneval_answercq_{inference_type}_{i}_chatgpt.jsonl')
    #
    #     answer_path, answer_results_path = answercq_w_test_runRequest('./../data/humaneval_test_cases_chatgpt.jsonl',
    #                                                                   inference_type + '_w_test', needcq_path,
    #                                                                   f'./../data/{inference_type}_results/humaneval_askcq_{inference_type}_{i}_results.jsonl',
    #                                                                   f'./../data/humaneval_answercq_{inference_type}_{i}_chatgpt_w_test.jsonl')
    #
    #     synthesize_path, synthesize_results_path = synthesize_runRequest(inference_type, needcq_path,
    #                                                                      f'./../data/{inference_type}_results/humaneval_askcq_{inference_type}_{i}_results.jsonl',
    #                                                                      answer_results_path,
    #                                                                      f'./../data/humaneval_synthesize_{inference_type}_{i}_chatgpt_w_test.jsonl')

    synthesize_results_list.append('./../data/one_shot_results/humaneval_synthesize_one_shot_4_results.jsonl')

    generate_file(humaneval_file, greedy_generate_file, needcq_path, synthesize_results_list,
                  f'./../data/one_shot_results/humaneval_final_one_shot_4.jsonl')
