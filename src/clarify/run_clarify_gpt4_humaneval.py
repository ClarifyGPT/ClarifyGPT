import json
import copy
from utils import *
from gpt4_utils import FewShotLLM
from src.prompt.prompt_humaneval import *
import functools
from threading import Thread
from tqdm import tqdm


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

    if save_path is None:
        save_path = sample_code_file.replace(".jsonl", "_needcq.jsonl")

    with open(save_path, 'w') as w:
        for test_idx, tests_line in tqdm(
                enumerate(tests_lines)):  # , sample_code_line in zip(tests_lines, sample_code_lines):
            tests_line = json.loads(tests_line)
            prompt = tests_line['prompt']
            entry_point = tests_line['entry_point']
            func_sig = getSignature(prompt, entry_point)
            tests = tests_line['tests']
            all_test_results = {}

            for sample_code_line in sample_code_lines[test_idx * 25: (test_idx + 1) * 25]:
                sample_code_line = json.loads(sample_code_line)
                task_id = sample_code_line['task_id']
                assert task_id == tests_line['task_id']
                generated_raw_code = sample_code_line['completion']
                complete_code = prompt + generated_raw_code
                # print(complete_code)
                # assert 1==2
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
                    all_test_results[str(test_result)].append(func_sig + '\n' + generated_raw_code)
                else:
                    all_test_results[str(test_result)] = [func_sig + '\n' + generated_raw_code]

            # print(len(all_test_results))
            # print('=================================')
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
            cq = parse_cq('gpt-3.5', data_line['askcq'])
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
                                                f'\n\nClarifying Questions:\n{cq.strip()}'
                                                f'\n\nAnswers:\n{{insert your answers here}}',
                                                )

            for res in llm_response:
                print(res)
                json.dump(dict(task_id=task_id, answercq=res), w)
                w.write('\n')

    return answercq_path


# 3. submit answercq task & run parallel request
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
            cq = parse_cq('gpt-3.5', data_line['askcq'])
            task_id = ori_data_line['task_id']
            python_func = test_line['solution']
            test_func = test_line['test_func']

            llm_response = code_llm._completion(300, 0.0, 1,
                                                answercq_prompt[inference_type]['instruction'],
                                                answercq_prompt[inference_type]['examples'],
                                                f'Python Function:\n{python_func.strip()}'
                                                       f'\nTest Cases:\n{test_func.strip()}'
                                                       f'\n\nClarifying Questions:\n{cq.strip()}'
                                                       f'\n\nAnswers:\n{{insert answers here}}'
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
        for ori_data_line, ask_data_line, answer_data_line in tqdm(
                zip(ori_data_lines, ask_data_lines, answer_data_lines)):
            ori_data_line = json.loads(ori_data_line)
            ask_data_line = json.loads(ask_data_line)
            answer_data_line = json.loads(answer_data_line)

            ori_prompt = ori_data_line['prompt']
            ask_cq = ask_data_line['askcq']
            answer_cq = answer_data_line['answercq']
            task_id = answer_data_line['task_id']
            clarification = parse_clarification(ask_cq, answer_cq)

            llm_response = code_llm._completion(300, 0.0, 1,
                                                synthesize_prompt[inference_type]['instruction'],
                                                synthesize_prompt[inference_type]['examples'],
                                                f'User Requirement:\n{ori_prompt.strip()}'
                                                f'\n{clarification}',
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
    sample_code_file = './../data/human-eval-v2-20210705_sample_gpt4_0.8_25_results_final.jsonl'
    test_case_file = './../data/humaneval_tests_final.jsonl'
    humaneval_file = './../data/human-eval-v2-20210705.jsonl'
    needcq_path = f'./../data/humaneval_needcq_gpt4.jsonl'
    # needcq_path = runTests_getTaskID(sample_code_file, test_case_file,
    #                                  f'./../data/humaneval_needcq_gpt4.jsonl')

    # greedy_generate_file = './../data/human-eval-v2-20210705_greedy_0.0_5_results_final.jsonl_results.jsonl'
    greedy_generate_file = './../data/gpt4_greedy/human-eval-v2-20210705_greedy_gpt4_0.0_5_results_final_0.jsonl'
    synthesize_results_list = []
    # for i in range(n):
    # synthesize_results_list.append(f'./../data/humaneval_synthesize_{inference_type}_{5}_gpt4_results.jsonl')

    # ask_results_path = f'./../data/humaneval_askcq_{inference_type}_2_gpt4_results.jsonl'
    # for i in range(n):
    i = 2
    # ask_results_path = askcq_runRequest(inference_type, needcq_path,
    #                             f'./../data/humaneval_askcq_{inference_type}_{i}_gpt4_results_w_test.jsonl')
    # #
    # # answer_results_path = answercq_runRequest(inference_type, needcq_path, ask_results_path,
    # #                                           f'./../data/humaneval_answercq_{inference_type}_{i}_gpt4_results.jsonl')
    #
    # answer_results_path = answercq_w_test_runRequest('./../data/humaneval_test_cases_gpt4.jsonl',
    #                                                  inference_type + '_w_test', needcq_path, ask_results_path,
    #                                                  f'./../data/humaneval_answercq_{inference_type}_{i}_gpt4_results_w_test.jsonl')

    synthesize_results_path = synthesize_runRequest(inference_type, needcq_path,
                                                    './../data/best_results/humaneval_askcq_three_shot_0_gpt4_results_w_test.jsonl',
                                                    './../data/best_results/humaneval_answercq_three_shot_0_gpt4_results_w_test_human.jsonl',
                                            f'./../data/best_results/humaneval_synthesize_{inference_type}_0_gpt4_results_w_test_human_{i}.jsonl')

    # synthesize_results_list.append(synthesize_results_path)
    #
    generate_file(humaneval_file, greedy_generate_file,
                  [synthesize_results_path],
                  f'./../data/best_results/humaneval_final_{inference_type}_gpt4_w_test_human_{i}.jsonl')
