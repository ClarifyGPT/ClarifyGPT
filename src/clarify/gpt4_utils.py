import time
from typing import Dict, List, Tuple, Callable, Union

import requests


class Role:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class FewShotLLM(object):
    def __init__(self, **kwargs) -> None:
        self.url = 'xxxx'
        self.api_key = 'xxxxx'
        self.headers = {'Content-Type': 'application/json', 'api-key': self.api_key}

    def _generate_completion_prompt(self, messages: List[Dict[str, str]]) -> str:
        return "\n".join([message['content'] for message in messages])

    def _generate_chat_completion_messages(self,
                                           instruction: str,
                                           examples: List[Dict[str, str]],
                                           prompt: str) -> List[Dict[str, str]]:
        messages = [
            {"role": Role.SYSTEM, "content": instruction}
        ]

        if examples:
            for example in examples:
                messages.append({"role": Role.USER, "content": example[Role.USER]})
                messages.append({"role": Role.ASSISTANT, "content": example[Role.ASSISTANT]})

        messages.append({"role": Role.USER, "content": prompt})

        return messages

    def _request(self, max_tokens, temperature, n, messages: List[Dict[str, str]]) -> str:
        params = {"max_tokens": max_tokens, "temperature": temperature, "n": n, "stop": None, "top_p": 0.95,
                  "messages": messages}

        resp = requests.post(self.url, json=params, headers=self.headers)

        return resp.json()

    def _completion(self,
                    max_tokens: int,
                    temperature: float,
                    n: int,
                    instruction: str,
                    examples: List[Dict[str, str]],
                    prompt: str) -> List[str]:

        messages = self._generate_chat_completion_messages(instruction, examples, prompt)

        cnt = 0
        while cnt < 1000:
            try:
                return [self._request(max_tokens, temperature, n, messages)['choices'][i]['message']['content']
                        for i in range(n)]

            except Exception as e:
                print("[Request Error]", e.args[0], f"retrying with sleep {cnt} secs...")
                cnt += 1
                # time.sleep(0.001)

        raise Exception(f"Fail to request OpenAI services with max_retries = {cnt}")


class CodeLLM(FewShotLLM):
    def generate_code(self,
                      max_tokens: int,
                      temperature: float,
                      n: int,
                      instruction: str,
                      examples: List[Dict[str, str]],
                      prompt: str,
                      extract_code_fn: Callable[[str], Union[str, Tuple[str, str]]]) -> Union[str, Tuple[str, str]]:
        completion = self._completion(max_tokens, temperature, n, instruction, examples, prompt)

        if extract_code_fn is not None:
            return extract_code_fn(completion)
        else:
            return completion