import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker
from src.config import RAW_DATA_DIR, RANDOM_SEED, DEFAULT_SAMPLE_ORDER_COUNT
from src.utils.logger import logger

fake = Faker()
Faker.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

def generate_warehouses() -> pd.DataFrame:
    logger.info('Generating raw warehouse facilities...')
    warehouses = [
        {'warehouse_id': 'WH-EAST-01', 'facility_name': 'New York Metro Fulfillment Center', 'city': 'Secaucus', 'state': 'NJ', 'region': 'East', 'capacity_units_per_day': 15000, 'automation_level': 'High', 'labor_shifts': 3},
        {'warehouse_id': 'WH-WEST-01', 'facility_name': 'Los Angeles Gateway Hub', 'city': 'Ontario', 'state': 'CA', 'region': 'West', 'capacity_units_per_day': 20000, 'automation_level': 'High', 'labor_shifts': 3},
        {'warehouse_id': 'WH-CENTRAL-01', 'facility_name': 'Midwest Distribution Center', 'city': 'Joliet', 'state': 'IL', 'region': 'Midwest', 'capacity_units_per_day': 18000, 'automation_level': 'Medium', 'labor_shifts': 2},
        {'warehouse_id': 'WH-SOUTH-01', 'facility_name': 'Texas Regional Logistics Hub', 'city': 'Fort Worth', 'state': 'TX', 'region': 'South', 'capacity_units_per_day': 12000, 'automation_level': 'Medium', 'labor_shifts': 2},
        {'warehouse_id': 'WH-SOUTHEAST-01', 'facility_name': 'Atlanta Southeast Terminal', 'city': 'Forest Park', 'state': 'GA', 'region': 'Southeast', 'capacity_units_per_day': 14000, 'automation_level': 'Medium', 'labor_shifts': 2},
        {'warehouse_id': 'WH-NORTHWEST-01', 'facility_name': 'Pacific Northwest Depot', 'city': 'Kent', 'state': 'WA', 'region': 'Northwest', 'capacity_units_per_day': 10000, 'automation_level': 'High', 'labor_shifts': 2},
        {'warehouse_id': 'WH-MOUNTAIN-01', 'facility_name': 'Rocky Mountain Logistics Point', 'city': 'Aurora', 'state': 'CO', 'region': 'Mountain', 'capacity_units_per_day': 8000, 'automation_level': 'Low', 'labor_shifts': 1},
        {'warehouse_id': 'WH-MIDATLANTIC-01', 'facility_name': 'Chesapeake Logistics Center', 'city': 'Baltimore', 'state': 'MD', 'region': 'Mid-Atlantic', 'capacity_units_per_day': 11000, 'automation_level': 'Medium', 'labor_shifts': 2}
    ]
    df = pd.DataFrame(warehouses)
    df.to_csv(RAW_DATA_DIR / 'warehouses.csv', index=False)
    return df

def generate_carriers() -> pd.DataFrame:
    logger.info('Generating raw logistics carrier contracts...')
    carriers = [
        {'carrier_id': 'CR-APEX-EXP', 'carrier_name': 'Apex Express Logistics', 'service_level': 'Next-Day Air', 'sla_contract_days': 1, 'base_tariff': 19.50, 'cost_per_kg': 1.80, 'reliability_score': 0.96},
        {'carrier_id': 'CR-TITAN-GRD', 'carrier_name': 'Titan Ground Network', 'service_level': 'Standard Ground', 'sla_contract_days': 3, 'base_tariff': 7.80, 'cost_per_kg': 0.65, 'reliability_score': 0.91},
        {'carrier_id': 'CR-VELOCITY-AIR', 'carrier_name': 'Velocity Air Express', 'service_level': 'Priority 2-Day Air', 'sla_contract_days': 2, 'base_tariff': 14.20, 'cost_per_kg': 1.25, 'reliability_score': 0.94},
        {'carrier_id': 'CR-METRO-POST', 'carrier_name': 'Metro Postal Parcel', 'service_level': 'Priority Mail', 'sla_contract_days': 2, 'base_tariff': 9.50, 'cost_per_kg': 0.85, 'reliability_score': 0.88},
        {'carrier_id': 'CR-SWIFT-RGN', 'carrier_name': 'Swift Regional Freight', 'service_level': 'Regional Ground', 'sla_contract_days': 2, 'base_tariff': 7.10, 'cost_per_kg': 0.55, 'reliability_score': 0.92},
        {'carrier_id': 'CR-OMNI-ECO', 'carrier_name': 'Omni Cargo Economy', 'service_level': 'Economy Freight', 'sla_contract_days': 5, 'base_tariff': 4.90, 'cost_per_kg': 0.40, 'reliability_score': 0.84}
    ]
    df = pd.DataFrame(carriers)
    df.to_csv(RAW_DATA_DIR / 'carriers.csv', index=False)
    return df

def generate_products(n_products: int = 120) -> pd.DataFrame:
    logger.info(f'Generating {n_products} raw product catalog items...')
    categories = {
        'Consumer Electronics': [
            ('Wireless ANC Headphones', 45.0, 149.99, 0.4),
            ('4K Ultra HD Monitor 27-inch', 120.0, 299.99, 5.2),
            ('Mechanical Gaming Keyboard', 32.0, 89.99, 1.1),
            ('Smart Fitness Watch Pro', 65.0, 199.99, 0.2),
            ('Portable Power Bank 20k', 14.0, 44.99, 0.5),
            ('Ultra-Slim Tablet 10-inch', 95.0, 279.99, 0.8),
            ('Wi-Fi 6 Mesh Router System', 55.0, 169.99, 1.3),
            ('4K Action Camera Waterproof', 75.0, 219.99, 0.3)
        ],
        'Home & Kitchen': [
            ('Smart Espresso Machine', 160.0, 420.00, 7.5),
            ('Air Fryer Digital 6-Quart', 38.0, 109.99, 4.8),
            ('Robot Vacuum with LiDAR', 140.0, 379.99, 4.2),
            ('Multi-Stage Water Filter', 28.0, 79.99, 2.6),
            ('Professional High-Speed Blender', 52.0, 149.99, 3.9),
            ('Non-Stick Ceramic Cookware Set', 68.0, 189.99, 6.5)
        ],
        'Apparel & Footwear': [
            ('Pro Cushion Running Shoes', 24.0, 119.99, 0.9),
            ('Weatherproof Alpine Parka', 55.0, 229.99, 1.8),
            ('Thermal Performance Hoodie', 16.0, 64.99, 0.6),
            ('Ergonomic Commuter Backpack', 22.0, 79.99, 1.2),
            ('Water-Resistant Trail Jacket', 30.0, 129.99, 0.7)
        ],
        'Health & Personal Care': [
            ('Sonic Electric Toothbrush Kit', 18.0, 69.99, 0.5),
            ('Deep Tissue Percussion Gun', 35.0, 129.99, 1.4),
            ('Smart Body Composition Scale', 19.0, 59.99, 1.6),
            ('Ionic Salon Hair Dryer', 26.0, 89.99, 0.9)
        ],
        'Office & Workspace': [
            ('Ergonomic Mesh Task Chair', 110.0, 299.99, 16.5),
            ('Electric Dual-Motor Standing Desk', 175.0, 479.99, 28.0),
            ('Heavy-Duty Dual Monitor Arm', 28.0, 84.99, 4.0),
            ('Architect LED Desk Lamp', 15.0, 49.99, 1.5)
        ],
        'Industrial & Tools': [
            ('Cordless Brushless Drill Set', 58.0, 159.99, 3.5),
            ('Digital Laser Distance Meter', 18.0, 54.99, 0.3),
            ('120-Piece Mechanics Socket Set', 42.0, 119.99, 7.0),
            ('High-Pressure Washer 2000PSI', 85.0, 229.99, 9.2)
        ]
    }

    products = []
    prod_idx = 1
    for category, items in categories.items():
        for base_name, base_cost, base_msrp, base_weight in items:
            for variant in ['Standard', 'Plus', 'Pro', 'Edition']:
                sku = f'SKU-{category[:3].upper()}-{prod_idx:04d}'
                name = f'{base_name} ({variant})'
                cost = round(base_cost * random.uniform(0.9, 1.25), 2)
                msrp = round(base_msrp * random.uniform(0.95, 1.2), 2)
                weight = round(base_weight * random.uniform(0.9, 1.15), 2)
                products.append({
                    'product_id': sku,
                    'product_name': name,
                    'category': category,
                    'unit_cost': cost,
                    'list_price': msrp,
                    'weight_kg': weight,
                    'is_hazardous': False
                })
                prod_idx += 1
                if len(products) >= n_products:
                    break
            if len(products) >= n_products:
                break
        if len(products) >= n_products:
            break

    df = pd.DataFrame(products)
    df.to_csv(RAW_DATA_DIR / 'products.csv', index=False)
    return df

def generate_customers(n_customers: int = 3000) -> pd.DataFrame:
    logger.info(f'Generating {n_customers} customer profiles...')
    segments = ['Retail Consumer', 'Premium VIP', 'B2B Commercial']
    states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'WA', 'VA', 'AZ', 'CO', 'MA', 'TN']
    
    customers = []
    for i in range(1, n_customers + 1):
        cust_id = f'CUST-{i:06d}'
        customers.append({
            'customer_id': cust_id,
            'customer_name': fake.company() if random.random() < 0.15 else fake.name(),
            'customer_segment': random.choices(segments, weights=[0.70, 0.20, 0.10])[0],
            'customer_state': random.choice(states),
            'signup_date': fake.date_between(start_date='-3y', end_date='-30d').strftime('%Y-%m-%d')
        })
    df = pd.DataFrame(customers)
    df.to_csv(RAW_DATA_DIR / 'customers.csv', index=False)
    return df

def generate_orders_and_fulfillments(
    df_products: pd.DataFrame,
    df_warehouses: pd.DataFrame,
    df_carriers: pd.DataFrame,
    df_customers: pd.DataFrame,
    n_orders: int = DEFAULT_SAMPLE_ORDER_COUNT
):
    logger.info(f'Generating {n_orders} transactional orders and fulfillment logs...')
    
    start_date = datetime(2025, 1, 1, 0, 0, 0)
    end_date = datetime(2025, 12, 31, 23, 59, 59)
    total_seconds = int((end_date - start_date).total_seconds())

    channels = ['Web Store', 'Mobile App', 'B2B Direct', 'Marketplace Hub']
    channel_weights = [0.45, 0.35, 0.10, 0.10]
    
    product_records = df_products.to_dict('records')
    warehouse_ids = df_warehouses['warehouse_id'].tolist()
    carrier_records = df_carriers.to_dict('records')
    carrier_lookup = {c['carrier_id']: c for c in carrier_records}
    customer_ids = df_customers['customer_id'].tolist()

    orders = []
    order_items = []
    fulfillments = []
    
    item_id_counter = 1
    fulfillment_id_counter = 1

    for order_idx in range(1, n_orders + 1):
        order_id = f'ORD-2025-{order_idx:07d}'
        cust_id = random.choice(customer_ids)
        channel = random.choices(channels, weights=channel_weights)[0]
        
        # Seasonality: higher volume in Q4 (Oct-Dec)
        month_bias = random.choices(
            range(1, 13),
            weights=[0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.09, 0.11, 0.14, 0.13]
        )[0]
        day = random.randint(1, 28)
        hour = random.choices(range(24), weights=[1,1,1,1,2,3,4,6,8,9,10,10,9,9,9,8,8,7,6,5,4,3,2,1])[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        order_placed_at = datetime(2025, month_bias, day, hour, minute, second)

        # Number of line items
        num_items = random.choices([1, 2, 3, 4, 5], weights=[0.55, 0.25, 0.12, 0.05, 0.03])[0]
        selected_prods = random.sample(product_records, k=num_items)

        order_gross_amount = 0.0
        order_discount_amount = 0.0
        order_total_weight = 0.0

        for prod in selected_prods:
            qty = random.choices([1, 2, 3, 5], weights=[0.75, 0.18, 0.05, 0.02])[0]
            unit_price = prod['list_price']
            discount_pct = random.choices([0.0, 0.05, 0.10, 0.15, 0.25], weights=[0.60, 0.15, 0.12, 0.08, 0.05])[0]
            discount_val = round(unit_price * qty * discount_pct, 2)
            line_total = round((unit_price * qty) - discount_val, 2)
            
            order_gross_amount += unit_price * qty
            order_discount_amount += discount_val
            order_total_weight += prod['weight_kg'] * qty

            order_items.append({
                'order_item_id': f'ITEM-{item_id_counter:08d}',
                'order_id': order_id,
                'product_id': prod['product_id'],
                'quantity': qty,
                'unit_price': unit_price,
                'unit_cost': prod['unit_cost'],
                'discount_amount': discount_val,
                'line_total_amount': line_total
            })
            item_id_counter += 1

        orders.append({
            'order_id': order_id,
            'customer_id': cust_id,
            'order_channel': channel,
            'order_placed_at': order_placed_at.strftime('%Y-%m-%d %H:%M:%S'),
            'gross_order_amount': round(order_gross_amount, 2),
            'total_discount_amount': round(order_discount_amount, 2),
            'net_order_amount': round(order_gross_amount - order_discount_amount, 2),
            'order_status': 'Completed'
        })

        # Warehouse dispatch assignment
        warehouse_id = random.choice(warehouse_ids)
        carrier_obj = random.choice(carrier_records)
        carrier_id = carrier_obj['carrier_id']
        sla_days = carrier_obj['sla_contract_days']

        # Dispatch latency (hours): normal distribution around 14h, with tail up to 48h
        # Mountain / Manual warehouses take longer
        base_latency_mean = 12.0 if '01' in warehouse_id and ('EAST' in warehouse_id or 'WEST' in warehouse_id) else 18.0
        dispatch_latency_hours = max(2.0, np.random.normal(loc=base_latency_mean, scale=7.0))
        
        # Occasional warehouse backlog (5% chance of 30-50h delay)
        if random.random() < 0.05:
            dispatch_latency_hours += random.uniform(20.0, 35.0)
            
        dispatched_at = order_placed_at + timedelta(hours=dispatch_latency_hours)

        # Promised delivery calculation (SLA in calendar/business days from order placed)
        promised_delivery_dt = order_placed_at + timedelta(days=sla_days, hours=4)

        # Transit duration (days)
        # Carrier reliability dictates delay probability
        reliability = carrier_obj['reliability_score']
        is_carrier_delayed = random.random() > reliability
        
        if is_carrier_delayed:
            transit_days = sla_days + random.uniform(0.8, 3.5)
        else:
            transit_days = max(0.4, np.random.normal(loc=sla_days * 0.85, scale=0.25))

        delivered_at = dispatched_at + timedelta(days=transit_days)

        # Shipping cost calculation
        shipping_cost = round(
            carrier_obj['base_tariff'] + 
            (order_total_weight * carrier_obj['cost_per_kg']) + 
            random.uniform(1.0, 3.5),
            2
        )

        fulfillments.append({
            'fulfillment_id': f'FUL-{fulfillment_id_counter:08d}',
            'order_id': order_id,
            'warehouse_id': warehouse_id,
            'carrier_id': carrier_id,
            'order_placed_at': order_placed_at.strftime('%Y-%m-%d %H:%M:%S'),
            'dispatched_at': dispatched_at.strftime('%Y-%m-%d %H:%M:%S'),
            'promised_delivery_date': promised_delivery_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'delivered_at': delivered_at.strftime('%Y-%m-%d %H:%M:%S'),
            'shipping_cost': shipping_cost,
            'package_weight_kg': round(order_total_weight, 2),
            'fulfillment_status': 'Delivered'
        })
        fulfillment_id_counter += 1

    df_orders = pd.DataFrame(orders)
    df_items = pd.DataFrame(order_items)
    df_fuls = pd.DataFrame(fulfillments)

    df_orders.to_csv(RAW_DATA_DIR / 'orders.csv', index=False)
    df_items.to_csv(RAW_DATA_DIR / 'order_items.csv', index=False)
    df_fuls.to_csv(RAW_DATA_DIR / 'fulfillments.csv', index=False)

    logger.info(f'Generated {len(df_orders)} orders, {len(df_items)} items, {len(df_fuls)} fulfillments.')

def main():
    logger.info('Starting Synthetic Raw Supply Chain Dataset Generation...')
    df_wh = generate_warehouses()
    df_cr = generate_carriers()
    df_pr = generate_products(n_products=120)
    df_cu = generate_customers(n_customers=3000)
    generate_orders_and_fulfillments(df_pr, df_wh, df_cr, df_cu, n_orders=DEFAULT_SAMPLE_ORDER_COUNT)
    logger.info('Raw dataset generation complete and saved to data/raw/.')

if __name__ == '__main__':
    main()
