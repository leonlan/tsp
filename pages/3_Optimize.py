import streamlit as st
from io import StringIO
from contextlib import redirect_stdout
import numpy as np

st.title("🗺️ Optimize")


def haversine(coords: list[tuple[int, int]]) -> np.ndarray:
    """
    Converts coordinates to a Haversine distance matrix (in meters).
    """

    from sklearn.metrics.pairwise import haversine_distances
    from math import radians

    RADIUS_EARTH = 6371000  # meters

    coords_rad = np.array(
        [[radians(lat), radians(lon)] for lat, lon in coords]
    )
    dist_matrix = haversine_distances(coords_rad)
    dist_meters = (dist_matrix * RADIUS_EARTH).round()  # rads to meters
    return dist_meters


def solve(time_limit):
    df = st.session_state.orders_df
    ...
    return tour


# Solve
time_limit = st.slider("Time Limit (seconds)", 1, 60, 10)

output_capture = StringIO()

if st.button("Solve Optimization Problem"):
    with redirect_stdout(output_capture):
        solution = solve(time_limit)  # TODO

    st.session_state.tour = tour
    st.success("Optimization completed!")
