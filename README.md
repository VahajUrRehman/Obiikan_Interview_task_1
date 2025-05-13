# gRPC-based LLM Question Answering Service

This project implements a distributed Question-Answering system using gRPC for
client-server communication. The system uses a Large Language Model (LLM) to
generate answers based on context retrieved from a database.

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

1. Install all dependencies:

```powershell
pip install -r requirements.txt
```

2. Create and configure the `.env` file as described in Environment Setup
   section.

3. Generate gRPC code (if modifying the protocol):

```powershell
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. grpc_server/proto/llm.proto
```

4. Test the database connection:

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
```

## Database

```
## Database Setup:
- PostgreSQL database with a `facts` table containing:
  - `topic` (text): The topic or subject
  - `info` (text): The information content


  CREATE TABLE facts (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    info TEXT
);
```

These Are SOme Queries Or sample Data I Used To Work On

```
INSERT INTO facts (topic, info) VALUES
-- ERP Topic: Inventory Management
('Inventory Management', 'Inventory management is a critical function in ERP systems, involving the tracking of raw materials, work-in-progress goods, and finished products. It ensures the right stock is in the right place at the right time, reducing costs and improving efficiency. ERP software automates these processes, offering real-time visibility into stock levels, reorder points, and supplier lead times. Features like barcode scanning and batch tracking enhance accuracy. Companies use inventory forecasting to prepare for demand fluctuations. Integration with sales and procurement helps maintain stock balance. It also enables return management and quality control. Overall, effective inventory management supports better decision-making and customer satisfaction.'),

-- ERP Topic: Accounts Payable Automation
('Accounts Payable', 'Accounts payable (AP) automation in ERP systems streamlines the process of paying vendors and suppliers. It reduces manual data entry, eliminates paper invoices, and helps avoid late fees through better scheduling. Integrated OCR (Optical Character Recognition) tools can scan and digitize invoices. Matching invoices with purchase orders and receipts ensures accuracy. Automation helps prevent fraud by implementing approval workflows. ERP-based AP solutions also integrate with banking systems to automate payments. AP dashboards provide insights into outstanding liabilities and cash flow. This function is vital for maintaining supplier relationships and ensuring compliance with financial controls.'),

-- General Tech Topic: Cloud Computing
('Cloud Computing', 'Cloud computing is the on-demand delivery of IT resources over the Internet, allowing users to access storage, computing power, and applications without physical infrastructure. It provides scalability, cost savings, and accessibility. There are three main models: IaaS (Infrastructure as a Service), PaaS (Platform), and SaaS (Software). Cloud services can be public, private, or hybrid. Popular providers include AWS, Azure, and Google Cloud. Businesses use cloud platforms to host ERP systems, data warehouses, and analytics tools. Cloud computing improves collaboration and supports remote work. Security, compliance, and service-level agreements are critical aspects to manage.'),

-- Tech Topic: REST APIs
('REST APIs', 'REST (Representational State Transfer) APIs are a set of web service principles used for building scalable web services. They use standard HTTP methods like GET, POST, PUT, and DELETE to perform operations on resources. REST APIs are stateless, meaning each request contains all necessary information. Data is typically exchanged in JSON format. REST APIs are widely used in modern ERP systems to integrate with external applications such as CRMs, eCommerce platforms, and third-party logistics providers. They allow developers to interact with the backend without exposing internal architecture. REST enables flexibility and supports mobile, web, and IoT clients.'),

-- Business Topic: Customer Relationship Management (CRM)
('Customer Relationship Management', 'CRM systems are designed to manage a company’s interactions with current and potential customers. They help track communications, manage leads, and streamline the sales pipeline. ERP systems often include integrated CRM modules or connect to external CRM platforms like Salesforce or HubSpot. CRMs provide insights into customer behavior, purchase history, and preferences. They improve customer service and retention. Features include contact management, sales forecasting, and campaign tracking. Automation in CRM helps send reminders, emails, and follow-ups. A centralized view of the customer enables better decision-making across sales, marketing, and service teams.'),

-- General Topic: SQL Joins
('SQL Joins', 'SQL joins are used to combine rows from two or more tables based on a related column. The most common types of joins are INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN. An INNER JOIN returns only matching records, while a LEFT JOIN includes all records from the left table and matching ones from the right. RIGHT JOIN is the opposite, and FULL OUTER JOIN returns all records when there is a match in one of the tables. Joins are fundamental for querying relational databases, allowing users to build comprehensive views of data from normalized table structures. They are critical in ERP systems for linking modules like sales, inventory, and finance.'),

-- ERP Topic: Procurement Lifecycle
('Procurement Process', 'Procurement in ERP systems encompasses the end-to-end process of acquiring goods and services. It starts with identifying a need, followed by requisition, approval, vendor selection, purchase order creation, delivery, invoice receipt, and payment. Automation ensures compliance with company policies and budgets. ERP procurement modules provide tools for managing supplier relationships, negotiating contracts, and tracking spend. Integration with inventory and finance ensures that stock levels and budgets are updated in real time. Modern systems also include analytics for spend optimization. Procurement plays a strategic role in cost control and operational efficiency.'),

-- Educational Topic: Data Normalization
('Data Normalization', 'Data normalization is the process of organizing data to reduce redundancy and improve integrity in relational databases. It involves dividing large tables into smaller, related ones and defining relationships between them. There are several normal forms (1NF, 2NF, 3NF, etc.) that guide the normalization process. In ERP systems, normalized databases help ensure consistent and scalable storage of information such as customer records, orders, and products. Normalization reduces anomalies in insert, update, and delete operations. However, over-normalization can impact performance, which is why a balanced design is important for transactional systems.'),

-- General Topic: Time Tracking
('Time Tracking Systems', 'Time tracking tools allow businesses to record employee hours for payroll, project billing, and productivity monitoring. Integrated with ERP systems, they automate timesheet approvals, leave tracking, and workforce analysis. Features include clock-in/out, geofencing, and mobile access. Accurate time tracking supports compliance with labor laws and enhances transparency in client billing. Advanced systems can integrate with project management tools and support job costing. Real-time dashboards provide insights into time allocation across departments. Time data feeds directly into financial modules, helping HR and accounting teams reduce errors and administrative workload.'),

-- ERP Topic: Business Intelligence in ERP
('ERP Business Intelligence', 'Business Intelligence (BI) tools integrated into ERP systems allow organizations to analyze data and make informed decisions. These tools pull data from various ERP modules, including finance, sales, operations, and HR. Dashboards, visualizations, and reports help track KPIs, trends, and anomalies. ERP BI enables forecasting, budgeting, and scenario analysis. With self-service analytics, users can explore data without relying on IT. Integration with external data sources provides a holistic view of business performance. Advanced BI capabilities may include machine learning, predictive analytics, and natural language queries. BI transforms raw ERP data into actionable insights.');
```

## Outputs

![Responses](outputs/response.png) ![Database](outputs/database.png)

The system architecture shows:

1. gRPC server with concurrent request handling
2. Database integration for context retrieval
3. HuggingFace LLM integration for answer generation

## Testing the Server

You can use gRPC command line tools or create a simple client to test the
server. Here's an example using Python's grpcio-tools:

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
