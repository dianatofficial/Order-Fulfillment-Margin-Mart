# Order Fulfillment & Margin Mart

[![CI Data Pipeline & Quality Verification](https://github.com/dianatofficial/Order-Fulfillment-Margin-Mart/actions/workflows/ci.yml/badge.svg)](https://github.com/dianatofficial/Order-Fulfillment-Margin-Mart/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.1+-FFF000.svg?logo=duckdb)](https://duckdb.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](https://www.docker.com/)

A high-performance **Supply Chain & Financial Analytics Data Mart** designed using **Kimball Dimensional Modeling** methodology. This repository provides an end-to-end analytics engineering pipeline that correlates transactional sales orders with warehouse dispatch events and carrier logistics logs to compute true daily product margins and fulfillment latency metrics.

---

## 📌 Business Context & Objective

In high-volume e-commerce and retail supply chains, gross revenue metrics often obscure operational margin erosion. Standard reporting typically evaluates top-line sales and logistics performance in separate silos:
1. **Financial Silo:** Records order sales and product manufacturing costs (COGS) without attributing real-time freight and fulfillment overhead.
2. **Logistics Silo:** Tracks carrier delivery SLAs and warehouse dispatch queues without tying delivery delays directly to product profit impact.

### Core Solution
This data mart unifies these operations by constructing:
- **`fact_daily_product_sales`**: An aggregated daily data mart at the grain of `(Date x Product x Warehouse x Carrier)` computing net revenue, product COGS, allocated parcel freight cost, and net gross profit margin.
- **`fact_order_fulfillment`**: A granular line-item fulfillment fact table tracking end-to-end supply chain cycle times (dispatch latency hours, transit days, SLA delay days, and delivery breach classifications).

---

## 🏗️ Dimensional Model (Kimball Star Schema)

```
                            +--------------------+
                            |      dim_date      |
                            +--------------------+
                            | PK  date_key       |
                            |     full_date      |
                            |     calendar_year  |
                            |     month_name     |
                            |     is_weekend     |
                            +---------+----------+
                                      |
                                      | 1:N
+--------------------+      +---------+----------+      +--------------------+
|    dim_product     |      |                    |      |   dim_warehouse    |
+--------------------+      |    fact_daily_     |      +--------------------+
| PK  product_key    |      |   product_sales    |      | PK  warehouse_key  |
|     product_id     +------+                    +------+     warehouse_id   |
|     category       | 1:N  | (Grain: Date x     | 1:N  |     facility_name  |
|     unit_cost      |      |  Product x WH x    |      |     region         |
|     list_price     |      |  Carrier)          |      |     capacity_tier  |
+--------------------+      +---------+----------+      +--------------------+
                                      |
                                      | 1:N
                            +---------+----------+
                            |    dim_carrier     |
                            +--------------------+
                            | PK  carrier_key    |
                            |     carrier_id     |
                            |     carrier_name   |
                            |     service_level  |
                            |     sla_days       |
                            +--------------------+
```

---

## 📐 Core Metric Formulations

### 1. Financial Measures
- **Net Revenue:**  
  $$\text{Net Revenue} = \text{Gross Line Sales} - \text{Promotional Discounts}$$
- **Allocated Shipping Cost:**  
  Proportionally distributed across line items by net value:  
  $$\text{Allocated Freight} = \text{Package Shipping Cost} \times \left( \frac{\text{Item Net Amount}}{\text{Order Net Total}} \right)$$
- **True Gross Margin:**  
  $$\text{Gross Margin (\$)} = \text{Net Revenue} - \text{COGS} - \text{Allocated Freight}$$
- **Gross Margin Percentage:**  
  $$\text{Gross Margin (\%)} = \frac{\text{Gross Margin (\$$\)}}{\text{Net Revenue}} \times 100$$

### 2. Supply Chain & Fulfillment Measures
- **Dispatch Latency (Hours):**  
  Elapsed duration from customer checkout to warehouse carrier handover:  
  $$\text{Dispatch Latency} = \frac{\text{Dispatched Timestamp} - \text{Order Placed Timestamp}}{3600}$$
- **Transit Time (Days):**  
  $$\text{Transit Time} = \frac{\text{Delivered Timestamp} - \text{Dispatched Timestamp}}{86400}$$
- **Delivery Delay Beyond SLA (Days):**  
  $$\text{Delivery Delay} = \max(0, \text{Transit Time} - \text{Contractual SLA Days})$$
- **On-Time Delivery Rate (%):**  
  $$\text{On-Time Delivery Rate} = \frac{\text{Total Packages} - \text{Delayed Packages}}{\text{Total Packages}} \times 100$$

---

## 📂 Repository Structure

```
Order-Fulfillment-Margin-Mart/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Automated CI data pipeline & test workflow
├── data/
│   ├── raw/                       # Staging CSV sources
│   └── processed/                 # Compressed Parquet analytical outputs
├── docs/
│   ├── architecture.md            # Dimensional architecture design document
│   └── data_dictionary.md         # Schema definitions & metric dictionary
├── src/
│   ├── config.py                  # Environment paths & business parameters
│   ├── pipeline/
│   │   ├── generate_raw_data.py   # Benchmark operational dataset generator
│   │   └── transform_mart.py      # DuckDB Kimball ELT transformation pipeline
│   ├── sql/
│   │   ├── staging/               # Staging transformation scripts
│   │   ├── dimensions/            # Conformed dimension SQL scripts
│   │   └── marts/                 # Fact tables & analytics reporting views
│   └── utils/
│       └── logger.py              # Structured logging utility
├── tests/
│   ├── test_data_integrity.py     # Referential integrity & orphan key tests
│   ├── test_mart_calculations.py  # Financial identity & metric sanity tests
│   └── test_schema_constraints.py # Primary key uniqueness & non-null assertions
├── app.py                         # Interactive Streamlit analytics dashboard
├── run_pipeline.py                # Master CLI pipeline orchestrator
├── Dockerfile                     # Container deployment image
├── docker-compose.yml             # Single-command orchestration
├── Makefile                       # Developer automation shortcuts
├── requirements.txt               # Production Python dependencies
└── README.md                      # Project documentation
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- `pip` or `conda`

### 1. Clone the Repository
```bash
git clone https://github.com/dianatofficial/Order-Fulfillment-Margin-Mart.git
cd Order-Fulfillment-Margin-Mart
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the End-to-End Data Pipeline
Execute raw dataset generation, DuckDB Kimball ELT transformations, and the automated test suite in a single command:
```bash
python run_pipeline.py --full-pipeline
```

### 4. Launch the Interactive Dashboard
Launch the interactive web application to visualize KPIs, investigate warehouse dispatch latencies, explore carrier SLA distributions, run SQL queries, and test what-if margin simulations:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment

To run the entire data mart and dashboard inside an isolated container:

```bash
docker-compose up --build
```
Access the application at `http://localhost:8501`.

---

## 🧪 Automated Testing & Data Quality Verification

The test suite validates data integrity, mathematical consistency, and relational constraints before tables are published:

```bash
pytest tests/ -v
```

### Verified Assertions:
1. **Referential Integrity:** 100% foreign key match between `fact_daily_product_sales` and conformed dimensions (`dim_product`, `dim_warehouse`, `dim_carrier`, `dim_date`).
2. **Financial Precision:** Strict validation of mathematical identity:  
   $$\text{Gross Margin} = \text{Net Revenue} - \text{COGS} - \text{Allocated Shipping}$$
3. **Metric Bounds:** Verification that `on_time_delivery_rate_pct` is bounded within $[0, 100]\%$ and fulfillment latencies are non-negative.
4. **Primary Key Uniqueness:** Strict validation of surrogate key uniqueness across all dimensions and facts.

---

## 📊 Analytical Views & Query Examples

### 1. Product Category Profitability Summary
```sql
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) AS total_skus,
    SUM(f.total_units_sold) AS units_sold,
    ROUND(SUM(f.net_revenue), 2) AS net_revenue,
    ROUND(SUM(f.total_cogs), 2) AS total_cogs,
    ROUND(SUM(f.total_allocated_shipping_cost), 2) AS shipping_freight,
    ROUND(SUM(f.gross_margin_amount), 2) AS gross_margin,
    ROUND((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 2) AS margin_pct
FROM fact_daily_product_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY gross_margin DESC;
```

### 2. Carrier SLA Compliance & Freight Efficiency Scorecard
```sql
SELECT 
    c.carrier_name,
    c.service_level,
    c.sla_contract_days,
    SUM(f.total_orders_count) AS total_shipments,
    ROUND(((SUM(f.total_line_items_count) - SUM(f.total_delayed_shipments)) * 100.0) / NULLIF(SUM(f.total_line_items_count), 0), 2) AS sla_compliance_pct,
    ROUND(AVG(f.avg_transit_time_days), 2) AS actual_transit_days,
    ROUND(SUM(f.total_allocated_shipping_cost) / NULLIF(SUM(f.total_units_sold), 0), 2) AS freight_cost_per_unit
FROM fact_daily_product_sales f
JOIN dim_carrier c ON f.carrier_key = c.carrier_key
GROUP BY c.carrier_name, c.service_level, c.sla_contract_days
ORDER BY sla_compliance_pct DESC;
```

---

## 💼 Business Use Cases & Applications

- **Supply Chain Leadership:** Identify fulfillment bottlenecks, balance warehouse loads, and negotiate carrier contracts based on empirical SLA compliance and freight drag.
- **Financial Operations & FP&A:** Calculate product-level net profitability after accounting for dynamic shipping costs and promotional markdowns.
- **Logistics Engineers:** Monitor warehouse dispatch queue performance and model transit variance across regional hubs.
- **E-Commerce Merchandising:** Discontinue or re-price heavy, low-margin products that generate negative unit economics due to shipping surcharges.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
