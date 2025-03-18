import openai
import requests
import os
import re

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  

# Receiver API URL
RECEIVER_API_URL = "http://127.0.0.1:8001/execute"

def generate_code():
    """Generates Python code for adding two numbers."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate a Python script for the task of the user. Return only the python code, without any markdown code blocks, or explanations."},
                {"role": "user", "content": "Generate Python code for adding two numbers."}
            ]
        )

        code = response.choices[0].message.content.strip()
        code = re.sub(r'```(?:python)?\s*', '', code)
        code = re.sub(r'```', '', code)
        print(code)

        return code

    except Exception as e:
        return f"Error generating code: {str(e)}"

def send_to_execution(code):
    """Sends generated code to the execution API and retrieves the result."""
    try:
        execution_response = requests.post(RECEIVER_API_URL, json={"code": code})

        if execution_response.status_code == 200:
            return execution_response.json()
        else:
            return {"error": f"Execution API Error: {execution_response.status_code}", "details": execution_response.text}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Step 1: Generate Code
    generated_code = generate_code()

    # Step 2: Send to Receiver for Execution
    execution_result = send_to_execution(generated_code)

    # Step 3: Store result in a variable
    final_result = execution_result
    print("Final Result Obtained from the API : ",final_result)

