import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Analytics")
st.write("Detailed metrics and performance overview.")

# Mock stat cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", "$45,231.89", "20.1%")
c2.metric("Active Users", "2,350", "180.1%")
c3.metric("Sales", "+12,234", "19%")
c4.metric("Active Products", "573", "-201", delta_color="inverse")

st.markdown("---")

col_main, col_sub = st.columns([2, 1])

with col_main:
    with st.container(border=True):
        st.subheader("Revenue Overview")
        revenue_data = pd.DataFrame([
            {"month": "Jan", "revenue": 4000},
            {"month": "Feb", "revenue": 3000},
            {"month": "Mar", "revenue": 5000},
            {"month": "Apr", "revenue": 4500},
            {"month": "May", "revenue": 6000},
            {"month": "Jun", "revenue": 5500},
            {"month": "Jul", "revenue": 7000}
        ])
        fig_area = px.area(revenue_data, x="month", y="revenue", color_discrete_sequence=['#10B981'])
        fig_area.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_area, use_container_width=True)

with col_sub:
    with st.container(border=True):
        st.subheader("Sales by Category")
        sales_data = pd.DataFrame([
            {"category": "Electronics", "sales": 400},
            {"category": "Clothing", "sales": 300},
            {"category": "Home", "sales": 200},
            {"category": "Books", "sales": 278},
            {"category": "Sports", "sales": 189}
        ])
        fig_bar = px.bar(sales_data, x="category", y="sales", color_discrete_sequence=['#10B981'])
        fig_bar.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
