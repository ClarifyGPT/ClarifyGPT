import json


def sort_parallel_datalines(data_lines):
    unsorted_data_line = [(int(json.loads(data_line)[0]['task_id']), data_line) for data_line in data_lines]
    sorted_data_line = sorted(unsorted_data_line, key=lambda x: x[0])
    data_lines = [item[1] for item in sorted_data_line]
    # print(len(data_lines))
    return data_lines


def getSignature(ori_prompt, entry_point):
    part_sig = '\ndef ' + entry_point
    part_sig_split = ori_prompt.split(part_sig)
    assert len(part_sig_split) == 2
    if part_sig_split[0].strip() == '':
        sig = ori_prompt.strip().split('\n')[0]
    else:
        assert len(ori_prompt.split(part_sig_split[0])) == 2
        sig = ori_prompt.split(part_sig_split[0])[-1].strip().split('\n')[0]
    assert sig[-1] == ':'
    return sig


def clean_format(generated_code):
    if "```" in generated_code:
        gen = generated_code.split("```")[1].strip()
        if gen.startswith("python"):
            gen = gen[len("python"):].strip()
    else:
        gen = generated_code

    return gen


def parse_code_w_prompt(model_name, generated_code, prompt, entry_point):
    if 'gpt-3.5' in model_name:
        gen = clean_format(generated_code)
        func_sig = 'def ' + entry_point + '('
        if gen.startswith(prompt.strip()):
            gen = gen.split(prompt.strip())[-1]
        elif func_sig in gen:
            gen_list = gen.split('\n')
            idx = 0
            for cur_gen in gen_list:
                if cur_gen.startswith(func_sig):
                    break
                else:
                    idx += 1
            if idx >= len(gen_list):
                gen = f"# CANNOT PARSE CODE SNIPPET\n{gen}"
                print(prompt)
                print(gen)
                assert 1 == 2
            gen = '\n'.join(gen_list[idx + 1:])
        else:
            gen = f"# CANNOT PARSE CODE SNIPPET\n{gen}"
            print(prompt)
            print(entry_point)
            print(gen)
            # assert 1 == 2
    else:
        pass
    return prompt + gen


def parse_code_w_prompt_mbpp(model_name, generated_code, prompt, entry_point):
    if 'gpt-3.5' in model_name:
        gen = clean_format(generated_code)
        func_sig = 'def ' + entry_point

        if func_sig in prompt:
            pre_func = prompt.split(func_sig)[0]
            gen = pre_func + gen
        else:
            gen = f"# CANNOT PARSE CODE SNIPPET\n{gen}"
            print(prompt)
            print(entry_point)
            print(gen)
    else:
        pass
    return gen


def parse_code_wo_prompt(model_name, generated_code, prompt, entry_point):
    if 'gpt-3.5' in model_name:
        gen = clean_format(generated_code)

        func_sig = 'def ' + entry_point
        if gen.startswith(prompt.strip()):
            gen = gen.split(prompt.strip())[-1]
        elif func_sig in gen:
            gen_list = gen.split('\n')
            idx = 0
            for cur_gen in gen_list:
                if cur_gen.startswith(func_sig):
                    break
                else:
                    idx += 1
            if idx >= len(gen_list):
                gen = f"# CANNOT PARSE CODE SNIPPET\n{gen}"
                print(prompt)
                print(gen)
                assert 1 == 2
            gen = '\n'.join(gen_list[idx + 1:])
        else:
            print("# CANNOT PARSE CODE SNIPPET")
            print(prompt)
            print('---------------------------')
            print(gen)
            gen_list = gen.split('\n')
            idx = 0
            for cur_gen in gen_list:
                if cur_gen.startswith('    '):
                    break
                else:
                    idx += 1
            gen = '\n'.join(gen_list[idx:])
    else:
        pass
    return gen


def parse_cq(model_name, generated_cq):
    if 'gpt-3.5' in model_name:
        if 'Clarifying Questions:' in generated_cq:
            cq = generated_cq.split('Clarifying Questions:')[-1]
        else:
            generated_cq_list = generated_cq.split('\n')
            idx = len(generated_cq_list)
            for i in list(reversed(range(len(generated_cq_list)))):
                if 'larify' in generated_cq_list[i] and 'uestions:' in generated_cq_list[i]:
                    break
                else:
                    idx -= 1
            if idx == 0:
                print('parse cq error')
                print(generated_cq)
                cq = 'No Questions.'
            else:
                cq = '\n'.join(generated_cq_list[idx:])
    else:
        pass
    return cq.strip()


def parse_cq_mbpp(generated_cq):
    assert '### Clarifying Question' in generated_cq
    generated_cq_list = generated_cq.split('\n')
    iidx = 0
    for idx in range(len(generated_cq_list)):
        iidx += 1
        if '### Clarifying Question' in generated_cq_list[idx]:
            break
    cq = '\n'.join(generated_cq_list[iidx:])
    return cq


def parse_answer(model_name, generated_ans):
    if 'gpt-3.5' in model_name:
        if 'Answers:\n' in generated_ans:
            ans = generated_ans.split('Answers:\n')[-1]
        else:
            generated_ans_list = generated_ans.split('\n')
            idx = len(generated_ans_list)
            for i in list(reversed(range(len(generated_ans_list)))):
                if 'nswers:' in generated_ans_list[i]:
                    break
                else:
                    idx -= 1
            if idx == 0:
                print('parse ans error')
                print(generated_ans)
                ans = 'No Answers.'
            else:
                ans = '\n'.join(generated_ans_list[idx:])
    else:
        pass
    return ans.strip()


def parse_clarification(generated_ask, generated_ans):
    generated_cq = parse_cq('gpt-3.5', generated_ask)
    # generated_ans = parse_ans(generated_ans)
    clarify_string = 'Clarification:\n'
    q_lines = generated_cq.strip().split('\n')
    a_lines = generated_ans.strip().split('\n')
    if len(q_lines) != len(a_lines):
        clarify_string += generated_ans.replace('\n\n', '\n')
    else:
        for idx, (q_line, a_line) in enumerate(zip(q_lines, a_lines)):
            clarify_string += f'{q_line}\n{a_line.replace(f"{idx + 1}. ", "- ")}\n'

    return clarify_string.strip()


def parse_clarification_mbpp(generated_ask, generated_ans):
    generated_ans_list = generated_ans.split('\n')
    assert '### Answer' in generated_ans_list[0]
    generated_ans = '\n'.join(generated_ans_list[1:])

    generated_cq = parse_cq_mbpp(generated_ask)
    # generated_ans = parse_ans(generated_ans)
    clarify_string = 'Clarification:\n'
    q_lines = generated_cq.strip().split('\n')
    a_lines = generated_ans.strip().split('\n')
    if len(q_lines) != len(a_lines):
        clarify_string += generated_ans.replace('\n\n', '\n')
    else:
        for idx, (q_line, a_line) in enumerate(zip(q_lines, a_lines)):
            clarify_string += f'{q_line}\n{a_line.replace(f"{idx + 1}. ", "- ")}\n'

    return clarify_string.strip()


def parse_explanation_mbpp(generated_ask, generated_ans):
    generated_ans_list = generated_ans.split('\n')
    assert '### Answer' in generated_ans_list[0]
    generated_ans = '\n'.join(generated_ans_list[1:])

    generated_cq = parse_cq_mbpp(generated_ask)
    # generated_ans = parse_ans(generated_ans)
    clarify_string = 'Explanation:\n'
    q_lines = generated_cq.strip().split('\n')
    a_lines = generated_ans.strip().split('\n')
    if len(q_lines) != len(a_lines):
        clarify_string += generated_ans.replace('\n\n', '\n')
    else:
        for idx, (q_line, a_line) in enumerate(zip(q_lines, a_lines)):
            clarify_string += f'{q_line}\n{a_line.replace(f"{idx + 1}. ", "- ")}\n'

    return clarify_string.strip()


def parse_synthesize(candidate_codes, generated_ask, generated_ans):
    code_string = ''
    assert 'Clarifying Questions:\n' in generated_ask
    generated_ask, generated_cq = generated_ask.split('Clarifying Questions:\n')
    # generated_ans = parse_ans(generated_ans)
    clarify_string = 'Clarification:\n'
    q_lines = generated_cq.strip().split('\n')
    a_lines = generated_ans.strip().split('\n')
    if len(q_lines) != len(a_lines):
        clarify_string += generated_ans.replace('\n\n', '\n')
    else:
        for idx, (q_line, a_line) in enumerate(zip(q_lines, a_lines)):
            clarify_string += f'{q_line}\n{a_line.replace(f"{idx + 1}. ", "- ")}\n'

    for idx, candidate_c in enumerate(candidate_codes):
        code_string += f'Solution {idx}:\n{candidate_c}\n'
        # assert f'Solution {idx}:\n' in generated_ask
        # code_string += generated_ask.split(f'Solution {idx + 1}:\n')[0].split(f'Solution {idx}:\n')[-1].strip() + '\n'
    return clarify_string.strip() + '\n\n' + code_string.strip()


def parse_information_ignored(generated_ask):
    assert '### Information Ignored:\n' in generated_ask
    # generated_ans = parse_ans(generated_ans)
    info = generated_ask.split('### Information Ignored:\n')[-1].strip()
    clarify_string = 'Clarification:\n' + info
    return clarify_string.strip()


def refine_prompt_clarify(ori_prompt, clarification):
    ori_prompt = ori_prompt.strip()
    assert ori_prompt[-7:] == "    '''"

    clarify_list = clarification.split('\n')
    clarification = '    ' + '\n    '.join(clarify_list) + '\n'
    refined_prompt = ori_prompt[:-7] + clarification + "    '''"
    return refined_prompt