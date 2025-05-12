# gRPC-based LLM Question Answering Service

This project implements a distributed Question-Answering system using gRPC for client-server communication. The system uses a Large Language Model (LLM) to generate answers based on context retrieved from a database.

## Project Structure

```
.
└── grpc_server/           # Server-side implementation
    ├── __init__.py
    ├── db.py              # Database operations
    ├── llm.py             # LLM integration
    ├── server.py          # gRPC server implementation
    └── proto/             # Protocol Buffers definitions
        ├── llm.proto      # Service and message definitions
        ├── llm_pb2.py     # Generated protobuf code
        └── llm_pb2_grpc.py # Generated gRPC code
```

## Components Description

### Server-side Components

1. `server.py`:
   - Implements the main gRPC server
   - Handles incoming requests through the `LLMService` class
   - Uses ThreadPoolExecutor for concurrent request handling
   - Runs on port 50051

2. `db.py`:
   - Manages data retrieval operations
   - Implements context fetching for questions
   - Used to provide relevant context to the LLM

3. `llm.py`:
   - Integrates with the Language Model
   - Handles answer generation using question and context
   - Manages model interactions and response formatting

4. `proto/llm.proto`:
   - Defines the service interface
   - Specifies request and response message formats
   - Protocol Buffers service definitions



## Setup and Installation

1. Clone the repository and create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. Install all dependencies:
```powershell
pip install -r requirements.txt
```

3. Create and configure the `.env` file as described in Environment Setup section.

4. Initialize the database:
```powershell
python -m grpc_server.init_db
```

5. Generate gRPC code (if modifying the protocol):
```powershell
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. grpc_server/proto/llm.proto
```

6. Test the database connection:
```powershell
python -m grpc_server.db
```

## Running the Server

1. Start the gRPC server:
```powershell
python -m grpc_server.server
```

The server will start on localhost:50051.

## Implementation Details

### gRPC Service Definition

The service is defined in `llm.proto`:
```protobuf
service LLM {
    rpc Ask (LLMRequest) returns (LLMReply) {}
}

message LLMRequest {
    string question = 1;
}

message LLMReply {
    string answer = 1;
}
```

### Server Implementation

- The server implements the `LLMServicer` interface
- Uses ThreadPoolExecutor for handling concurrent requests
- Processes requests in these steps:
  1. Receive question from client
  2. Fetch relevant context from database
  3. Generate answer using LLM
  4. Return response to client



## Features

- gRPC server implementation
- Concurrent request handling using ThreadPoolExecutor
- Context-aware answer generation
- Integration with HuggingFace models
- Scalable design

## Notes

- The server runs on localhost:50051 by default
- Make sure all required Python packages are installed
- The system uses HuggingFace models for LLM integration
- Configure HuggingFace token in environment variables before running

## Environment Setup

1. Create a `.env` file in the project root with the following variables:
```env
# HuggingFace API token
HF_TOKEN=your_huggingface_token

# PostgreSQL database connection
DATABASE_URL=postgresql://username:password@localhost:5432/your_database



# Server Configuration
GRPC_SERVER_PORT=50051
```

2. Required Models:
- LLM: `meta-llama/Llama-4-Scout-17B-16E-Instruct`
- Provider: SambaNova

3. Database Setup:
- PostgreSQL database with a `facts` table containing:
  - `topic` (text): The topic or subject
  - `info` (text): The information content

## System Architecture

![System Architecture](image.png)

The system architecture shows:
1. gRPC server with concurrent request handling
2. Database integration for context retrieval
3. HuggingFace LLM integration for answer generation

## Testing the Server

You can use gRPC command line tools or create a simple client to test the server. Here's an example using Python's grpcio-tools:

```python
import grpc
from grpc_server.proto import llm_pb2_grpc, llm_pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = llm_pb2_grpc.LLMStub(channel)
        response = stub.Ask(llm_pb2.LLMRequest(question="What is Bitcoin?"))
        print(f"Answer: {response.answer}")

if __name__ == '__main__':
    run()
```
