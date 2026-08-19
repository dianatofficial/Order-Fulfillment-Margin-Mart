# Data Mart Data Dictionary

## Dimension: `dim_product`
| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `product_key` | INTEGER | Primary Key | Surrogate key for product entity |
| `product_id` | VARCHAR | Natural Key | Business SKU identifier |
| `product_name` | VARCHAR | - | Full descriptive name of product |
| `category` | VARCHAR | - | High-level product taxonomy category |
| `unit_cost` | DECIMAL(10,2) | - | Standard manufacturing cost of goods sold (COGS) |
| `list_price` | DECIMAL(10,2) | - | Retail list selling price (MSRP) |
| `standard_margin_amount` | DECIMAL(10,2) | - | Expected nominal margin per unit (`list_price - unit_cost`) |
| `target_margin_pct` | DECIMAL(5,2) | - | Theoretical gross margin percentage |
| `margin_tier` | VARCHAR | - | Margin classification ('High', 'Medium', 'Low') |
| `weight_kg` | DECIMAL(8,2) | - | Unit package weight in kilograms |

---

## Dimension: `dim_warehouse`
| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `warehouse_key` | INTEGER | Primary Key | Surrogate key for fulfillment center |
| `warehouse_id` | VARCHAR | Natural Key | Business facility code (e.g. WH-EAST-01) |
| `facility_name` | VARCHAR | - | Full name of warehouse facility |
| `city` | VARCHAR | - | Facility location city |
| `state` | VARCHAR | - | Facility location state code |
| `region` | VARCHAR | - | Geographic sales region |
| `capacity_units_per_day` | INTEGER | - | Maximum design throughput units per day |
| `capacity_tier` | VARCHAR | - | Scale classification ('Tier 1 Mega Hub', 'Tier 2 Regional', etc.) |
| `automation_level` | VARCHAR | - | Facility automation status ('High', 'Medium', 'Low') |

---

## Dimension: `dim_carrier`
| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `carrier_key` | INTEGER | Primary Key | Surrogate key for logistics carrier |
| `carrier_id` | VARCHAR | Natural Key | Logistics service provider code |
| `carrier_name` | VARCHAR | - | Carrier legal name |
| `service_level` | VARCHAR | - | Service class ('Next-Day Air', 'Standard Ground', etc.) |
| `sla_contract_days` | INTEGER | - | Contractual delivery commitment threshold in days |
| `base_tariff` | DECIMAL(10,2) | - | Baseline parcel dispatch tariff |
| `cost_per_kg` | DECIMAL(10,2) | - | Variable weight surcharge per kilogram |

---

## Fact Table: `fact_daily_product_sales`
| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `date_key` | INTEGER | Foreign Key | References `dim_date.date_key` |
| `product_key` | INTEGER | Foreign Key | References `dim_product.product_key` |
| `warehouse_key` | INTEGER | Foreign Key | References `dim_warehouse.warehouse_key` |
| `carrier_key` | INTEGER | Foreign Key | References `dim_carrier.carrier_key` |
| `total_orders_count` | BIGINT | Measure | Count of distinct orders fulfilled |
| `total_line_items_count` | BIGINT | Measure | Count of individual order line items |
| `total_units_sold` | BIGINT | Measure | Total units sold across all lines |
| `gross_revenue` | DECIMAL(12,2) | Measure | Sum of gross sales before discounts |
| `total_discounts_amount` | DECIMAL(12,2) | Measure | Sum of promotional deductions |
| `net_revenue` | DECIMAL(12,2) | Measure | Gross revenue minus discounts |
| `total_cogs` | DECIMAL(12,2) | Measure | Direct cost of goods sold |
| `total_allocated_shipping_cost` | DECIMAL(12,2) | Measure | Proportional shipping cost allocated to product lines |
| `gross_margin_amount` | DECIMAL(12,2) | Measure | Net revenue minus COGS minus shipping costs |
| `gross_margin_pct` | DECIMAL(5,2) | Measure | Gross margin expressed as percentage of net revenue |
| `total_delayed_shipments` | BIGINT | Measure | Number of shipments exceeding carrier SLA |
| `total_delayed_dispatches` | BIGINT | Measure | Number of dispatches exceeding 24h warehouse queue |
| `on_time_delivery_rate_pct` | DECIMAL(5,2) | Measure | Percentage of shipments delivered within SLA |
| `avg_dispatch_latency_hours` | DECIMAL(6,2) | Measure | Average elapsed hours between order placement and dispatch |
| `avg_transit_time_days` | DECIMAL(6,2) | Measure | Average carrier transit duration in days |
| `avg_delivery_delay_days` | DECIMAL(6,2) | Measure | Average days delayed past contractual SLA |
