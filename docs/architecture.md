# Architecture Document

## Overview
This document describes the overall system architecture for the Logistics Analytics Platform. The system is designed to efficiently process large logistics datasets (millions of records), provide actionable analytics via a web dashboard, and be easy to deploy for developers—all with minimal setup.

## System Components

### 1. API Service (FastAPI)
- **Purpose:** Exposes RESTful endpoints for querying shipments, vehicle logs, and vehicles. Pre-calculate and refresh aggregates (e.g., materialized views, summary tables) to ensure fast API responses.
- **Features:**
  - Asynchronous handling using FastAPI for high throughput.
  - Data validation via Pydantic schemas.
  - Organized structure with separate folders for routes, models, schemas, and business logic.
  - Operates independently of API and ETL services.
  
### 2. ETL/Ingestion Service
- **Purpose:** Efficiently ingest and process large JSON files containing logistics data.
- **Features:**
  - Streams JSON files using `ijson` to avoid full memory load.
  - Uses an in-memory buffer (via `StringIO`) to batch records.
  - Loads data into PostgreSQL using the high-performance `COPY` command.
  - Implements transaction management, retries (with exponential backoff), and error logging.
  - Logs failed batches asynchronously to a designated folder for later reprocessing.
  - Supports ingestion for multiple datasets (vehicle_logs, shipments, vehicles) using a centralized constants file.

### 3. Database (PostgreSQL)
- **Purpose:** Acts as the central data store for transactional data, historical records, and precomputed analytics.
- **Features:**
  - Strong ACID compliance and robust indexing.
  - Schema versioning via Alembic migrations.
  - Deployed in a Docker container, enabling an out-of-the-box setup.
  - Internal networking allows backend services to connect using container names.

### 4. Docker & Orchestration
- **Purpose:** Provide a containerized, easy-to-deploy environment for all system components.
- **Features:**
  - Each service (API, ETL, PostgreSQL) is containerized.
  - A root-level `docker-compose.yml` orchestrates the multi-container setup.
  - Environment variables and configuration files allow seamless switching between development and production.
  - Optionally expose non-conflicting ports for local development (e.g., mapping PostgreSQL to port 5433).

## Data Flow
1. **Ingestion:**
   - Raw JSON files are placed in the `data/raw` folder.
   - The ETL service streams and validates these files, batching records and loading them into PostgreSQL using COPY.
   - Failed batches are recorded asynchronously for later reprocessing.
  
2. **Pre-calculation:**
   - The API creates/refreshes aggregates (e.g., recalculating average delivery times) materialized views or summary tables upon completion of ETL.

3. **API Serving:**
   - The API service retrieves precomputed results from the database (or a caching layer if implemented) and provides endpoints for data queries.
   - The API remains highly responsive since it does not perform heavy calculations on-the-fly.

## Deployment Architecture
- **Containerization:** All components are dockerized, ensuring that developers can run the full stack with a single Docker command.
- **Networking:** Containers communicate over a shared network; for example, the API connects to PostgreSQL using its service name.
- **Configuration Management:** Environment variables (via `.env` files) control database credentials, batch sizes, and other key settings.
- **Scalability:** The modular architecture allows for independent scaling of the API, and ETL.
