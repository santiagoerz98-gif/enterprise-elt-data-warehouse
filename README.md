# Enterprise Data Warehouse
This project implements a modern ELT data pipeline using the Northwind OLTP database as the source system. Its purpose is to extract operational data, store an immutable raw copy locally, transform and model the data using dbt, and load it into a DuckDB analytical warehouse.

The pipeline is orchestrated with Prefect to provide a reproducible and maintainable workflow that separates **extraction, storage, transformation, and orchestration responsibilities**.

### Architecture Components

| Component          | Technology     | Responsibility                                     |
| ------------------ | -------------- | -------------------------------------------------- |
| **Data Source**    | Northwind OLTP | Provides the operational source data               |
| **Extraction**     | Python         | Connects to Northwind and extracts the source data |
| **Raw Storage**    | Local files    | Stores the extracted data in its original/raw form |
| **Data Warehouse** | DuckDB         | Stores data for analytical querying                |
| **Transformation** | dbt            | Cleans, transforms, tests, and models the data     |
| **Orchestration**  | Prefect        | Coordinates and monitors pipeline execution        |

### Data Flow

```text
Northwind OLTP
      │
      ▼
   Python
 Extraction
      │
      ▼
  Raw Files
      │
      ▼
   DuckDB
      │
      ▼
    dbt
 Transformation
      │
      ▼
 Analytical Models
      ▲
      │
   Prefect
 Orchestration
```
