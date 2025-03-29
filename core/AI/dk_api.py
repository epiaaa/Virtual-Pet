import re
import time
import threading

from openai import OpenAI


class Conversation:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.messages = [{'role': 'system', 'content': '简介回答，尽量50字以内'}]

    def get_response(self, messages, model='deepseek-chat', stream=False, print_content=False):
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream
            )
        except Exception as e:
            print(f"请求错误: {e}")
            exit()
        reasoning_content = ''
        content = ''

        if stream:
            for chunk in response:
                if model == 'deepseek-reasoner' and chunk.choices[0].delta.reasoning_content:
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                    if print_content:
                        print(chunk.choices[0].delta.reasoning_content, end='')
                elif chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    if print_content:
                        print(chunk.choices[0].delta.content, end='')
            print('\n')
        else:
            if model == 'deepseek-reasoner':
                reasoning_content = response.choices[0].message.reasoning_content
            content = response.choices[0].message.content
            if print_content:
                print(reasoning_content)
                print(content)

        end_time = time.time()
        print(f"总费时: {end_time - start_time} seconds")
        return reasoning_content, content

    def conversation(self, user_input, model='deepseek-chat', stream=False, print_content=False):
        self.messages.append({'role': 'user', 'content': user_input})
        get_response = self.get_response(self.messages, model=model, stream=stream, print_content=print_content)
        self.messages.append({'role': 'assistant', 'content': get_response[1]})
        return get_response[1]


def check_string(string):
    pattern = r'^\d.*\..*$'
    if re.match(pattern, string):
        return True
    else:
        return False


def split_data(raw):
    record_value = re.findall(r'\[.*?: (\d+\.?\d*)\]', raw)

    return record_value


# @lru_cache()
def save_prompt_data(data):
    formatter_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    path = f"./prompt_data/{formatter_time}.txt"
    with open(path, mode='a+') as save_e:
        save_e.write(data)
        save_e.write("\n")
