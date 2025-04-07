import streamlit as st
import pandas as pd

st.set_page_config(page_title="Home", layout="wide")
st.title("Breinstein Delivery")

if "orders_df" not in st.session_state:
    st.session_state.orders_df = pd.read_csv("data/orders_data.csv")

st.markdown("Use the sidebar to view Orders or see them on the Map.")
