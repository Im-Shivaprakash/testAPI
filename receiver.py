from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import io
import sys

app = FastAPI()

# Define a request model
class CodeRequest(BaseModel):
    code: str

@app.post("/execute")
async def execute_code(payload: CodeRequest):
    """Executes the received Python code directly in memory."""
    code = payload.code

    if not code:
        raise HTTPException(status_code=400, detail="No code received")

    try:
        # Capture standard output and errors
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        sys.stdout = stdout_buffer  # Redirect stdout
        sys.stderr = stderr_buffer  # Redirect stderr

        exec(code, {"__builtins__": {}}, {})  # Execute in a restricted environment

        sys.stdout = sys.__stdout__  # Restore stdout
        sys.stderr = sys.__stderr__  # Restore stderr

        return {
            "output": stdout_buffer.getvalue().strip(),
            "errors": stderr_buffer.getvalue().strip()
        }

    except Exception as e:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        raise HTTPException(status_code=500, detail=str(e))
