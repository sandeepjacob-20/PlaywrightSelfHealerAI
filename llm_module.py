import google.generativeai as genai
import os
from pathlib import Path

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-2.5-flash')

def path_prep(path):
    path = Path(path.strip('" '))
    return path

def html_extractor(page):
    html = page.content()
    return html

def llm_caller(file_path, error, html):
    # print("Evaluating issue with LLM")
    path = path_prep(file_path)
    file_name = file_path.split('/')[-1].split('.')[0]
    html = html_extractor(html)
    if file_path == None:
        response = model.generate_content(f"can u generate some solutions to the given issue\n{error}")
        # console.print(Markdown(response.text))
        return True
    else:
        print("--- Invoking LLM")
        with open(path,"r") as f:
            file_data = f.read()
        response = model.generate_content(f"can u find a solution to the given issue\n{error}\nthe file is {file_data}\n\nhte html DOM is {html}\n\nnote: make it very brief and rewrite the whole code")
        code = response.text.split("```python\n")[1].split("```")[0]
        print(code)
        print(f"--- Rewriting error file {file_path}")
        with open(f"./fixed_files/{file_name}_fixed.py","w") as f:
            f.write(code)
        print("--- File modified and saved in fixed_files folder.")
        return True