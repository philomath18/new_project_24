import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

# Define a function to fetch and load the latest data
@st.cache(ttl=3600)
def load_data():
    file_id = "1W3wyUzLnEuItWNS5Jjg6E5GUdnNpVdIT"
    file_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(file_url)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
    try:
        df = df.drop('Unnamed: 0', axis=1)
    except:
        pass
    return df
print('Hi')
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

# Pie Chart for Multiplier Flags
st.subheader("Multiplier Milestone Distribution")
multipliers = ['3x', '5x', '10x', '20x']
multiplier_counts = {multiplier: df[multiplier].sum() for multiplier in multipliers}
fig_pie = px.pie(
    names=list(multiplier_counts.keys()), 
    values=list(multiplier_counts.values()), 
    title="Distribution of Multiplier Milestones",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig_pie)

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
