### Hi there 👋
This is a replication package for ClarifyGPT: A Framework for Enhancing LLM-based Code Generation via Requirement Clarification.

### Project Summary
Large Language Models (LLMs) have demonstrated impressive capabilities in automatically generating code from provided natural language requirements. However, in real-world practice, it is inevitable that the requirements written by users might be ambiguous or insufficient. Current LLMs will directly generate programs according to those unclear requirements regardless of interactive clarification, which will likely deviate from the origin user intents. To bridge that gap, we introduce a novel framework named ClarifyGPT, which aims to enhance code generation by empowering LLMs with the ability to identify ambiguous requirements and ask targeted clarifying questions. In particular, ClarifyGPT first detects whether a given requirement is ambiguous by performing a code consistency check. If it is ambiguous, ClarifyGPT prompts an LLM to generate targeted clarifying questions. After receiving question responses, ClarifyGPT refines the ambiguous requirement and inputs it into the same LLM to generate a final code solution. To evaluate our ClarifyGPT, we first conduct a human evaluation involving ten participants who use ClarifyGPT for code generation on two publicly available benchmarks: MBPP-sanitized and MBPP-ET. The results show that ClarifyGPT elevates the performance (Pass@1) of GPT-4 from 70.96% to 80.80% on MBPP-sanitized. Furthermore, to perform large-scale automated evaluations of ClarifyGPT across different LLMs and benchmarks without requiring user participation, we introduce a high-fidelity simulation method to simulate user responses. The automated evaluation results also demonstrate that ClarifyGPT can significantly enhance code generation performance compared to the baselines.

### File organization
- baseline ## baseline method GPT-Eingeering
- evaluation ## the evaluation dataset and scripts
  - human-eval ## HumanEval benchmark openai_humaneval
  - MBPP ## MBPP benchmark google_mbpp
- src ## the source code of our method ClarifyGPT
  - prompt ## the designed prompts for HumanEval and MBPP
  - clarify ## the main scripts to run ClarifyGPT
  
### Run & Evaluation
Run ClairfyGPT on HumanEval or MBPP
```
python src/run_clarify_{model_name}_{benchmark}.py
For example:
python src/run_clarify_chatgpt_mbpp.py
```
Calculate the pass@1 metrics
```
python evaluation/MBPP/main.py
```
