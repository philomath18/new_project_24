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

# Reshape data for heatmap
df_melted = df.melt(id_vars='coin', var_name='Multiplier', value_name='Reached')

# Replace multiplier names to ensure they are in the correct order
df_melted['Multiplier'] = pd.Categorical(df_melted['Multiplier'], categories=['3x', '5x', '10x', '20x'], ordered=True)

# Adjust 'Reached' values to match the multipliers for the color scale
df_melted['Reached'] = df_melted['Multiplier'].str.extract(r'(\d+)').astype(int)['Multiplier'] * df_melted['Reached']

# Create the heatmap
fig = px.imshow(
    df.pivot(index='coin', columns='Multiplier', values='Reached'),
    labels={'x': 'Multiplier', 'y': 'Coin', 'color': 'Multiplier'},
    title="Heatmap of Multiplier Achievement by Coin",
    color_continuous_scale=px.colors.sequential.Viridis,
)

# Update layout for larger width and custom color legend
fig.update_layout(
    xaxis=dict(title="Multiplier", tickmode='linear', automargin=True),
    yaxis=dict(title="Coin", automargin=True),
    height=1000,
    width=1000,  # Increase width for better visibility
    coloraxis_colorbar=dict(
        title="Multiplier",
        tickvals=[3, 5, 10, 20],  # Only show relevant values in the color bar
        ticktext=['3x', '5x', '10x', '20x'],
    )
)

# Show the updated heatmap
fig.show()


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
