import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db_connector import connect_to_db


def fetch_data_as_dataframe():
    """
    Fetches the joined customer and bill data from the database
    and returns it as a clean pandas DataFrame.
    """
    db_conn = connect_to_db()
    if not db_conn:
        return pd.DataFrame()  # Return empty DataFrame on connection failure

    # SQL query to get all relevant data in one go
    query = """
    SELECT 
        c.name, c.address, c.email,
        b.meterno, b.billdate, b.consumed, 
        b.amount, b.paid
    FROM bill b
    JOIN customer c ON b.meterno = c.meterno
    """

    try:
        df = pd.read_sql(query, db_conn)
        # Convert 'billdate' to a proper datetime format for analysis
        df['billdate'] = pd.to_datetime(df['billdate'])
        print("Data successfully fetched and loaded into DataFrame.")
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
    finally:
        if db_conn.is_connected():
            db_conn.close()


def plot_monthly_consumption(df):
    """
    Takes a DataFrame and returns a matplotlib figure of
    total electricity consumption per month.
    """
    # Set the style for the plot
    sns.set_style("whitegrid")

    # Group data by month and sum the consumption
    monthly_data = df.set_index('billdate').resample('ME')['consumed'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_data.plot(kind='line', marker='o', ax=ax, color='dodgerblue', label='Units Consumed')

    ax.set_title('Total Monthly Electricity Consumption Trend', fontsize=16)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Total Units Consumed (in kWh)', fontsize=12)
    ax.legend()
    plt.tight_layout()

    return fig


def plot_top_consumers(df, top_n=10):
    """
    Takes a DataFrame and returns a matplotlib figure of the
    top N highest consuming customers by total amount paid.
    """
    sns.set_style("whitegrid")

    top_consumers = df.groupby('name')['amount'].sum().nlargest(top_n).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    top_consumers.plot(kind='barh', ax=ax, color='skyblue')

    ax.set_title(f'Top {top_n} Consumers by Total Bill Amount', fontsize=16)
    ax.set_xlabel('Total Amount Paid (₹)', fontsize=12)
    ax.set_ylabel('Customer Name', fontsize=12)

    # Add labels to the bars
    for i, v in enumerate(top_consumers):
        ax.text(v + 50, i, f'₹{int(v)}', color='black', va='center')

    plt.tight_layout()

    return fig