from fastapi import FastAPI, HTTPException
import subprocess
import os
import tempfile

app = FastAPI()

@app.post("/execute")
async def execute_code(payload: dict):
    """Executes the received Python code and returns the result."""
    code = payload.get("code", "")

    if not code:
        raise HTTPException(status_code=400, detail="No code received")

    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Execute the code and capture the output
        result = subprocess.run(
            ["python3", temp_file_path],  # Use "python3" for Render compatibility
            capture_output=True, text=True
        )

        # Remove the temporary file after execution
        os.remove(temp_file_path)

        return {"output": result.stdout.strip(), "errors": result.stderr.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
