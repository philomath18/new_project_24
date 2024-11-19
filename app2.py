import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

# Define a function to fetch and load the latest data
@st.cache(ttl=3600)  # Cache data for an hour
def load_data():
    # Replace YOUR_FILE_ID with the actual Google Drive file ID
    file_id = "1W3wyUzLnEuItWNS5Jjg6E5GUdnNpVdIT"
    file_url = f"https://drive.google.com/uc?id={file_id}"
    
    # Download the file content
    response = requests.get(file_url)
    response.raise_for_status()  # Raise an exception for bad responses
    
    # Read the CSV data using io.StringIO to handle potential encoding issues
    df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
    
    try:
        df = df.drop('Unnamed: 0', axis=1)  # Drop the extra index column if present
    except:
        df = df
    
    return df

# Fetch the latest data
df = load_data()

# Create a new column for INR-formatted values (for display purposes)
df['value_inr'] = df['value'].apply(lambda x: "₹{:,.2f}".format(x))

# Calculate the total portfolio value (sum of the original 'value' column, not the formatted one)
total_value = df['value'].sum()

# Format the total portfolio value in INR
total_value_inr = "₹{:,.2f}".format(total_value)

# Streamlit app layout
st.title("Crypto Portfolio Tracker")
st.write("This dashboard shows your crypto portfolio performance.")

# Display the total portfolio value at the top right in bold
st.markdown(f"<h3 style='text-align: right; font-weight: bold;'>Total Portfolio Value: {total_value_inr}</h3>", unsafe_allow_html=True)

# Display the DataFrame
st.subheader("Portfolio Data")
st.dataframe(df)

# Bubble chart visualization for portfolio analysis
st.subheader("Portfolio Overview - Bubble Chart")

# Bubble chart (adjust columns as per your DataFrame structure)
fig = px.scatter(
    df, 
    x='coin',  # Use the coin names on the X-axis
    y='value',  # Y-axis should be the value of the coin (numeric for charting)
    size='value',  # Bubble size should be proportional to the value
    color='coin',  # Color by coin type (or any other column, like 'category')
    hover_name='coin',  # Show the coin name when hovering
    text='coin',  # Display coin names inside the bubbles
    title="Bubble Chart of Portfolio"
)

# Customize the layout of the bubble chart
fig.update_traces(marker=dict(sizemode='diameter', line_width=2, opacity=0.6))

# Show the plot in Streamlit
st.plotly_chart(fig)
