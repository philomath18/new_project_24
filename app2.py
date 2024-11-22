import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

# Load data function
def load_data():
    github_repo_url = "https://raw.githubusercontent.com/philomath18/new_project_24/refs/heads/main/crypto_portfolio_updated.csv"
    response = requests.get(github_repo_url)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
    df = df.drop('Unnamed: 0', axis=1, errors='ignore')
    return df

# Load the dataset
df = load_data()

# Function to update portfolio based on user input
# Function to update portfolio based on user input
def update_portfolio(df):
    # We'll track the number of iterations to make each widget key unique
    iteration = 0
    
    while True:
        # Coin Name - Use a unique key for the selectbox based on iteration
        coin_options = df['coin'].unique()
        selected_coin = st.selectbox(
            'Select Coin', 
            coin_options,
            key=f"select_coin_{iteration}"  # Unique key for each iteration
        )

        # Current Quantity (make sure it’s an integer or float)
        current_qty = df.loc[df['coin'] == selected_coin, 'qty'].values[0]

        # Ensure that current_qty is a number (int or float), in case it’s NaN or another type
        if pd.isna(current_qty):
            current_qty = 0  # Set to 0 if it's NaN
        else:
            current_qty = float(current_qty)  # Ensure it's a float

        # Updated Quantity (ensure it's an int or float) - Unique key for each iteration
        updated_qty = st.number_input(
            f'Enter updated quantity for {selected_coin}', 
            value=current_qty, 
            key=f"number_input_qty_{iteration}"  # Unique key for each iteration
        )

        # Update the quantity in the dataframe
        df.loc[df['coin'] == selected_coin, 'qty'] = updated_qty

        # Recalculate values based on updated quantity
        df['value'] = df['prices'] * df['qty']
        df['value_inr'] = df['value'] * 90

        # Ask if the user wants to update another coin
        update_another = st.radio(
            'Do you have updates on any other coin?', 
            ['No', 'Yes'],
            key=f"update_another_{iteration}"  # Unique key for each iteration
        )

        if update_another == 'No':
            break
        else:
            iteration += 1  # Increment the iteration to generate unique keys for the next loop
            continue

    return df



# Update portfolio based on user inputs

df.loc[df['coin'] == 'USDT', 'prev_price'] = 1
df.loc[df['coin'] == 'USDT', 'percent_gain'] = 0


df = update_portfolio(df)

# Recalculate portfolio metrics
df['value_initial'] = df['prev_price'] * df['qty'] * 90
total_initial_value = df['value_initial'].sum()

# Calculate the total portfolio value
df['value'] = df['value'].astype(int)
df['value_inr'] = df['value'] * 90
df['value_inr'] = df['value_inr'].astype(int)

#st.markdown(f"<h3 style='text-align: right; font-weight: bold;'>check: {total_initial_value}</h3>", unsafe_allow_html=True)

# Calculate the total portfolio value
total_value = df['value'].sum()
total_value_inr = total_value * 90

total_value_inr_formatted = "₹{:,.0f}".format(total_value_inr)

percent_gain_portfolio = (total_value_inr - total_initial_value) * 100 / total_initial_value
percent_gain_portfolio = "{:,.0f}%".format(percent_gain_portfolio)

# Streamlit app layout
st.title("Crypto Portfolio Tracker")
st.markdown(f"<h3 style='text-align: right; font-weight: bold;'>Total Portfolio Value: {total_value_inr_formatted}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: right; font-weight: bold;'>Total Portfolio Gain: {percent_gain_portfolio}</h3>", unsafe_allow_html=True)
st.write("This dashboard shows your crypto portfolio performance.")

# Display the updated data
st.subheader("Updated Portfolio Data")
st.dataframe(df)

# Bubble Chart
st.subheader("Portfolio Overview - Bubble Chart")
fig_bubble = px.scatter(
    df, 
    x='coin', 
    y='value_inr', 
    size='value_inr', 
    color='coin', 
    hover_name='coin', 
    text='coin', 
    title="Bubble Chart of Portfolio"
)
fig_bubble.update_traces(marker=dict(sizemode='diameter', line_width=2, opacity=0.6), textfont=dict(color='white', size=14))
st.plotly_chart(fig_bubble, use_container_width=True)

# Percent Gain by Coin Bar Chart
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
fig_bar.update_traces(
    marker=dict(
        color=df['percent_gain'],  # Set the color based on percent_gain
        colorbar=dict(
            title="Percent Gain",
            tickvals=[-10, -5, 0, 5, 10, 15, 20],  # Custom ticks for the color scale
        )
    )
)
st.plotly_chart(fig_bar, use_container_width=True)

# Percent Gain vs Value Scatter Plot
st.subheader("Percent Gain vs Value")
fig_scatter = px.scatter(
    df, 
    x='percent_gain', 
    y='value_inr', 
    size='value_inr', 
    color='coin', 
    hover_name='coin', 
    title="Percent Gain vs Portfolio Value",
    labels={"percent_gain": "Percent Gain (%)", "value": "Value (₹)"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

####

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
    title="Multipliers Reached by Coins",
    xaxis=dict(title="Coin", tickangle=45),
    yaxis=dict(title="Multiplier", tickvals=['3x', '5x', '10x', '20x'], ticktext=['3x', '5x', '10x', '20x']),
    showlegend=False,
    height=600,
    margin=dict(l=50, r=50, t=50, b=50),
)

# Display the lollipop chart
st.plotly_chart(fig_lollipop, use_container_width=True)
