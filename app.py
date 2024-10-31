import streamlit as st
import numpy as np
import pandas as pd

# Custom CSS for styling (if needed)
style = """
  <style>
      .metric-container {
          text-align: center;
      }
  </style>
"""
st.markdown(style, unsafe_allow_html=True)

@st.cache  # Use caching to speed up data load
def load_data():
    file = "bakerysales.csv"
    df = pd.read_csv(file)
    
    # Rename columns for clarity
    df.rename(columns={
        "Unnamed: 0": "id", 
        "article": "product",
        "Quantity": "quantity"
    }, inplace=True)
    
    # Clean unit_price data
    df.unit_price = df.unit_price.str.replace(",", ".").str.replace("€", "").str.strip().astype("float")
    
    # Calculate sales
    df["sales"] = df.quantity * df.unit_price
    
    # Drop rows with zero sales
    df.drop(df[df.sales == 0].index, inplace=True)

    # Convert date column to datetime format
    df["date"] = pd.to_datetime(df.date)
    
    return df

# Load the dataset
df = load_data()

# App title
st.title("Bakery Sales App")
st.write("Analyze bakery sales data and gain insights.")

# Sidebar Filters
st.sidebar.header("Filter Options")
products = df["product"].unique()
selected_product = st.sidebar.multiselect("Choose Product", products, default=[products[0], products[2]])

# Filter data based on user selection
filtered_table = df[df["product"].isin(selected_product)]

# Display Metrics
def display_metrics(dataframe):
    total_sales = dataframe["sales"].sum() if not dataframe.empty else 0
    total_qty = dataframe["quantity"].sum() if not dataframe.empty else 0
    total_transaction = dataframe["id"].count() if not dataframe.empty else 0

    st.subheader("Sales Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Number of transactions", total_transaction)
    col2.metric("Total Quantity Sold", total_qty)
    col3.metric("Total Sales (€)", f"{total_sales:.2f}")

# Call the metrics display function
display_metrics(filtered_table)

# Display filtered table
if not filtered_table.empty:
    st.dataframe(filtered_table[["date", "product", "quantity", "unit_price", "sales"]])
    
    # Visualize total sales by selected products
    st.write("## Total Sales of Selected Products")
    total_sales_by_product = filtered_table.groupby(['product'])["sales"].sum().sort_values(ascending=True)
    st.bar_chart(total_sales_by_product)
else:
    st.warning("No data available for the selected product(s). Please adjust your filters.")

# Add a footer and user guidance
st.sidebar.write("### About this App")
st.sidebar.info("This app allows you to analyze bakery sales, visualize total sales by product, and understand your bakery's performance.")
