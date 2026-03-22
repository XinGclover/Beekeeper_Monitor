# 🐝 Beekeeper Monitor – Environmental Monitoring Data Platform 🍯

**Beekeeper Monitor** is a full-stack data engineering project designed to simulate a real-world environmental monitoring system for beekeeping operations.

The platform integrates data from multiple external sources—including weather forecasts, in-hive sensors, and wildfire alerts—and transforms them into actionable insights through a rule-based alerting system and interactive dashboards.

*This project was developed as part of a higher vocational program focused on data modeling and system design, with an emphasis on building a realistic end-to-end data pipeline.*
> 🎯 **Goal:** Enable proactive risk detection (e.g., overheating hives, humidity imbalance, wildfire threats) to support data-driven decision-making for beekeepers.

---

## 🧠 Key Features

- 📡 **Multi-source data ingestion**
  - Weather forecasts (SMHI API)
  - Hive sensor measurements (simulated IoT data)
  - Wildfire risk data

- ⚙️ **Automated data pipelines**
  - Python-based ingestion jobs
  - Scheduled data collection and processing

- 🧩 **Rule-based alert engine**
  - Configurable thresholds (temperature, humidity, fire risk)
  - Real-time anomaly detection
  - Alarm event generation

- 📊 **Analytics-first architecture**
  - SQL views as the core analytical layer
  - Pre-aggregated data for efficient querying

- 🖥️ **Interactive monitoring dashboard**
  - Built with Streamlit
  - Hierarchical filtering:  
    `location → apiary → hive → sensor`

---

## 🏗️ System Overview

The system follows a layered architecture:

### 1. External Data Sources
- Weather forecasts (SMHI Weather API)
- Environmental sensors in beehives
- Wildfire risk data

### 2. Data Ingestion Layer
Python pipelines retrieve, transform, and load data into PostgreSQL.

- Handles API integration and parsing  
- Ensures data consistency via upsert logic  
- Tracks ingestion jobs and statuses  

### 3. Data Storage Layer (PostgreSQL)

Stores structured data including:

- Locations and apiaries  
- Sensor measurements  
- Weather and wildfire data  
- Alarm rules and events  
- Scraping job metadata  

> 💡 Analytical logic is implemented using SQL views (`db/views`), keeping Python lightweight.

---

### 4. Processing & Rule Engine

The rule engine evaluates incoming data against predefined conditions:

- Temperature thresholds  
- Humidity levels  
- Wildfire severity indicators  

When conditions are met:
- Alarm events are generated  
- Contextual metadata is stored  

---

### 5. Monitoring & Analytics Layer

A Streamlit dashboard provides:

- Real-time monitoring  
- Historical trend analysis  
- Alert tracking  
- Flexible filtering across system hierarchy  

---

## 🌦️ Example: Weather Data Pipeline

The weather ingestion pipeline performs:

1. Create a scraping job record  
2. Fetch forecast data from SMHI API  
3. Parse and normalize response  
4. Store observations in PostgreSQL  
5. Update job status  

To prevent duplicates:

- Unique constraint on `(location_id, valid_time)`  
- UPSERT logic  

---

## 🧱 Architecture Summary

- **External Sources** → APIs & sensors  
- **Ingestion Layer** → Python pipelines  
- **Storage Layer** → PostgreSQL (tables + views)  
- **Processing Layer** → Rule engine  
- **Presentation Layer** → Streamlit dashboard  

---

## 🛠️ Technologies

- Python  
- PostgreSQL  
- SQL  
- REST APIs  
- psycopg2  
- python-dotenv  
- Streamlit  

---

## 📦 Repository Structure

The repository is organized into a few main modules:

- **ingestion/**  
  Data ingestion pipelines for sensors, weather, and wildfire data.

- **rule_engine/**  
  Processes incoming data and evaluates alarm rules.

- **dashboard/**  
  Streamlit application for monitoring, filtering, and visualization.

- **db/**  
  Database layer including table definitions, views, and seed data.

- **notification/**  
  Handles alert delivery (extensible component).

> For full details, please refer to the repository structure in GitHub.
