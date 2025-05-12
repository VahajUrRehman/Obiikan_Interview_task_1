from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc
import sys
from pathlib import Path
import os

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from grpc_server.proto import llm_pb2_grpc, llm_pb2

app = FastAPI(
    title="LLM Service API",
    description="FastAPI integration with gRPC LLM service",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str  # Matches the proto definition exactly

class QuestionResponse(BaseModel):
    answer: str    # Matches the proto definition exactly

@app.get("/")
async def root():
    return {
        "service": "LLM Question Answering API",
        "endpoints": {
            "/ask": "POST - Ask a question to the LLM"
        }
    }

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        # Create gRPC channel
        channel = grpc.insecure_channel('localhost:50051')
        stub = llm_pb2_grpc.LLMStub(channel)
        
        # Create gRPC request matching proto definition
        grpc_request = llm_pb2.LLMRequest(question=request.question)
        
        # Call gRPC service
        grpc_response = stub.Ask(grpc_request)
        
        # Return response matching proto definition
        return QuestionResponse(answer=grpc_response.answer)
        
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=503,
            detail=f"LLM Service Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server Error: {str(e)}"
        )
    finally:
        if 'channel' in locals():
            channel.close()
