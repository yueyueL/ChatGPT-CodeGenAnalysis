import openai
import os
import re
import json

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "Your OpenAI API key" 
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_chatgpt_response(prompt, model='gpt-3.5-turbo', temperature=0):
    """
    Returns the response from ChatGPT for a given prompt
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=temperature,
    )
    return response


def get_code_from_response(text, language):
    if "```" not in text:
        return text.strip()

    if f"```{language}" in text:
        pattern = rf'```{language}(.*?)```'
    else:
        pattern = r'```(.*?)```'

    code_blocks = re.findall(pattern, text, re.DOTALL)
    return ''.join(code_blocks).strip()


def generate_code(output_dir, lang="python"):
    """
    Generates code from ChatGPT for a given code task
    """

    tasks_meta_path = r"path/to/leetcode_tasks/leetcode.json"
    with open(tasks_meta_path, 'r') as f:
        tasks_meta_lists = json.load(f)

    for task_meta in tasks_meta_lists:
        task_id = task_meta['id']
        task_name = task_meta['name']
        task_description = task_meta['task_description']
        
        messages_prompt = f"Please provide a code implementation of the following description:\n{task_description}"
        template_key = f"{lang}_template"
        if template_key in task_meta:
            messages_prompt += f"\nProvide a valid {lang} code with this template:\n{task_meta[template_key]}"

        messages = [{"role": "system", "content": f"Your task is to write a {lang} program"}]
        messages.append({"role": "user", "content": messages_prompt})
        response = get_chatgpt_response(messages)

        code = get_code_from_response(response.choices[0].message.content, lang)
        if lang == "python":
            output_file = os.path.join(output_dir, f"{task_id}-{task_name}.py")
        else:
            output_file = os.path.join(output_dir, f"{task_id}-{task_name}.java")

        with open(output_file, 'w') as f:
            f.write(code)

if __name__ == "__main__":
    output_directory = "path/to/data/results/code/python/"
    generate_code(output_directory, lang="python")
    # generate_code(output_directory, lang="java")
