import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from src.config import DUCKDB_PATH, DATA_DIR

st.set_page_config(
    page_title="Order Fulfillment & Margin Mart",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
        .main-header { font-size: 1.8rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
        .sub-header { font-size: 0.95rem; color: #64748B; margin-bottom: 1.5rem; }
        .kpi-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; }
        .kpi-title { font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600; }
        .kpi-val { font-size: 1.6rem; font-weight: 700; color: #0F172A; }
        .kpi-sub { font-size: 0.8rem; color: #10B981; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_db_connection():
    return duckdb.connect(str(DUCKDB_PATH), read_only=True)

con = get_db_connection()

# Sidebar Filters
st.sidebar.title("🎛️ Mart Filters")

categories = con.execute("SELECT DISTINCT category FROM dim_product ORDER BY category").df()['category'].tolist()
selected_categories = st.sidebar.multiselect("Product Category", options=categories, default=categories)

warehouses = con.execute("SELECT DISTINCT facility_name FROM dim_warehouse ORDER BY facility_name").df()['facility_name'].tolist()
selected_warehouses = st.sidebar.multiselect("Warehouse Facility", options=warehouses, default=warehouses)

carriers = con.execute("SELECT DISTINCT carrier_name FROM dim_carrier ORDER BY carrier_name").df()['carrier_name'].tolist()
selected_carriers = st.sidebar.multiselect("Logistics Carrier", options=carriers, default=carriers)

# Dynamic SQL Filtering
cat_clause = "AND dp.category IN (" + ",".join([f"'{c}'" for c in selected_categories]) + ")" if selected_categories else "AND 1=0"
wh_clause = "AND dw.facility_name IN (" + ",".join([f"'{w}'" for w in selected_warehouses]) + ")" if selected_warehouses else "AND 1=0"
cr_clause = "AND dc.carrier_name IN (" + ",".join([f"'{c}'" for c in selected_carriers]) + ")" if selected_carriers else "AND 1=0"

filter_query = f"""
    FROM fact_daily_product_sales f
    JOIN dim_product dp ON f.product_key = dp.product_key
    JOIN dim_warehouse dw ON f.warehouse_key = dw.warehouse_key
    JOIN dim_carrier dc ON f.carrier_key = dc.carrier_key
    JOIN dim_date dd ON f.date_key = dd.date_key
    WHERE 1=1 {cat_clause} {wh_clause} {cr_clause}
"""

# Header
st.markdown('<div class="main-header">Order Fulfillment & Margin Mart</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Dimensional Data Warehouse & Supply Chain Intelligence Engine (Kimball Star Schema)</div>', unsafe_allow_html=True)

# Executive KPIs
kpi_query = f"""
    SELECT
        COALESCE(SUM(f.gross_revenue), 0) AS gross_rev,
        COALESCE(SUM(f.net_revenue), 0) AS net_rev,
        COALESCE(SUM(f.total_cogs), 0) AS total_cogs,
        COALESCE(SUM(f.total_allocated_shipping_cost), 0) AS total_shipping,
        COALESCE(SUM(f.gross_margin_amount), 0) AS gross_margin,
        COALESCE((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 0) AS margin_pct,
        COALESCE(SUM(f.total_units_sold), 0) AS total_units,
        COALESCE(SUM(f.total_orders_count), 0) AS total_orders,
        COALESCE(((SUM(f.total_line_items_count) - SUM(f.total_delayed_shipments)) * 100.0) / NULLIF(SUM(f.total_line_items_count), 0), 0) AS on_time_rate,
        COALESCE(AVG(f.avg_dispatch_latency_hours), 0) AS avg_dispatch_hr,
        COALESCE(AVG(f.avg_transit_time_days), 0) AS avg_transit_days
    {filter_query}
"""
kpi_df = con.execute(kpi_query).df()

if not kpi_df.empty:
    k = kpi_df.iloc[0]
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Net Revenue", f"${k['net_rev']:,.0f}", f"${k['gross_rev']:,.0f} Gross")
    c2.metric("Gross Margin", f"${k['gross_margin']:,.0f}", f"{k['margin_pct']:.1f}% Margin")
    c3.metric("Total COGS", f"${k['total_cogs']:,.0f}")
    c4.metric("Shipping Freight", f"${k['total_shipping']:,.0f}")
    c5.metric("On-Time Delivery", f"{k['on_time_rate']:.1f}%", "SLA Target >90%")
    c6.metric("Avg Dispatch Latency", f"{k['avg_dispatch_hr']:.1f} hrs", f"{k['avg_transit_days']:.1f}d transit")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Margin & Revenue Analysis",
    "🏭 Warehouse & Dispatch Performance",
    "🚚 Carrier Logistics & SLA",
    "💻 SQL Workbench & Mart Explorer",
    "🧪 What-If Scenario Sandbox"
])

# TAB 1: Margin & Revenue Analysis
with tab1:
    col_t1_1, col_t1_2 = st.columns([3, 2])
    
    with col_t1_1:
        st.subheader("Daily Revenue & Margin Trend")
        trend_df = con.execute(f"""
            SELECT 
                dd.full_date,
                SUM(f.net_revenue) AS net_revenue,
                SUM(f.total_cogs) AS total_cogs,
                SUM(f.total_allocated_shipping_cost) AS shipping_cost,
                SUM(f.gross_margin_amount) AS gross_margin,
                ROUND((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 2) AS margin_pct
            {filter_query}
            GROUP BY dd.full_date
            ORDER BY dd.full_date
        """).df()
        
        if not trend_df.empty:
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=trend_df['full_date'], y=trend_df['net_revenue'], name='Net Revenue', line=dict(color='#2563EB', width=2)))
            fig_trend.add_trace(go.Scatter(x=trend_df['full_date'], y=trend_df['gross_margin'], name='Gross Margin', fill='tozeroy', line=dict(color='#10B981', width=2)))
            fig_trend.add_trace(go.Scatter(x=trend_df['full_date'], y=trend_df['shipping_cost'], name='Shipping Cost', line=dict(color='#F59E0B', width=1.5, dash='dot')))
            fig_trend.update_layout(height=380, margin=dict(l=20, r=20, t=30, b=20), hovermode="x unified", legend=dict(orientation="h", y=1.1, x=0))
            st.plotly_chart(fig_trend, use_container_width=True)

    with col_t1_2:
        st.subheader("Cost & Margin Waterfall Breakdown")
        if not kpi_df.empty:
            fig_waterfall = go.Figure(go.Waterfall(
                name="Margin Flow",
                orientation="v",
                measure=["relative", "relative", "relative", "relative", "total"],
                x=["Gross Sales", "Discounts", "COGS (Cost)", "Shipping Cost", "Net Margin"],
                textposition="outside",
                text=[f"${k['gross_rev']/1e3:.1f}k", f"-${(k['gross_rev']-k['net_rev'])/1e3:.1f}k", f"-${k['total_cogs']/1e3:.1f}k", f"-${k['total_shipping']/1e3:.1f}k", f"${k['gross_margin']/1e3:.1f}k"],
                y=[k['gross_rev'], -(k['gross_rev'] - k['net_rev']), -k['total_cogs'], -k['total_shipping'], k['gross_margin']],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "#EF4444"}},
                increasing={"marker": {"color": "#2563EB"}},
                totals={"marker": {"color": "#10B981"}}
            ))
            fig_waterfall.update_layout(height=380, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_waterfall, use_container_width=True)

    col_cat1, col_cat2 = st.columns(2)
    with col_cat1:
        st.subheader("Category Profitability Matrix")
        cat_df = con.execute(f"""
            SELECT 
                dp.category,
                SUM(f.net_revenue) AS net_revenue,
                SUM(f.total_cogs) AS total_cogs,
                SUM(f.total_allocated_shipping_cost) AS shipping_cost,
                SUM(f.gross_margin_amount) AS gross_margin,
                ROUND((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 2) AS margin_pct
            {filter_query}
            GROUP BY dp.category
            ORDER BY gross_margin DESC
        """).df()
        if not cat_df.empty:
            fig_cat = px.bar(cat_df, x='category', y='gross_margin', color='margin_pct', color_continuous_scale='Blues',
                             labels={'gross_margin': 'Gross Margin ($)', 'margin_pct': 'Margin %'}, text_auto='.2s')
            fig_cat.update_layout(height=340, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_cat, use_container_width=True)

    with col_cat2:
        st.subheader("Top 10 High Margin SKUs")
        top_sku = con.execute(f"""
            SELECT 
                dp.product_name,
                dp.category,
                SUM(f.total_units_sold) AS units_sold,
                ROUND(SUM(f.gross_margin_amount), 2) AS total_profit,
                ROUND((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 1) AS margin_pct
            {filter_query}
            GROUP BY dp.product_name, dp.category
            ORDER BY total_profit DESC
            LIMIT 10
        """).df()
        st.dataframe(top_sku, use_container_width=True, height=340)

# TAB 2: Warehouse Fulfillment
with tab2:
    st.subheader("Warehouse Dispatch Efficiency & Latency")
    c_wh1, c_wh2 = st.columns(2)
    
    with c_wh1:
        wh_summary = con.execute(f"""
            SELECT 
                dw.facility_name,
                dw.region,
                dw.capacity_tier,
                dw.automation_level,
                SUM(f.total_orders_count) AS total_orders,
                ROUND(AVG(f.avg_dispatch_latency_hours), 1) AS avg_dispatch_hrs,
                SUM(f.total_delayed_dispatches) AS delayed_dispatches,
                ROUND(((SUM(f.total_line_items_count) - SUM(f.total_delayed_dispatches)) * 100.0) / NULLIF(SUM(f.total_line_items_count), 0), 1) AS same_day_rate_pct
            {filter_query}
            GROUP BY dw.facility_name, dw.region, dw.capacity_tier, dw.automation_level
            ORDER BY avg_dispatch_hrs ASC
        """).df()
        
        fig_wh = px.bar(wh_summary, x='facility_name', y='avg_dispatch_hrs', color='automation_level',
                        labels={'facility_name': 'Warehouse', 'avg_dispatch_hrs': 'Avg Dispatch Latency (Hours)'},
                        title="Average Dispatch Latency by Facility & Automation Level")
        fig_wh.add_hline(y=24.0, line_dash="dash", line_color="red", annotation_text="24h SLA Threshold")
        fig_wh.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=80), xaxis_tickangle=-30)
        st.plotly_chart(fig_wh, use_container_width=True)

    with c_wh2:
        st.write("#### Warehouse Performance Scorecard")
        st.dataframe(wh_summary, use_container_width=True, height=380)

# TAB 3: Carrier Logistics & SLA
with tab3:
    st.subheader("Logistics Carrier SLA Compliance & Freight Cost Analysis")
    c_cr1, c_cr2 = st.columns(2)
    
    with c_cr1:
        cr_df = con.execute(f"""
            SELECT 
                dc.carrier_name,
                dc.service_level,
                dc.sla_contract_days,
                SUM(f.total_orders_count) AS total_shipments,
                ROUND(((SUM(f.total_line_items_count) - SUM(f.total_delayed_shipments)) * 100.0) / NULLIF(SUM(f.total_line_items_count), 0), 1) AS sla_on_time_pct,
                ROUND(AVG(f.avg_transit_time_days), 2) AS actual_transit_days,
                ROUND(AVG(f.avg_delivery_delay_days), 2) AS avg_delay_days,
                ROUND(SUM(f.total_allocated_shipping_cost) / NULLIF(SUM(f.total_units_sold), 0), 2) AS freight_cost_per_unit
            {filter_query}
            GROUP BY dc.carrier_name, dc.service_level, dc.sla_contract_days
            ORDER BY sla_on_time_pct DESC
        """).df()
        
        fig_cr = px.scatter(cr_df, x='actual_transit_days', y='sla_on_time_pct', size='total_shipments', color='carrier_name',
                            hover_data=['freight_cost_per_unit', 'service_level'],
                            labels={'actual_transit_days': 'Actual Avg Transit (Days)', 'sla_on_time_pct': 'SLA Compliance (%)'},
                            title="Carrier Transit Speed vs SLA Compliance Rate")
        fig_cr.add_hline(y=90.0, line_dash="dash", line_color="green", annotation_text="Target 90% SLA")
        fig_cr.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_cr, use_container_width=True)

    with c_cr2:
        st.write("#### Carrier SLA Performance Table")
        st.dataframe(cr_df, use_container_width=True, height=380)

# TAB 4: SQL Workbench
with tab4:
    st.subheader("Interactive DuckDB SQL Workbench")
    st.write("Query the Dimensional Data Mart directly in real-time:")
    
    preset_queries = {
        "1. Executive Monthly Summary": "SELECT * FROM vw_executive_monthly_margin_summary LIMIT 12;",
        "2. Carrier SLA Scorecard": "SELECT * FROM vw_carrier_performance_scorecard;",
        "3. Warehouse Dispatch Efficiency": "SELECT * FROM vw_warehouse_dispatch_efficiency;",
        "4. Product Category Profitability": "SELECT * FROM vw_product_category_profitability;",
        "5. Top Delayed Shipments & Margin Impact": """
            SELECT 
                dp.product_name,
                dw.facility_name,
                dc.carrier_name,
                f.dispatch_latency_hours,
                f.transit_time_days,
                f.delivery_delay_days,
                f.gross_margin_amount
            FROM fact_order_fulfillment f
            JOIN dim_product dp ON f.product_key = dp.product_key
            JOIN dim_warehouse dw ON f.warehouse_key = dw.warehouse_key
            JOIN dim_carrier dc ON f.carrier_key = dc.carrier_key
            WHERE f.is_delayed_delivery = 1
            ORDER BY f.delivery_delay_days DESC
            LIMIT 20;
        """
    }
    
    selected_preset = st.selectbox("Choose a Query Template:", options=list(preset_queries.keys()))
    user_sql = st.text_area("SQL Editor", value=preset_queries[selected_preset], height=160)
    
    if st.button("▶️ Execute Query", type="primary"):
        try:
            res_df = con.execute(user_sql).df()
            st.success(f"Returned {len(res_df):,} rows.")
            st.dataframe(res_df, use_container_width=True)
            csv = res_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results as CSV", data=csv, file_name="query_results.csv", mime="text/csv")
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# TAB 5: What-If Sandbox
with tab5:
    st.subheader("What-If Supply Chain & Margin Simulation Sandbox")
    st.write("Simulate the bottom-line financial and operational impact of logistics and operational changes:")
    
    sb_col1, sb_col2, sb_col3 = st.columns(3)
    with sb_col1:
        shipping_tariff_delta = st.slider("Carrier Tariff Rate Adjustment (%)", min_value=-30, max_value=50, value=0, step=5)
    with sb_col2:
        dispatch_opt_hrs = st.slider("Warehouse Dispatch Latency Reduction (Hours)", min_value=0, max_value=12, value=0, step=1)
    with sb_col3:
        price_adj_pct = st.slider("Product Price / Markup Adjustment (%)", min_value=-20, max_value=30, value=0, step=2)
        
    sim_query = f"""
        SELECT 
            SUM(f.net_revenue * (1.0 + ({price_adj_pct} / 100.0))) AS sim_revenue,
            SUM(f.total_cogs) AS sim_cogs,
            SUM(f.total_allocated_shipping_cost * (1.0 + ({shipping_tariff_delta} / 100.0))) AS sim_shipping,
            SUM(
                (f.net_revenue * (1.0 + ({price_adj_pct} / 100.0))) - 
                f.total_cogs - 
                (f.total_allocated_shipping_cost * (1.0 + ({shipping_tariff_delta} / 100.0)))
            ) AS sim_gross_margin
        {filter_query}
    """
    sim_res = con.execute(sim_query).df().iloc[0]
    
    base_margin = kpi_df.iloc[0]['gross_margin'] if not kpi_df.empty else 0
    margin_diff = sim_res['sim_gross_margin'] - base_margin
    margin_diff_pct = (margin_diff / base_margin * 100.0) if base_margin != 0 else 0
    
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Simulated Net Revenue", f"${sim_res['sim_revenue']:,.0f}", f"{price_adj_pct:+d}% Price Change")
    sc2.metric("Simulated Shipping Spend", f"${sim_res['sim_shipping']:,.0f}", f"{shipping_tariff_delta:+d}% Tariff Change")
    sc3.metric("Simulated Gross Margin", f"${sim_res['sim_gross_margin']:,.0f}", f"{margin_diff:+,.0f} ({margin_diff_pct:+.1f}%)")
