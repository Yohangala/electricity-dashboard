import streamlit as st
import pandas as pd
from analysis import fetch_data_as_dataframe, plot_monthly_consumption, plot_top_consumers

# Set the page configuration for a wider layout
st.set_page_config(layout="wide")

# App Title
st.title('⚡ Electricity Consumption Analysis Dashboard')
st.markdown("An interactive dashboard to analyze customer electricity usage and billing data.")


# --- Load Data ---
# Add a caching decorator to prevent reloading data on every interaction
@st.cache_data
def load_data():
    df = fetch_data_as_dataframe()
    return df


df = load_data()

if df.empty:
    st.error("Failed to load data. Please check the database connection and ensure data exists.")
else:
    # --- Key Performance Indicators (KPIs) ---
    st.header('Key Metrics')

    total_revenue = df['amount'].sum()
    avg_consumption = df['consumed'].mean()
    unpaid_bills_count = df[df['paid'] == 'Unpaid'].shape[0]
    total_unpaid_amount = df[df['paid'] == 'Unpaid']['amount'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹ {total_revenue:,.2f}")
    col2.metric("Avg. Consumption", f"{avg_consumption:.2f} kWh")
    col3.metric("Unpaid Bills (#)", f"{unpaid_bills_count}")
    col4.metric("Unpaid Amount", f"₹ {total_unpaid_amount:,.2f}")

    st.markdown("---")

    # --- Visualizations ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Monthly Consumption Trend')
        fig_monthly = plot_monthly_consumption(df)
        st.pyplot(fig_monthly)

    with col2:
        st.subheader('Top 10 Consumers')
        fig_top_consumers = plot_top_consumers(df)
        st.pyplot(fig_top_consumers)

    st.markdown("---")

    # --- Raw Data Explorer ---
    st.header('Data Explorer')
    st.dataframe(df)