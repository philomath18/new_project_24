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
fig_bubble.update_traces(hovertemplate="<b>%{text}</b><br>Value: %{y:.0f} ₹<br>Coin: %{x}")

# Plotting the bar chart
st.subheader("Percent Gain by Coin")
fig_bar = px.bar(
    df, 
    x='coin', 
    y='percent_gain', 
    color='percent_gain', 
    title="Percent Gain by Coin",
    labels={"percent_gain": "Percent Gain (%)"},
    color_continuous_scale='RdYlGn'  # Set continuous color scale from red to green
)

# Customize the color scale range to center around 0 for better visual effect
fig_bar.update_traces(
    marker=dict(
        color=df['percent_gain'],  # Set the color based on percent_gain
        colorbar=dict(
            title="Percent Gain",
            tickvals=[-10, -5, 0, 5, 10, 15, 20],  # Custom ticks for the color scale
        )
    )
)

# Display the chart
fig_scatter.update_traces(hovertemplate="<b>%{text}</b><br>Percent Gain: %{x:.0f}%<br>Value: %{y:.0f} ₹")
st.plotly_chart(fig_bar, use_container_width=True)

##### Multiplier Chart
# Heatmap for Coin Multipliers
# Heatmap for Coin Multipliers
st.subheader("Multiplier Achievement Heatmap")

# Reshape the DataFrame for heatmap input
df_heatmap = df[['coin', '3x', '5x', '10x', '20x']].melt(id_vars='coin', var_name='Multiplier', value_name='Reached')

# Replace 'Reached' with numeric values (0 for not reached, 1 for reached)
df_heatmap['Reached'] = df_heatmap['Reached'].apply(lambda x: 1 if x == 1 else 0)

# Ensure the 'Multiplier' column has the correct order (3x, 5x, 10x, 20x)
multiplier_order = ['3x', '5x', '10x', '20x']
df_heatmap['Multiplier'] = pd.Categorical(df_heatmap['Multiplier'], categories=multiplier_order, ordered=True)

# Create the pivot table for the heatmap
pivot_df = df_heatmap.pivot(index='coin', columns='Multiplier', values='Reached')

# Create heatmap with a discrete color scale (using only 2 colors for 0 and 1)
fig_heatmap = px.imshow(
    pivot_df,
    labels={'x': 'Multiplier', 'y': 'Coin', 'color': 'Reached'},
    title="Heatmap of Multiplier Achievement by Coin",
    color_continuous_scale=['white', 'green'],  # Discrete colors for 0 and 1
    height=1200  # Fit all coins
)

# Set the color scale to be discrete with two values
fig_heatmap.update_traces(
    colorscale=[[0, 'white'], [1, 'green']],  # Red for 0 (Not Reached), Green for 1 (Reached)
    colorbar=dict(tickvals=[0, 1], ticktext=["Not Reached", "Reached"])  # Labels for 0 and 1
)

# Update the x-axis to ensure the correct order of multipliers
fig_heatmap.update_layout(
    xaxis=dict(
        title="Multiplier",
        categoryorder='array',  # Ensuring the x-axis is ordered
        categoryarray=multiplier_order  # Explicit order for x-axis categories
    ),
    yaxis=dict(
        title="Coin"
    )
)

# Show the heatmap
st.plotly_chart(fig_heatmap, use_container_width=True)

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
fig_scatter.update_traces(hovertemplate="<b>%{text}</b><br>Percent Gain: %{x:.0f}%<br>Value: %{y:.0f} ₹")
st.plotly_chart(fig_scatter, use_container_width=True)


###

import plotly.express as px
import plotly.graph_objects as go


# Reshape the data for the lollipop chart (melt the multipliers)
df_stack = df[['coin', '3x', '5x', '10x', '20x']].melt(id_vars='coin', var_name='Multiplier', value_name='Reached')

# Filter only rows where multiplier was reached (Reached == 1)
df_stack_filtered = df_stack[df_stack['Reached'] == 1]

# Create the lollipop chart
fig_lollipop = go.Figure()

# Add scatter (markers for the lollipops)
fig_lollipop.add_trace(
    go.Scatter(
        x=df_stack_filtered['coin'],
        y=df_stack_filtered['Multiplier'],
        mode='markers',
        marker=dict(size=12, color='blue', line=dict(width=2, color='black')),
        name='Multiplier Reached'
    )
)

# Add lines (sticks for the lollipops)
fig_lollipop.add_trace(
    go.Scatter(
        x=df_stack_filtered['coin'],
        y=df_stack_filtered['Multiplier'],
        mode='lines',
        line=dict(width=3, color='blue'),
        name='Multiplier Line'
    )
)

# Customize layout
fig_lollipop.update_layout(
    title="Lollipop Chart for Multipliers by Coin",
    xaxis=dict(title="Coin", tickangle=45),
    yaxis=dict(title="Multiplier", tickvals=['3x', '5x', '10x', '20x'], ticktext=['3x', '5x', '10x', '20x']),
    showlegend=False,
    height=600,
    margin=dict(l=50, r=50, t=50, b=50),
)

# Display the lollipop chart
st.plotly_chart(fig_lollipop, use_container_width=True)
