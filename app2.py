!pip install streamlit
import pandas as pd
import streamlit as st

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
                                           # ^^^^^^^^ Force comma as delimiter
     
    try:                                      #          ^ handle inconsistent lines with a warning
      df = df.drop('Unnamed: 0', axis = 1)
    except:
      df = df
    
    return df

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
