from setuptools import setup, find_packages

setup(
    name="llm-grpc-service",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "python-dotenv",
        "psycopg2",
        "huggingface-hub",
    ],
)
