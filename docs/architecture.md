# System Architecture & Dimensional Modeling

## 1. Executive Summary
The **Order Fulfillment & Margin Mart** is a high-performance analytical data mart engineered to solve the disconnect between transactional e-commerce sales, fulfillment execution logs, and net profitability calculations. 

Traditional reporting often measures sales volume and shipping SLA compliance in operational silos. This data mart bridges that gap by modeling granular line-item costs, allocated freight expenses, warehouse dispatch queues, and carrier SLAs within a unified Kimball star schema.

---

## 2. Dimensional Model Architecture

```
                          +-------------------+
                          |     dim_date      |
                          |-------------------|
                          | PK  date_key      |
                          |     full_date     |
                          |     year/quarter  |
                          |     month_name    |
                          |     is_weekend    |
                          +---------+---------+
                                    |
                                    |
+-------------------+     +---------+---------+     +-------------------+
|    dim_product    |     |                   |     |   dim_warehouse   |
|-------------------|     |  fact_daily_      |     |-------------------|
| PK  product_key   +-----+  product_sales    +-----+ PK  warehouse_key |
|     product_id    |     |                   |     |     warehouse_id  |
|     category      |     | (Grain: Date x    |     |     facility_name |
|     unit_cost     |     |  Product x WH x   |     |     region        |
|     list_price    |     |  Carrier)         |     |     capacity_tier |
+-------------------+     +---------+---------+     +-------------------+
                                    |
                                    |
                          +---------+---------+
                          |    dim_carrier    |
                          |-------------------|
                          | PK  carrier_key   |
                          |     carrier_id    |
                          |     carrier_name  |
                          |     service_level |
                          |     sla_days      |
                          +-------------------+
```

---

## 3. Data Processing Layers

### Layer 1: Ingestion & Staging (`src/sql/staging/`)
- Ingests raw source logs from transactional databases and WMS (Warehouse Management System) event logs.
- Standardizes data types, validates timestamps, and enforces schema consistency.

### Layer 2: Dimensions & Conformed Dimensions (`src/sql/dimensions/`)
- **`dim_date`**: Calendar hierarchy, fiscal periods, seasons, weekend/holiday markers.
- **`dim_product`**: Product catalog metadata, category classifications, base manufacturing COGS, and standard MSRP.
- **`dim_warehouse`**: Facility metadata, geographical region, capacity tier, and automation level.
- **`dim_carrier`**: Logistics carrier contractual metadata, service levels, baseline tariffs, and contractual SLA delivery days.

### Layer 3: Fact Tables (`src/sql/marts/`)
- **`fact_order_fulfillment`**: Granular shipment line-item fact table storing individual fulfillment timestamps, package weights, allocated shipping costs, dispatch latencies, and transit SLA compliance.
- **`fact_daily_product_sales`**: Aggregated daily grain analytical mart computing gross sales, promotional deductions, net revenue, total COGS, allocated freight spend, net gross profit margin, dispatch latency hours, and on-time delivery rate.

---

## 4. Key Mathematical Formulations

### Net Revenue
$$\text{Net Revenue} = \text{Gross Sales Amount} - \text{Promotional Discounts}$$

### Allocated Shipping Cost (Proportional to Net Item Value)
$$\text{Allocated Shipping Cost} = \text{Total Package Freight Cost} \times \left( \frac{\text{Item Net Amount}}{\text{Order Net Total}} \right)$$

### True Gross Profit Margin
$$\text{Gross Profit Margin (\$) } = \text{Net Revenue} - \text{Total COGS} - \text{Allocated Shipping Cost}$$

$$\text{Gross Profit Margin (\%) } = \frac{\text{Gross Profit Margin (\$) }}{\text{Net Revenue}} \times 100$$

### Fulfillment Latencies
$$\text{Dispatch Latency (Hours)} = \frac{\text{Dispatched Timestamp} - \text{Order Placed Timestamp}}{3600}$$

$$\text{Transit Time (Days)} = \frac{\text{Delivered Timestamp} - \text{Dispatched Timestamp}}{86400}$$

$$\text{Delivery Delay (Days)} = \max(0, \text{Transit Time (Days)} - \text{SLA Target Days})$$
