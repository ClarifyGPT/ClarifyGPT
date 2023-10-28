import json
import copy
from utils import *
from gpt4_utils import FewShotLLM
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

    if save_path is None:
        save_path = sample_code_file.replace(".jsonl", "_needcq.jsonl")

    with open(save_path, 'w') as w:
        for test_idx, tests_line in tqdm(
                enumerate(tests_lines)):  # , sample_code_line in zip(tests_lines, sample_code_lines):
            tests_line = json.loads(tests_line)
            prompt = tests_line['prompt']
            entry_point = tests_line['entry_point']
            tests = tests_line['tests']
            time_limit_func = 'import signal\nfrom contextlib import contextmanager\nclass TimeoutException(Exception): pass\n\n@contextmanager\ndef time_limit(seconds: float):\n    def signal_handler(signum, frame):\n        raise TimeoutException("Timed out!")\n    signal.setitimer(signal.ITIMER_REAL, seconds)\n    signal.signal(signal.SIGALRM, signal_handler)\n    try:\n        yield\n    finally:\n        signal.setitimer(signal.ITIMER_REAL, 0)\n'

            all_test_results = {}
            for sample_code_line in sample_code_lines[test_idx * 25: (test_idx + 1) * 25]:
                sample_code_line = json.loads(sample_code_line)
                assert prompt == sample_code_line['prompt']
                generated_raw_code = sample_code_line['raw_code_completion']
                complete_code = parse_code_w_prompt_mbpp('gpt-3.5', generated_raw_code, prompt, entry_point)
                # print(complete_code)
                # assert 1==2
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

                if str(test_result) in all_test_results.keys():
                    all_test_results[str(test_result)].append(clean_format(generated_raw_code))
                else:
                    all_test_results[str(test_result)] = [clean_format(generated_raw_code)]

            # print(len(all_test_results))
            # print('=================================')
            if len(all_test_results) > 1:
                print(len(all_test_results))
                need_cq_dict = {'task_id': tests_line['task_id'], 'prompt': prompt, 'candidate_codes': [],
                                'exec_results': list(all_test_results.keys())}
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
def askcq_runRequest(inference_type, needcq_file, askcq_path=None):
    code_llm = FewShotLLM()

    with open(needcq_file, 'r') as f:
        data_lines = f.readlines()

    if askcq_path is None:
        askcq_path = needcq_file.replace(".jsonl", "_askcq_results.jsonl")

    with open(askcq_path, 'w') as w:
        for data_line in tqdm(data_lines):
            data_line = json.loads(data_line)
            task_id = data_line['task_id']
            ori_prompt = data_line['prompt']
            candidate_codes = data_line['candidate_codes']

            code_string = ''
            for idx, candidate_c in enumerate(candidate_codes):
                code_string += f'Solution {idx}:\n{candidate_c}\n'

            if inference_type == 'zero_shot':
                assert 1 == 2
                llm_response = code_llm._completion(800, 0.0, 1,
                                                    askcq_prompt[inference_type]['instruction'],
                                                    askcq_prompt[inference_type]['examples'],
                                                    f'User Requirement:\n{ori_prompt.strip()}\n{code_string.strip()}'
                                                    f'\nAnalysis:\n{{insert your analysis results here}}'
                                                    f'\nClarifying Questions:\n{{insert your clarifying questions here}}',
                                                    )
            else:
                llm_response = code_llm._completion(800, 0.0, 1,
                                                    askcq_prompt[inference_type]['instruction'],
                                                    askcq_prompt[inference_type]['examples'],
                                                    f'User Requirement:\n{ori_prompt.strip()}\n{code_string.strip()}',
                                                    )

            for res in llm_response:
                print(res)
                print('=======================================')
                json.dump(dict(task_id=task_id, askcq=res), w)
                w.write('\n')

    return askcq_path


# 3. submit answercq task & run parallel request
def answercq_runRequest(inference_type, needcq_file, askcq_results_path, answercq_path=None):
    code_llm = FewShotLLM()

    with open(needcq_file, 'r') as f:
        ori_data_lines = f.readlines()

    with open(askcq_results_path, 'r') as f:
        data_lines = f.readlines()

    assert len(data_lines) == len(ori_data_lines)

    if answercq_path is None:
        answercq_path = askcq_results_path.replace(".jsonl", "_answercq_results.jsonl")

    with open(answercq_path, 'w') as w:
        for ori_data_line, data_line in tqdm(zip(ori_data_lines, data_lines)):
            ori_data_line = json.loads(ori_data_line)
            data_line = json.loads(data_line)
            cq = parse_cq_mbpp(data_line['askcq'])
            task_id = ori_data_line['task_id']
            ori_prompt = ori_data_line['prompt']

            # print(answercq_prompt[inference_type][0])
            # print(answercq_prompt[inference_type][1:])
            # assert 1==2
            # print(answercq_prompt[inference_type])

            llm_response = code_llm._completion(300, 0.0, 1,
                                                answercq_prompt[inference_type]['instruction'],
                                                answercq_prompt[inference_type]['examples'],
                                                f'User Requirement:\n{ori_prompt.strip()}'
                                                       f'\n\n### Clarifying Questions:\n{cq.strip()}'
                                                       f'\n\n### Answers:\n{{insert answers here}}'
                                                )

            for res in llm_response:
                print(res)
                json.dump(dict(task_id=task_id, answercq=res), w)
                w.write('\n')

    return answercq_path


def answercq_w_test_runRequest(test_file, inference_type, needcq_file, askcq_results_path, answercq_path=None):
    code_llm = FewShotLLM()

    with open(needcq_file, 'r') as f:
        ori_data_lines = f.readlines()

    with open(askcq_results_path, 'r') as f:
        data_lines = f.readlines()

    with open(test_file, 'r') as f:
        test_lines = f.readlines()

    assert len(data_lines) == len(ori_data_lines) == len(test_lines)

    if answercq_path is None:
        answercq_path = askcq_results_path.replace(".jsonl", "_answercq_results.jsonl")

    with open(answercq_path, 'w') as w:
        for ori_data_line, data_line, test_line in tqdm(zip(ori_data_lines, data_lines, test_lines)):
            ori_data_line = json.loads(ori_data_line)
            data_line = json.loads(data_line)
            test_line = json.loads(test_line)
            cq = parse_cq_mbpp(data_line['askcq'])
            task_id = ori_data_line['task_id']
            assert task_id == test_line['task_id']
            python_func = test_line['solution']
            test_cases = '\n'.join(test_line['test_list'])

            # print(answercq_prompt[inference_type][0])
            # print(answercq_prompt[inference_type][1:])
            # assert 1==2
            # print(answercq_prompt[inference_type])

            llm_response = code_llm._completion(300, 0.0, 1,
                                                answercq_prompt[inference_type]['instruction'],
                                                answercq_prompt[inference_type]['examples'],
                                                f'Python Function:\n{python_func.strip()}'
                                                       f'\nTest Cases:\n{test_cases.strip()}'
                                                       f'\n\n### Clarifying Questions:\n{cq.strip()}'
                                                       f'\n\n### Answers:\n{{insert answers here}}',
                                                )

            for res in llm_response:
                print(res)
                json.dump(dict(task_id=task_id, answercq=res), w)
                w.write('\n')

    return answercq_path


# 4. synthesize the prompt with cqs and answers
def synthesize_runRequest(inference_type, needcq_file, askcq_results_path, answercq_results_path,
                          synthesize_path=None):
    code_llm = FewShotLLM()

    with open(needcq_file, 'r') as f:
        ori_data_lines = f.readlines()

    with open(askcq_results_path, 'r') as f:
        ask_data_lines = f.readlines()

    with open(answercq_results_path, 'r') as f:
        answer_data_lines = f.readlines()

    if synthesize_path is None:
        synthesize_path = answercq_results_path.replace(".jsonl", "_synthesize_results.jsonl")

    with open(synthesize_path, 'w') as w:
        for ori_data_line, ask_data_line, answer_data_line in tqdm(zip(ori_data_lines, ask_data_lines, answer_data_lines)):
            ori_data_line = json.loads(ori_data_line)
            ask_data_line = json.loads(ask_data_line)
            answer_data_line = json.loads(answer_data_line)

            ori_prompt = ori_data_line['prompt']
            ask_cq = ask_data_line['askcq']
            answer_cq = answer_data_line['answercq']
            task_id = answer_data_line['task_id']
            clarification = parse_clarification_mbpp(ask_cq, answer_cq)
            refined_prompt = refine_prompt_clarify(ori_prompt, clarification)

            llm_response = code_llm._completion(300, 0.0, 1,
                                                synthesize_prompt[inference_type]['instruction'],
                                                synthesize_prompt[inference_type]['examples'],
                                                f'User Requirement:\n{refined_prompt}',
                                                )

            for res in llm_response:
                print(res)
                print('=================================')
                json.dump(dict(task_id=task_id, raw_code_completion=res), w)
                w.write('\n')

    return synthesize_path


# 5. generate the final humaneval file
def generate_file(humaneval_file, greedy_generate_file, synthesize_results_list, final_path=None):
    with open(humaneval_file, 'r') as f:
        ori_data_lines = f.readlines()
    with open(greedy_generate_file, 'r') as f:
        greedy_data_lines = f.readlines()

    n = len(synthesize_results_list)
    modified_code_dict = {'task_id_list': [], 'code_list': []}
    for i in range(n):
        with open(synthesize_results_list[i], 'r') as f:
            synthesize_data_lines = f.readlines()

        modified_code_dict['task_id_list'] = []
        modified_code_dict['code_list'].append([])
        for synthesize_data_line in synthesize_data_lines:
            synthesize_data_line = json.loads(synthesize_data_line)
            task_id = synthesize_data_line['task_id']
            generated_raw_code = synthesize_data_line['raw_code_completion']

            modified_code_dict['task_id_list'].append(task_id)
            modified_code_dict['code_list'][i].append(generated_raw_code)
        assert len(modified_code_dict['task_id_list']) == len(modified_code_dict['code_list'][i])

    with open(final_path, 'w') as w:
        for ori_idx, ori_data_line in tqdm(enumerate(ori_data_lines)):
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
    sample_code_file = './../data/mbpp_sanitized_microsoft_sample_0.8_25_results_final_gpt4.jsonl'
    test_case_file = './../data/mbpp_tests_final.jsonl'
    mbpp_file = './../data/mbpp_sanitized_microsoft.jsonl'
    greedy_generate_file = './../data/gpt4_greedy_mbpp/mbpp_sanitized_microsoft_greedy_0.0_3_results_final_gpt4_1.jsonl'
    # needcq_path = runTests_getTaskID(sample_code_file, test_case_file,f'./../data/mbpp_needcq_gpt4.jsonl')
    needcq_path = './../data/mbpp_needcq_gpt4.jsonl'
    n = 3
    synthesize_results_list = []
    # # for i in range(n):
    # for i in range(n):
    i = 5

    # synthesize_results_list.append(f'./../data/humaneval_synthesize_{inference_type}_{i}_gpt4_results.jsonl')
    # ask_results_path = askcq_runRequest(inference_type, needcq_path,
    #                             f'./../data/mbpp_askcq_{inference_type}_{i}_gpt4_results.jsonl')

    # answer_results_path = answercq_runRequest(inference_type, needcq_path, f'./../data/mbpp_askcq_{inference_type}_{i}_gpt4_results.jsonl',
    #                                           f'./../data/mbpp_answercq_{inference_type}_{i}_gpt4_results_wo_test.jsonl')
    # #
    # #
    # answer_results_path = answercq_w_test_runRequest('./../data/mbpp_test_cases_gpt4.jsonl', inference_type + '_w_test', needcq_path,
    #                                                  f'./../data/mbpp_askcq_{inference_type}_{i}_gpt4_results.jsonl',
    #                                                  f'./../data/mbpp_answercq_{inference_type}_{i}_gpt4_results.jsonl')

    synthesize_results_path = synthesize_runRequest(inference_type, needcq_path,
                                                    f'./../data/best_results/mbpp_askcq_three_shot_0_gpt4_results.jsonl',
                                                    f'./../data/best_results/mbpp_answercq_three_shot_0_gpt4_results_human.jsonl',
                                                    f'./../data/best_results/mbpp_synthesize_{inference_type}_0_gpt4_results_human_{i}.jsonl')

    synthesize_results_list.append(synthesize_results_path)

    generate_file(mbpp_file, greedy_generate_file,
                  synthesize_results_list,
                  f'./../data/best_results/mbpp_final_{inference_type}_gpt4_{i}_human.jsonl')
