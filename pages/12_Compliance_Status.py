import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Compliance data
met = 4
total = 10
not_met = total - met

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=['Met', 'Not Met'],
    values=[met, not_met],
    hole=.3,
    marker_colors=['#00C853', '#FF3D00']
)])

# Get today's date in the desired format
today_date = datetime.now().strftime("%d %b %Y")

# Update layout
fig.update_layout(
    title_text="EU AI Act Compliance Status: {} out of {} as of {}".format(met, total, today_date), 
    annotations=[dict(text=f'{met}/{total}', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

# Display the chart in Streamlit
st.plotly_chart(fig)

