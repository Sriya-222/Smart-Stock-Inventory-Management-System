import streamlit as st
import pandas as pd
import math
from src.lib.api import api_call

st.title("Products")
st.write("Browse and manage available inventory items.")

user = st.session_state.get('user', {})
is_admin = user.get('role') == 'admin'

def fetch_products():
    try:
        return api_call('/products')
    except Exception as e:
        st.error(f"Failed to fetch products: {str(e)}")
        return []

if "products" not in st.session_state:
    st.session_state.products = fetch_products()
    
# Add Product section for admins
if is_admin:
    with st.expander("➕ Add New Product"):
        with st.form("add_product"):
            st.subheader("General Information")
            col1, col2 = st.columns(2)
            name = col1.text_input("Product Name")
            sku = col2.text_input("SKU")
            category = st.selectbox("Category", ["Electronics", "Clothing", "Beverages", "Grains", "Dairy", "Snacks"])
            
            col_p1, col_p2, col_p3 = st.columns(3)
            price = col_p1.number_input("Unit Selling Price ($)", min_value=0.0, step=0.01)
            cost = col_p2.number_input("Cost Price ($)", min_value=0.0, step=0.01)
            stock = col_p3.number_input("Initial Stock", min_value=0, step=1)

            st.markdown("---")
            st.subheader("Smart Inventory Parameters")
            st.write("Fill these out to automatically calculate the Reorder Point (ROP) and Economic Order Quantity (EOQ).")
            
            c1, c2, c3 = st.columns(3)
            daily_demand = c1.number_input("Avg. Daily Demand", min_value=0.0, step=1.0, value=5.0)
            lead_time = c2.number_input("Lead Time (Days)", min_value=0.0, step=1.0, value=7.0)
            safety_stock = c3.number_input("Safety Stock", min_value=0.0, step=1.0, value=10.0)
            
            c4, c5 = st.columns(2)
            ordering_cost = c4.number_input("Ordering Cost per Order ($)", min_value=0.0, step=1.0, value=50.0)
            annual_holding_cost = c5.number_input("Annual Holding Cost per Unit ($)", min_value=0.0, step=0.1, value=2.5)
            
            submitted = st.form_submit_button("Calculated Smart Inventory & Create Product", type="primary")
            if submitted:
                if not name or not sku:
                    st.error("Name and SKU are required.")
                elif annual_holding_cost == 0:
                    st.error("Holding cost cannot be zero to calculate EOQ.")
                else:
                    try:
                        # ROP = (Daily Demand * Lead Time) + Safety Stock
                        calculated_rop = math.ceil((daily_demand * lead_time) + safety_stock)
                        
                        # Annual Demand = Daily Demand * 365
                        annual_demand = daily_demand * 365
                        
                        # EOQ = sqrt((2 * Annual Demand * Ordering Cost) / Holding Cost)
                        calculated_eoq = math.ceil(math.sqrt((2 * annual_demand * ordering_cost) / annual_holding_cost))
                        
                        new_pwd = api_call('/products', method='POST', data={
                            "name": name,
                            "sku": sku,
                            "category": category,
                            "price": price,
                            "costPrice": cost,
                            "stock": stock,
                            "minLevel": calculated_rop,
                            "reorderPoint": calculated_eoq,
                            "description": "A great product"
                        })
                        st.session_state.products = fetch_products() # Refresh
                        st.success(f"Product added successfully! Calculated ROP: {calculated_rop}, Calculated EOQ: {calculated_eoq}")
                    except Exception as e:
                        st.error(f"Failed to add: {str(e)}")

st.markdown("---")

search = st.text_input("🔍 Search products by name...")
categories = ["All", "Electronics", "Clothing", "Beverages", "Grains", "Dairy", "Snacks"]
cat_filter = st.selectbox("Category Filter", categories)

filtered = []
for p in st.session_state.products:
    if search.lower() in p.get('name', '').lower():
        if cat_filter == "All" or p.get('category') == cat_filter:
            filtered.append(p)

if not filtered:
    st.info("No products found.")
else:
    for p in filtered:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
            with c1:
                st.subheader(p.get('name', 'Unknown'))
                st.caption(f"SKU: {p.get('sku', 'N/A')} | Cat: {p.get('category', '')}")
            with c2:
                st.write(f"**Price:** ${p.get('price', 0):.2f}")
                st.write(f"**Stock:** {p.get('stock', 0)}")
            with c3:
                stock = p.get('stock', 0)
                min_lvl = p.get('minLevel', 10)
                if stock <= 0:
                    st.error("Out of Stock")
                elif stock <= min_lvl:
                    st.warning(f"Low Stock (ROP: {min_lvl})")
                else:
                    st.success("In Stock")
            with c4:
                if is_admin:
                    if st.button("Delete", key=f"del_{p['_id']}", type="primary"):
                        try:
                            api_call(f"/products/{p['_id']}", method='DELETE')
                            st.success("Deleted")
                            st.session_state.products = fetch_products()
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                else:
                    quantity = st.number_input("Qty", min_value=1, max_value=max(1, stock), key=f"qty_{p['_id']}")
                    if st.button("Buy", key=f"buy_{p['_id']}", disabled=stock<=0, type="primary"):
                        try:
                            api_call(f"/products/{p['_id']}/buy", method='PUT', data={"quantity": quantity})
                            st.success(f"Purchased {quantity}x {p['name']}!")
                            st.session_state.products = fetch_products()
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
