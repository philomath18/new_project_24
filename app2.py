import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

# Function to fetch and load the latest data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    file_id = "YOUR_GOOGLE_DRIVE_FILE_ID"  # Replace with your file ID
    file_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(file_url)
    response.raise_for_status()  
    df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
    
    # Add time simulation column for animation (e.g., months or synthetic time)
    df['time'] = pd.Series(range(len(df))) % 12  # Cycles through 12 time points
    return df

# Load data
df = load_data()

# Calculate the total portfolio value
total_value = df['value'].sum()
total_value_inr = f"₹{total_value:,.2f}"

# Streamlit app layout
st.title("Dynamic Crypto Portfolio Tracker")
st.markdown(f"<h3 style='text-align: right;'>Total Portfolio Value: {total_value_inr}</h3>", unsafe_allow_html=True)

# Bubble chart with animation
st.subheader("Animated Portfolio Bubble Chart")
fig = px.scatter(
    df,
    x='coin',
    y='value',
    size='value',
    color='coin',
    animation_frame='time',  # Add animation based on 'time'
    hover_name='coin',
    text='coin',
    title="Portfolio Bubble Chart with Animation",
    size_max=100,  # Control the maximum bubble size
)

# Enhance layout for better visibility
fig.update_traces(marker=dict(sizemode='diameter', opacity=0.7))
fig.update_layout(
    xaxis=dict(title="Coin", tickangle=-45),  # Rotate X-axis labels
    yaxis=dict(title="Value (INR)", showgrid=False),
    hoverlabel=dict(font_size=14, font_color="white"),
    title_font_size=20
)

# Display the chart
st.plotly_chart(fig)
