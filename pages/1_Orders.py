import streamlit as st

st.title("Orders List")

df = st.session_state.orders_df
edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # allow adding rows
    use_container_width=True,
    key="orders_editor",
)

# --- Validation ---
errors = []

# Check for valid latitude/longitude
invalid_lat = ~edited_df["Latitude"].between(-90, 90)
invalid_lon = ~edited_df["Longitude"].between(-180, 180)

if invalid_lat.any():
    errors.append("One or more latitude values are out of bounds (-90 to 90).")

if invalid_lon.any():
    errors.append(
        "One or more longitude values are out of bounds (-180 to 180)."
    )

if errors:
    for err in errors:
        st.error(err)
    st.warning("Please fix the above issues before saving.")
else:
    if st.button("💾 Save Changes"):
        st.session_state.orders_df = edited_df
        st.success("✅ Changes saved in session.")

    if st.button("💾 Save to File"):
        edited_df.to_csv("data/orders_data.csv", index=False)
        st.success("✅ Data saved to CSV!")
