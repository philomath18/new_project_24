import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

# Define a function to fetch and load the latest data
#@st.cache(ttl=3600)
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

# Load data
df = load_data()

# Create a new column for INR-formatted values
df['value_inr'] = df['value'].apply(lambda x: "₹{:,.2f}".format(x))

# Calculate the total portfolio value
total_value = df['value'].sum()
total_value_inr = "₹{:,.2f}".format(total_value)

# Streamlit app layout
st.title("Crypto Portfolio Tracker")
st.markdown(f"<h3 style='text-align: right; font-weight: bold;'>Total Portfolio Value: {total_value_inr}</h3>", unsafe_allow_html=True)
st.write("This dashboard shows your crypto portfolio performance.")

# Display the data
st.subheader("Portfolio Data")
st.dataframe(df)

# Bubble Chart
st.subheader("Portfolio Overview - Bubble Chart")
fig_bubble = px.scatter(
    df, 
    x='coin', 
    y='value', 
    size='value', 
    color='coin', 
    hover_name='coin', 
    text='coin', 
    title="Bubble Chart of Portfolio"
)
fig_bubble.update_traces(marker=dict(sizemode='diameter', line_width=2, opacity=0.6), textfont=dict(color='white', size=14))
st.plotly_chart(fig_bubble)

# Bar Chart for Percent Gain
st.subheader("Percent Gain by Coin")
fig_bar = px.bar(
    df, 
    x='coin', 
    y='percent_gain', 
    color='percent_gain', 
    title="Percent Gain by Coin",
    labels={"percent_gain": "Percent Gain (%)"}
)
fig_bar.update_layout(coloraxis_colorbar=dict(title="Percent Gain"))
st.plotly_chart(fig_bar)

# Horizontal Bar Chart for Multiplier Progression
st.subheader("Coins vs. Maximum Multiplier Reached")

# Find the maximum multiplier achieved for each coin
multiplier_map = {'3x': 3, '5x': 5, '10x': 10, '20x': 20}  # Map column names to numeric values
df['max_multiplier'] = df[['3x', '5x', '10x', '20x']].dot([3, 5, 10, 20])  # Calculate max multiplier per coin

# Create the horizontal bar chart
fig_horizontal = px.bar(
    df.sort_values('max_multiplier', ascending=True),  # Sort coins by max multiplier
    y='coin',  # Coins on Y-axis
    x='max_multiplier',  # Multiplier values on X-axis
    orientation='h',  # Horizontal bars
    title="Maximum Multiplier Reached by Each Coin",
    color='max_multiplier',  # Use a color gradient based on max multiplier
    color_continuous_scale=px.colors.sequential.Viridis,  # Modern color palette
    labels={'coin': 'Coin', 'max_multiplier': 'Maximum Multiplier'},
    text='max_multiplier'  # Display max multiplier as text on the bars
)

# Customize layout for clarity
fig_horizontal.update_layout(
    xaxis=dict(title="Multiplier Value"),  # X-axis title
    yaxis=dict(title="Coin", automargin=True),  # Y-axis title
    coloraxis_colorbar=dict(title="Multiplier"),  # Colorbar title
    height=800  # Adjust height for better readability
)

# Show the chart
st.plotly_chart(fig_horizontal)

# Scatter Plot: Percent Gain vs Value
st.subheader("Percent Gain vs Value")
fig_scatter = px.scatter(
    df, 
    x='percent_gain', 
    y='value', 
    size='value', 
    color='coin', 
    hover_name='coin', 
    title="Percent Gain vs Portfolio Value",
    labels={"percent_gain": "Percent Gain (%)", "value": "Value (₹)"}
)
st.plotly_chart(fig_scatter)
