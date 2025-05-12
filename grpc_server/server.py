import grpc
from concurrent import futures
from grpc_server.proto import llm_pb2_grpc, llm_pb2
from grpc_server.db import fetch_data
from grpc_server.llm import generate_answer

class LLMService(llm_pb2_grpc.LLMServicer):
    
    def Ask(self, request, context):
        print(f"[gRPC] Received question: {request.question}")
        context_data = fetch_data(request.question)
        if not context_data:
            context_data = request.question  # Use the question itself as context if no data is fetched
        answer = generate_answer(request.question, context_data)
        return llm_pb2.LLMReply(answer=answer)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    llm_pb2_grpc.add_LLMServicer_to_server(LLMService(), server)
    server.add_insecure_port("[::]:50051")
    print("[gRPC] Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
