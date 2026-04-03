import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard")
st.write("Real-time inventory insights and optimization recommendations")

# Mock Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total SKUs", "2,847", "+12% vs last month")
with col2:
    st.metric("Stock Value", "$1.2M", "+8.3% vs last month")
with col3:
    st.metric("Turnover Rate", "4.2x", "+0.6 vs last month")
with col4:
    st.metric("Low Stock Alerts", "23", "+5 vs last month", delta_color="inverse")

st.markdown("---")

col_left, col_mid, col_right = st.columns(3)

with col_left:
    with st.container(border=True):
        st.subheader("Stock by Category")
        category_data = pd.DataFrame([
            {"name": "Beverages", "value": 1400},
            {"name": "Grains", "value": 1100},
            {"name": "Dairy", "value": 800},
            {"name": "Snacks", "value": 650},
            {"name": "Condiments", "value": 400},
            {"name": "Frozen", "value": 250}
        ])
        fig_bar = px.bar(category_data, x="value", y="name", orientation='h', color_discrete_sequence=['#10B981'])
        fig_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

with col_mid:
    with st.container(border=True):
        st.subheader("Status Distribution")
        pie_data = pd.DataFrame([
            {"name": "Optimal", "value": 65, "color": "#10B981"},
            {"name": "Low Stock", "value": 18, "color": "#F59E0B"},
            {"name": "Critical", "value": 8, "color": "#EF4444"},
            {"name": "Overstock", "value": 9, "color": "#3B82F6"}
        ])
        fig_pie = px.pie(pie_data, values="value", names="name", hole=0.6, color="name", 
                         color_discrete_map={row['name']: row['color'] for _, row in pie_data.iterrows()})
        fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    with st.container(border=True):
        st.subheader("Stock Level Trend")
        trend_data = pd.DataFrame([
            {"month": "Sep", "value": 72}, {"month": "Oct", "value": 68},
            {"month": "Nov", "value": 75}, {"month": "Dec", "value": 80},
            {"month": "Jan", "value": 78}, {"month": "Feb", "value": 82}
        ])
        fig_line = px.line(trend_data, x="month", y="value", markers=True, color_discrete_sequence=['#10B981'])
        fig_line.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300)
        st.plotly_chart(fig_line, use_container_width=True)
