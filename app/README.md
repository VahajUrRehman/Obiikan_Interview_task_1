# FastAPI with gRPC LLM Service

This FastAPI application provides a REST API interface to interact with the gRPC LLM service.

## Installation

1. Install dependencies (from project root):
```powershell
cd d:\Obikan\Obiikan_Interview_task_1
pip install -e .
cd app
pip install -r requirements.txt
```

This ensures both the gRPC server package and the FastAPI dependencies are installed correctly.

## Running the Application

1. First, ensure the gRPC server is running:
```powershell
cd grpc_server
python -m grpc_server.server
```

2. In a new terminal, start the FastAPI application:
```powershell
cd app
uvicorn main:app --reload
```

3. Access the API documentation at:
```
http://localhost:8000/docs
```

## API Endpoints

### GET /
- Root endpoint
- Returns a welcome message

### POST /ask
- Submit a question to the LLM
- Request body: `{"text": "your question here"}`
- Returns: `{"answer": "LLM's response", "error": null}`

## Example Usage

Using curl:
```powershell
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"text\":\"What is cloud computing?\"}"
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"text": "What is cloud computing?"}
)
print(response.json())
