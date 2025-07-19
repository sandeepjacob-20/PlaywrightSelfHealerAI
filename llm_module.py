import google.generativeai as genai
import os
from pathlib import Path
# using the local ollama model
import ollama

# genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-2.5-flash')

def generator(error,file_data,html, llm_mode):
    if llm_mode == 'endpoint':
        response = model.generate_content(f"can u find a solution to the given issue\n{error}\nthe file is {file_data}\n\nhte html DOM is {html}\n\nnote: make it very brief and rewrite the whole code")
        return response.text.split("```python\n")[1].split("```")[0]
    elif llm_mode == 'local':
        message = f"can u find a solution to the given issue\n{error}\nthe file is {file_data}\n\nhte html DOM is {html}\n\nnote: make it very brief and rewrite the whole code"
        response = ollama.generate(
            model='gemma3:4b',
            prompt=message
        )
        print(response['response'])
        return response['response'].split("```python\n")[1].split("```")[0]

def path_prep(path):
    path = Path(path.strip('" '))
    return path

def html_extractor(page):
    html = page.content()
    return html

def llm_caller(file_path, error, html, llm_mode):
    # print("Evaluating issue with LLM")
    path = path_prep(file_path)
    file_name = file_path.split('/')[-1].split('.')[0]
    html = html_extractor(html)
    print("--- Invoking LLM")
    with open(path,"r") as f:
        file_data = f.read()
    code = generator(error,file_data,html, llm_mode)
    print(code)
    print(f"--- Rewriting error file {file_path}")
    with open(f"./fixed_files/{file_name}_fixed.py","w") as f:
        f.write(code)
    print("--- File modified and saved in fixed_files folder.")
    return True
