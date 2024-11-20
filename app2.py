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

# Map multiplier columns to numeric values for calculation
multiplier_map = {'3x': 3, '5x': 5, '10x': 10, '20x': 20}

# Calculate the max multiplier reached for each coin
df['max_multiplier'] = df[['3x', '5x', '10x', '20x']].dot([3, 5, 10, 20])  

# Sort the DataFrame by maximum multiplier for better visualization
df_sorted = df.sort_values('max_multiplier', ascending=True)

# Create the horizontal bar chart
fig_horizontal = px.bar(
    df_sorted,  # Use the sorted DataFrame
    y='coin',  # Coins on the Y-axis
    x='max_multiplier',  # Maximum multiplier on the X-axis
    orientation='h',  # Horizontal bar chart
    title="Maximum Multiplier Reached by Each Coin",
    color='max_multiplier',  # Use a gradient color scale based on the multiplier
    color_continuous_scale=px.colors.sequential.Viridis,  # Modern gradient color palette
    labels={'coin': 'Coin', 'max_multiplier': 'Maximum Multiplier'},  # Custom axis labels
    text='max_multiplier'  # Show the multiplier as text on the bars
)

# Customize layout for better visibility
fig_horizontal.update_layout(
    xaxis=dict(title="Multiplier Value"),  # Title for X-axis
    yaxis=dict(title="Coin", automargin=True),  # Ensure coin names fit
    coloraxis_colorbar=dict(title="Multiplier"),  # Colorbar title
    height=1200,  # Dynamically increase height to fit 70 coins
    margin=dict(l=200, r=50, t=50, b=50)  # Increase left margin for long coin names
)

# Customize bar text to ensure clarity
fig_horizontal.update_traces(textposition='inside', textfont_size=12)

# Show the updated chart in Streamlit
st.plotly_chart(fig_horizontal)

###################
# Heatmap for Coin Multipliers
st.subheader("Multiplier Achievement Heatmap")

# Reshape the DataFrame for heatmap input
df_heatmap = df[['coin', '3x', '5x', '10x', '20x']].melt(id_vars='coin', var_name='Multiplier', value_name='Reached')

# Replace 'Reached' with numeric values (0 for not reached, 1 for reached)
df_heatmap['Reached'] = df_heatmap['Reached'].apply(lambda x: 1 if x == 1 else 0)

# Create heatmap
fig_heatmap = px.imshow(
    df_heatmap.pivot(index='coin', columns='Multiplier', values='Reached'),
    labels={'x': 'Multiplier', 'y': 'Coin', 'color': 'Reached'},
    color_continuous_scale='Viridis',
    title="Heatmap of Multiplier Achievement by Coin",
    height=1200  # Fit all coins
)

# Show the heatmap
st.plotly_chart(fig_heatmap)




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
