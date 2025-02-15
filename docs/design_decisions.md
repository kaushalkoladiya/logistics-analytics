# Design Decisions Document

## Introduction
This document outlines the key design decisions for the Logistics Analytics Platform. It explains the rationale behind each choice, the trade-offs considered, and how these decisions help us achieve performance, scalability, and ease of use.

## Technology Choices

### FastAPI for API Service
- **Decision:** Build the API using FastAPI.
- **Rationale:** 
  - Provides asynchronous processing for high concurrent load.
  - Uses Pydantic for automatic data validation and auto-generated API documentation.
- **Trade-offs:** While Flask is simpler, its synchronous nature can become a bottleneck under heavy I/O.

### PostgreSQL as the Database
- **Decision:** Use PostgreSQL for data storage.
- **Rationale:** 
  - ACID-compliant with robust support for complex queries and indexing.
  - Extensible with features like partitioning and sharding.
- **Trade-offs:** Although NoSQL options like MongoDB offer flexible schemas, they lack strong relational integrity and mature analytical capabilities.

### ETL/Ingestion with Streaming and COPY
- **Decision:** Use `ijson` to stream JSON files and PostgreSQL’s COPY command for batch ingestion.
- **Rationale:**
  - Streaming avoids memory overload even with 10M+ records.
  - COPY provides significant performance benefits over row-by-row INSERT.
- **Trade-offs:** 
  - Implementing streaming and buffering introduces complexity.
  - Managing batch-level retries and error logging is necessary but adds code overhead.

### Listener for Pre-calculation
- **Decision:** Use a dedicated listener to handle precalculations.
- **Rationale:** 
  - Pre-computing aggregates ensures the API serves fast responses.
  - Decouples heavy computations from API request processing.
- **Trade-offs:** 
  - Introduces slight data staleness since aggregates are created/updated on completion of ETL process.

### Docker for Containerization and Ease of Deployment
- **Decision:** Containerize the entire system (API, ETL, PostgreSQL) using Docker.
- **Rationale:** 
  - Simplifies the development environment—developers only need Docker.
  - Provides a consistent deployment across different environments.
- **Trade-offs:** 
  - Container orchestration adds an extra abstraction layer.
  - Requires careful configuration of networking and volume management.

## Folder Structure and Organization

### Modularization
- **Separation of Concerns:** Code is organized into distinct modules (API, ETL) to maintain clarity and scalability.
- **Constants & Configurations:** A centralized constants file (e.g., `etl/ingestion/constants.py`) is used for file paths, table names, and processing parameters.

### Maintenance
- **Logging and Error Handling:** Robust logging and error handling mechanisms are built into the ETL process to manage failed batches without interrupting the overall process.

## Performance and Scalability Considerations

### Memory Efficiency
- **Streaming JSON:** Uses `ijson` to process large files without loading them entirely into memory.
- **Batch Processing:** Uses in-memory buffers (StringIO) for each batch; a new buffer is created for every batch to minimize overhead.

### Database Ingestion
- **COPY Command:** Leverages PostgreSQL’s COPY command for fast, bulk insertion.
- **Transaction Management:** Processes records in batches with commit/rollback mechanisms to ensure data consistency.

### Asynchronous Failure Handling
- **Failed Batch Logging:** Failed batches are written asynchronously to a designated folder, ensuring the ingestion process continues without delay.

### Deployment
- **Docker & docker-compose:** A root-level `docker-compose.yml` file orchestrates all services, enabling developers to run the full stack with minimal setup.

## Conclusion
The design decisions have been made with a focus on achieving high performance, scalability, and ease of use. The trade-offs made are intended to ensure that the platform can handle large-scale data ingestion and processing while remaining responsive for API consumers. This document serves as the basis for the current implementation and will guide further enhancements as needed.
