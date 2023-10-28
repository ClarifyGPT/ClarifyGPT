# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import argparse
import json
import logging
import os

from postprocess import PostProcessor
from execution import evaluate_with_test_code
from evaluation import pass_at_K

logging.basicConfig(
    format="SystemLog: [%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path_for_solution", type=str, help="model input file in .jsonl format",
                        default='./../../src/data/MBPP_ET_v2.jsonl')  # mbpp_sanitized_microsoft.jsonl # MBPP_ET_v2.jsonl
    parser.add_argument("--predict_path_for_solution", type=str, help="model output file in .jsonl format",
                        default='./../../src/data/mbpp_final_three_shot_gpt4_1.jsonl')
    # './../../src/data/mbpp_final_zero_shot_gpt4_3.jsonl'
    # './../../src/data/gpt4_greedy_mbpp/mbpp_sanitized_microsoft_greedy_0.0_3_results_final_gpt4_1.jsonl'
    # parser.add_argument("--source_path_for_test", type=str, help="model input file in .jsonl format")
    # parser.add_argument("--predict_path_for_test", type=str, help="model output file in .jsonl format")

    args = parser.parse_args()
    
    handled_solutions, task_count = PostProcessor.map_task_id_for_solution(args.predict_path_for_solution, args.source_path_for_solution)
    # handled_test_cases = PostProcessor.map_task_id_for_test_case(args.predict_path_for_solution, args.source_path_for_solution)
    # print(handled_test_cases)
    # assert 1==2
    ground_truth_exec_result = evaluate_with_test_code(handled_solutions, timeout=0.1)
    with open(args.predict_path_for_solution.replace('.jsonl', '.results_jsonl'), 'w') as w:
        for data_line in ground_truth_exec_result:
            json.dump(data_line, w)
            w.write('\n')
    logger.info('pass rates of random solutions')
    pass_at_K(ground_truth_exec_result)