import google.generativeai as genai
import os
from pathlib import Path
# using the local ollama model
import ollama
os.environ["API_KEY"] = "wdeff"
# Ensure the API key is set for Google Generative AI
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-2.5-flash')
   
def generator(error,file_data,html, llm_mode):
    message = f"can u find a solution to the given issue\n{error}\nthe file is {file_data}\n\nhte html DOM is {html}\n\nnote: make it very brief and rewrite the whole code"
    if llm_mode == 'endpoint':

        response = model.generate_content(message)
        return response.text.split("```python\n")[1].split("```")[0]
    
    elif llm_mode == 'local':
        
        response = ollama.generate(
            model='gemma3:4b',
            prompt=message
        )
        print(response['response'])
        return response['response'].split("```python\n")[1].split("```")[0]

def path_prep(path):
    path = Path(path.strip('" '))
    return path

def html_extractor(page,error,llm_mode):
    html = page.content()
    prompt = f"based on the error given below\n{error}\nCan u extract the required html DOM from {html}\n\nnote: i want only the html DOM in the response and nothing else\n\nmake sure to wrap the html DOM in ```html\n and ```"
    if llm_mode == 'endpoint':
        response = model.generate_content(prompt)
        html = response.text.split("```html\n")[1].split("```")[0]
    elif llm_mode == 'local':
        response = ollama.generate(
            model='gemma3:4b',
            prompt=prompt
        )
        html = response['response'].split("```html\n")[1].split("```")[0]
    return html
    
def get_file_name(file_path):
    if os.name == 'nt':
        return file_path.split('\\')[-1].split('.')[0]
    else:
        return file_path.split('/')[-1].split('.')[0]      

def llm_caller(file_path, error, html, llm_mode):
    # print("Evaluating issue with LLM")
    path = path_prep(file_path)
    file_name = get_file_name(file_path)
    print("--- Extracting HTML information")
    html = html_extractor(html,error,llm_mode)
    print("--- Invoking LLM")
    with open(path,"r") as f:
        file_data = f.read()
    code = generator(error,file_data,html, llm_mode)
    print(code)
    print(f"--- Rewriting error file {file_path}")
    try:
        with open(f"./fixed_files/{file_name}_fixed.py","w") as f:
            f.write(code)
        print("--- File modified and saved in fixed_files folder.")
        return True
    except Exception as e:
        print(f"--- Failed to save the modified file: {e}")
        return False
