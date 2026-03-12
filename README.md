# Beekeeper Monitor – Environmental Monitoring Data Pipeline

Beekeeper Monitor is a data engineering project developed as part of a university group assignment on data modeling and system design.

The goal of the project is to design a data-driven monitoring system for beekeeping environments. The system collects and processes data from multiple sources such as weather forecasts, sensor measurements, and wildfire alerts to help beekeepers detect potential risks and respond proactively.

The project covers the full data flow, from data ingestion to rule-based alerting and monitoring dashboards.

## System Overview

The Beekeeper Monitor system consists of several components:

1. **External Data Sources**
   - Weather forecasts (SMHI Weather API)
   - Environmental sensors installed in beehives
   - Wildfire risk information

2. **Data Ingestion Layer**
   Python-based pipelines retrieve data from external APIs and sensors and store them in a PostgreSQL database.

3. **Data Storage**
   The system uses a relational database to store structured data including:
   - Locations
   - Sensor measurements
   - Weather data
   - External data sources
   - Scraping job metadata

4. **Processing and Rule Engine**
   The system evaluates predefined rules (e.g., temperature thresholds, humidity levels, fire risk indicators) to detect abnormal conditions.

5. **Alert and Notification System**
   When a rule is triggered, the system generates alarm events and notifies subscribed users through configured channels.

6. **Monitoring and Analysis**
   The stored data can be used for dashboards, monitoring tools, and historical analysis of environmental conditions affecting beehives.

## Weather Data Pipeline

In this repository, the weather ingestion pipeline retrieves forecast data from the SMHI Weather API for configured locations.

The pipeline performs the following steps:

1. Create a scraping job record
2. Retrieve weather forecasts for each location
3. Parse the API response
4. Store weather observations in the database
5. Update the job status after completion

To prevent duplicate records, the pipeline uses a unique constraint and upsert logic based on `(location_id, valid_time)`.

## Project Architecture

External Sources
        │
        ▼
Data Ingestion (Python Pipelines)
        │
        ▼
PostgreSQL Database
        │
        ▼
Rule Engine
        │
        ▼
Alarm Events & Notifications
        │
        ▼
Monitoring and Analytics


## Technologies

- Python
- PostgreSQL
- REST APIs
- psycopg2
- dotenv
- SQL

## Project Structure

ingestion/
  weather/
    client.py
    models.py
    repository.py
    pipeline.py

db/
  tables/
    location.sql
    weather_data.sql
    scraping_job.sql