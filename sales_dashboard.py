# Run this in Jupyter to create the FIXED dashboard file
dashboard_code = '''
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Analytics Dashboard")
st.write("Interactive dashboard for analyzing sales performance")

@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df.columns = df.columns.str.strip()
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Month'] = df['OrderDate'].dt.to_period('M').astype(str)
    df['Revenue_INR'] = pd.to_numeric(df['Revenue_INR'], errors='coerce').fillna(0)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Regions", df['Region'].unique(), default=df['Region'].unique())
products = st.sidebar.multiselect("Products", df['Product'].unique(), default=df['Product'].unique())
segments = st.sidebar.multiselect("Customer Segments", df['CustomerSegment'].unique(), default=df['CustomerSegment'].unique())

filtered_df = df[
    (df['Region'].isin(regions)) & 
    (df['Product'].isin(products)) &
    (df['CustomerSegment'].isin(segments))
]

# KPIs
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['Revenue_INR'].sum()
    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

with col2:
    total_orders = filtered_df['OrderID'].nunique()
    st.metric("Total Orders", f"{total_orders}")

with col3:
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
    st.metric("Avg Order Value", f"₹{avg_order:,.0f}")

with col4:
    total_qty = filtered_df['Quantity'].sum()
    st.metric("Quantity Sold", f"{total_qty}")

# Charts
st.header("Analytics Charts")

# Revenue by Region and Products
col1, col2 = st.columns(2)

with col1:
    region_sales = filtered_df.groupby('Region')['Revenue_INR'].sum().reset_index()
    fig1 = px.bar(region_sales, x='Region', y='Revenue_INR', title="Revenue by Region")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    product_sales = filtered_df.groupby('Product')['Revenue_INR'].sum().reset_index()
    fig2 = px.pie(product_sales, values='Revenue_INR', names='Product', title="Revenue by Product")
    st.plotly_chart(fig2, use_container_width=True)

# Monthly Trend and Customer Segments
col1, col2 = st.columns(2)

with col1:
    monthly_sales = filtered_df.groupby('Month')['Revenue_INR'].sum().reset_index()
    fig3 = px.line(monthly_sales, x='Month', y='Revenue_INR', title="Monthly Sales Trend", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    segment_sales = filtered_df.groupby('CustomerSegment')['Revenue_INR'].sum().reset_index()
    fig4 = px.bar(segment_sales, x='CustomerSegment', y='Revenue_INR', title="Revenue by Customer Segment")
    st.plotly_chart(fig4, use_container_width=True)

# Discount Analysis
fig5 = px.scatter(filtered_df, x='DiscountPct', y='Revenue_INR', color='Product', 
                 title="Discount % vs Revenue", size='Quantity')
st.plotly_chart(fig5, use_container_width=True)

# Data Table
st.header("Sales Data")
st.dataframe(filtered_df, use_container_width=True, height=300)

# Export button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name=f"filtered_sales_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Sales Analytics Dashboard")
'''

# Create the fixed Python file
with open('sales_dashboard_fixed.py', 'w') as f:
    f.write(dashboard_code)

print("✅ sales_dashboard_fixed.py created successfully!")
print("🎯 Now run this command in Command Prompt:")
print("streamlit run sales_dashboard_fixed.py")