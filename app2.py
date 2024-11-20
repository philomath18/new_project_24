import pandas as pd
import requests
import io

# Function to load data
def load_data():
    file_id = "1cwZLxlaob5P40ijaGf4U3Rqc4ERwVYI6"
    file_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(file_url)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
    try:
        df = df.drop('Unnamed: 0', axis=1)
    except:
        pass
    return df

# Function to format INR values correctly
def format_inr(value):
    """Format the value in INR style with commas at appropriate places."""
    if pd.isna(value):  # Handle NaN values
        return "₹0"
    
    # Convert value to integer (in case it's a float)
    value = int(value)
    
    # Format value using the appropriate rule: commas after 3 digits, then every 2 digits
    return "₹{:,.0f}".format(value).replace(",", "X").replace("X", ",", 1)

# Load data
df = load_data()

# Create a new column for INR-formatted values
df['value_inr'] = df['value'].apply(format_inr)

# Calculate the total portfolio value
total_value = df['value'].sum()
total_value_inr = format_inr(total_value)

# Streamlit app layout
import streamlit as st
st.title("Crypto Portfolio Tracker")
st.markdown(f"<h3 style='text-align: right; font-weight: bold;'>Total Portfolio Value: {total_value_inr}</h3>", unsafe_allow_html=True)
st.write("This dashboard shows your crypto portfolio performance.")

# Display the data
st.subheader("Portfolio Data")
st.dataframe(df)

# Bubble Chart
import plotly.express as px
st.subheader("Portfolio Overview - Bubble Chart")
fig_bubble = px.scatter(
    df, 
    x='coin', 
    y='value', 
    size='value', 
    color='coin', 
    hover_name='coin', 
    text='coin', 
    title="Bubble Chart of Portfolio",
    labels={"value": "Value (₹)"}  # Ensure the value is labeled correctly
)
fig_bubble.update_traces(marker=dict(sizemode='diameter', line_width=2, opacity=0.6), textfont=dict(color='white', size=14))
fig_bubble.update_traces(hovertemplate="<b>%{text}</b><br>Value: %{y:.0f} ₹<br>Coin: %{x}")

st.plotly_chart(fig_bubble, use_container_width=True)
