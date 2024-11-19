import pandas as pd
import streamlit as st

# Define a function to fetch and load the latest data
@st.cache(ttl=3600)  # Cache data for an hour
def load_data():
    # Replace YOUR_FILE_ID with the actual Google Drive file ID
    file_url = "https://drive.google.com/file/d/1W3wyUzLnEuItWNS5Jjg6E5GUdnNpVdIT"  # Replace YOUR_FILE_ID
    return pd.read_csv(file_url)

# Fetch the latest data
df = load_data()

# Streamlit app layout
st.title("Crypto Portfolio Tracker")
st.write("This dashboard shows your crypto portfolio performance.")

# Display the DataFrame
st.subheader("Portfolio Data")
st.dataframe(df)

# Bubble chart visualization for portfolio analysis
st.subheader("Portfolio Overview - Bubble Chart")
import plotly.express as px

# Bubble chart (adjust columns as per your DataFrame structure)
fig = px.scatter(
    df, 
    x='prices', 
    y='qty', 
    size='value', 
    hover_name='coin', 
    title="Bubble Chart of Portfolio"
)
st.plotly_chart(fig)

#color='Multiplier (X)'