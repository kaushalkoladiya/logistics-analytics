# Logistics Analytics Platform

A comprehensive platform for processing and analyzing logistics data, consisting of an ETL pipeline and a REST API service for data visualization and analytics.

## Overview

This application consists of three main components:

1. **ETL Service**: Processes logistics data including:
   - Vehicle information
   - Vehicle trip logs
   - Shipment records
   
2. **API Service**: FastAPI-based REST API providing:
   - Route performance analytics
   - Vehicle metrics
   - Shipment cost analysis
   - Real-time data visualization endpoints

3. **PostgreSQL Database**: Stores processed data and supports analytics queries

## Prerequisites

- Docker and Docker Compose
- npm (for frontend development)

## Environment Setup

1. Create a `.env` file in the root directory:

```env
# Database Configuration
DB_NAME=logistics_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

# ETL Configuration
BATCH_SIZE=10000
MAX_RETRIES=3

# API Configuration
API_PORT=8000
```

## Running the Application

1. **Start all services using Docker Compose:**
```bash
docker-compose up --build
```

2. **Start individual services:**
```bash
# Start only the database
docker-compose up postgres

# Start ETL process
docker-compose up etl

# Start API service
docker-compose up api
```

3. **Stop all services:**
```bash
docker-compose down
```

4. **Start frontend:**
```bash
cd client
npm install
npm run dev
```

## Data Processing

The ETL service processes three types of JSON files:
- `vehicles.json`: Vehicle information
- `vehicle_logs.json`: Trip logs for vehicles
- `shipments.json`: Shipment records

Place these files in `etl/data/raw/` directory before starting the ETL service.

## API Endpoints

Once the API service is running, you can access:

- `http://localhost:8000/api/route/reliability` - Route reliability metrics
- `http://localhost:8000/api/route/cost-value` - Route cost analysis
- `http://localhost:8000/api/vehicles/metrics` - Vehicle performance metrics
- `http://localhost:8000/api/shipments` - Shipment analytics
- Many more

## Monitoring

- ETL progress can be monitored through the container logs
- Failed records are stored in `etl/data/failed/`
- API service includes built-in logging for request tracking

## Development

1. **Local Development Setup:**
```bash
# API Service
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ETL Service
cd etl
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Running Tests:**
```bash
# Coming soon
```

## Troubleshooting

1. **Database Connection Issues:**
   - Ensure PostgreSQL container is running
   - Check database credentials in .env
   - Verify network connectivity between containers

2. **ETL Processing Failures:**
   - Check logs in ETL container
   - Inspect failed records in etl/data/failed/
   - Verify input data format

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
