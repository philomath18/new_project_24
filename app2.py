import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

# Define a function to fetch and load the latest data
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

##### Multiplier Chart

# Reshape data for the chart (melt the columns into long format)
df_stack = df[['coin', '3x', '5x', '10x', '20x']].melt(id_vars='coin', var_name='Multiplier', value_name='Reached')

# Filter only where multiplier is reached (Reached == 1)
df_stack_filtered = df_stack[df_stack['Reached'] == 1]

# Set order of multipliers for y-axis (3x, 5x, 10x, 20x)
multiplier_order = ['3x', '5x', '10x', '20x']

# Ensure the multiplier column has the correct order
df_stack_filtered['Multiplier'] = pd.Categorical(df_stack_filtered['Multiplier'], categories=multiplier_order, ordered=True)

# Calculate the value at the 3x multiplier (3 * initial_price * qty)
df_stack_filtered['value_at_3x'] = df_stack_filtered.apply(
    lambda row: 3 * df[df['coin'] == row['coin']]['prev_price'].values[0] * df[df['coin'] == row['coin']]['qty'].values[0] if row['Multiplier'] == '3x' else 0,
    axis=1
)

# Create the stacked bar chart with the calculated value in the center
fig_stacked = px.bar(
    df_stack_filtered,
    x='coin',
    y='Multiplier',
    color='Multiplier',
    title="Stacked Bar Chart of Multipliers by Coin",
    color_discrete_sequence=px.colors.qualitative.Set3,
    labels={'coin': 'Coin', 'Multiplier': 'Multiplier'},
    text='Multiplier'
)

# Add value_at_3x in the center of each bar for 3x multiplier
fig_stacked.update_traces(
    texttemplate='%{text}',  # Add multiplier value in the center of the bars
    textposition='inside',
    insidetextanchor='middle',
    textfont=dict(size=14, color='white', family='Arial', weight='bold')
)

# Update layout for stacked bar chart
fig_stacked.update_layout(
    xaxis=dict(
        title="Coin",
        categoryorder='array', 
        categoryarray=df['coin'].tolist()  # Ensuring the coin order is preserved
    ),
    yaxis=dict(
        title="Multiplier",
        tickvals=[3, 5, 10, 20],  # Set the tick values as the actual multipliers
        ticktext=['3x', '5x', '10x', '20x']
    ),
    height=700, 
    margin=dict(l=50, r=50, t=50, b=50),  
)

# Show the stacked chart in Streamlit
st.plotly_chart(fig_stacked)

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
