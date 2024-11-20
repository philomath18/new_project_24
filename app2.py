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

import plotly.express as px
import pandas as pd

# Sample DataFrame (replace with your actual data)
data = {
    'coin': ['BTC', 'ETH', 'XRP', 'LTC', 'SOL'],
    '3x': [1, 1, 0, 1, 0],
    '5x': [1, 0, 1, 0, 1],
    '10x': [0, 1, 0, 1, 0],
    '20x': [1, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

# Reshape data for stacking (melt the dataframe)
df_stack = df[['coin', '3x', '5x', '10x', '20x']].melt(id_vars='coin', var_name='Multiplier', value_name='Reached')

# Only keep the rows where the multiplier is reached (i.e., where the value is 1)
df_stack = df_stack[df_stack['Reached'] == 1]

# Define the order of multipliers
multiplier_order = ['3x', '5x', '10x', '20x']

# Create stacked bar chart
fig_stacked = px.bar(
    df_stack,
    x='coin',
    y='Multiplier',
    color='Multiplier',
    title="Stacked Bar Chart of Multipliers by Coin",
    color_discrete_sequence=px.colors.qualitative.Set3,
    labels={'coin': 'Coin', 'Multiplier': 'Multiplier'},
    text='Multiplier'
)

# Update the layout for the color scale and axis
fig_stacked.update_traces(marker=dict(line=dict(width=1, color='white')))  # Optional: border color for bars
fig_stacked.update_layout(
    coloraxis=dict(
        colorscale='Viridis',  # Choose an appropriate color scale
        colorbar=dict(title="Multiplier Value", tickvals=[3, 5, 10, 20], ticktext=['3x', '5x', '10x', '20x'])
    ),
    xaxis=dict(
        title="Coin",
        categoryorder='array',
        categoryarray=df['coin'].tolist()  # Ensure coins are ordered based on input data
    ),
    yaxis=dict(
        title="Multiplier",
        tickvals=[3, 5, 10, 20],  # Make sure multiplier values are shown as ticks
        ticktext=['3x', '5x', '10x', '20x']
    ),
    height=700,  # Adjust based on visualization
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
)

# Show the chart
st.plotly_chart(fig_stacked)


###############


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
