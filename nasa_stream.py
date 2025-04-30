import mysql.connector as db
import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid
connection = db.connect (

    host = "localhost",
    user = "root",
    password = "Srinivas123@",
    database = "nasa"
    
)
curr = connection.cursor()


# --- SQL Queries ---


sql_queries = {

    "1. Count asteroid approaches": """
        SELECT neo_reference_id, COUNT(*) AS approach_count
        FROM close_approach
        GROUP BY neo_reference_id
    """,
    "2. Average velocity per asteroid": """
        SELECT neo_reference_id, AVG(relative_velocity_kmph) AS avg_velocity
        FROM close_approach
        GROUP BY neo_reference_id
    """,
    "3. Top 10 fastest asteroids": """
        SELECT neo_reference_id, MAX(relative_velocity_kmph) AS top_speed
        FROM close_approach
        GROUP BY neo_reference_id
        ORDER BY top_speed DESC
        LIMIT 10
    """,
    "4. Hazardous asteroids (>3 approaches)": """
        SELECT id, COUNT(*) AS approach_count
        FROM asteroids
        WHERE  is_potentially_hazardous_asteroid = 1
        GROUP BY id
        HAVING approach_count > 3

    """,
    "5. Month with most approaches": """
        SELECT DATE_FORMAT(close_approach_date, '%Y-%m-%d') AS month, COUNT(*) AS count
        FROM close_approach
        GROUP BY month
        ORDER BY count DESC
        LIMIT 5
    """,
    "6. Fastest asteroid ever": """
        SELECT neo_reference_id, close_approach_date, relative_velocity_kmph
        FROM close_approach
        ORDER BY relative_velocity_kmph DESC
        LIMIT 1
    """,
    "7. Asteroids by max estimated diameter": """
        SELECT id, name, estimated_diameter_max_km
        FROM asteroids
        ORDER BY estimated_diameter_max_km DESC
    """,
    "8. Asteroids getting closer over time": """
        SELECT neo_reference_id, close_approach_date, miss_distance_km
        FROM close_approach
        ORDER BY neo_reference_id, close_approach_date
    """,
    "9. Closest approach per asteroid": """
        SELECT neo_reference_id, close_approach_date, miss_distance_km
        FROM close_approach
        WHERE (neo_reference_id, miss_distance_km) IN (
            SELECT neo_reference_id, MIN(miss_distance_km)
            FROM close_approach
            GROUP BY neo_reference_id
        )
    """,
    "10. Asteroids with velocity > 50,000 km/h": """
        SELECT neo_reference_id, close_approach_date, relative_velocity_kmph
        FROM close_approach
        WHERE relative_velocity_kmph > 50000
    """,
    "11. Count of approaches per month": """
        SELECT DATE_FORMAT(close_approach_date, '%Y-%m') AS month, COUNT(*) AS count
        FROM close_approach
        GROUP BY month
        ORDER BY month
    """,
    "12. Brightest asteroid (lowest magnitude)": """
        SELECT id, name, absolute_magnitude_h
        FROM asteroids
        ORDER BY absolute_magnitude_h ASC
        LIMIT 1
    """,
    
    "13. Hazardous vs Non-Hazardous": """
        SELECT is_potentially_hazardous_asteroid, COUNT(*) AS count
        FROM asteroids
        GROUP BY is_potentially_hazardous_asteroid
    """,
    "14. Passed closer than Moon (<1 LD)": """
        SELECT neo_reference_id, close_approach_date, miss_distance_lunar
        FROM close_approach
        WHERE miss_distance_lunar > 1
    """,
    "15. Came within 0.05 astronomical": """
        SELECT neo_reference_id, close_approach_date, astronomical
        FROM close_approach
        WHERE astronomical< 0.05
    """,
    "16.Asteroids Approaching Earth with Specific Velocity Range":"""
        SELECT neo_reference_id, relative_velocity_kmph
        FROM close_approach
        WHERE relative_velocity_kmph BETWEEN 20000 AND 50000
        ORDER BY relative_velocity_kmph DESC
        """,
    "17.Asteroids with Largest Estimated Diameters":"""
        SELECT id, name, estimated_diameter_max_km
        FROM asteroids
        ORDER BY estimated_diameter_max_km DESC
        LIMIT 5;
        """

}

# --- Sidebar ---
st.sidebar.title("🚀 Asteroids Approaches")
menu_selection = st.sidebar.radio("Go to", ["Filter Criteria", "Queries"])

# --- Main Layout ---
st.markdown("<h1 style='text-align: center;'>🚀 NASA Asteroid Tracker</h1>", unsafe_allow_html=True)
st.markdown("---")


# === Main Page Behavior ===
if menu_selection == "Filter Criteria":
    # --- FILTER CRITERIA PAGE ---
    st.header("🎛️ Set Filters")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.start_date = st.date_input("From Date", st.session_state.start_date)
        st.session_state.min_vel = st.slider("Min Velocity (km/h)", 0.00, 100000.00,value=(1400.00,175000.00))

        st.session_state.diam_min = st.slider("Min Diameter (km)", 0.00, 5.00, value=(0.00,5.00))
    with col2:
        st.session_state.end_date = st.date_input("To Date", st.session_state.end_date)
        st.session_state.diam_max = st.slider("Max Diameter (km)", 0.00, 5.00, value=(0.00,10.00))
        st.session_state.max_au = st.slider("Max AU Distance", 0.00, 1.00, value=(0.00162219,0.50015825))

    st.session_state.max_ld = st.slider("Max Lunar Distance", 0.00, 10.00, value=(0.631031,191.859))
    st.session_state.hazardous_filter = st.selectbox(
        "Hazardous Only?", [ 1,0],
        index=None
    )

    if st.button("🔍 Apply Filters",key="apply_filiters"):
        # --- Build the Custom Query ---
        query = """
SELECT 
    ca.neo_reference_id,
    ca.close_approach_date,
    ca.relative_velocity_kmph,
    ca.astronomical,
    ca.miss_distance_lunar,
    a.name,
    a.estimated_diameter_min_km,
    a.estimated_diameter_max_km,
    a.is_potentially_hazardous_asteroid
FROM close_approach ca
JOIN asteroids a ON ca.neo_reference_id = a.id
WHERE 
     ca.close_approach_date BETWEEN %s AND %s
        AND ca.relative_velocity_kmph BETWEEN %s AND %s
        AND ca.astronomical BETWEEN %s AND %s
        AND ca.miss_distance_lunar BETWEEN %s AND %s
        AND a.estimated_diameter_min_km BETWEEN %s AND %s
        AND a.estimated_diameter_max_km BETWEEN %s AND %s
        AND a.is_potentially_hazardous_asteroid = %s

"""
        params = [
        st.session_state.start_date, st.session_state.end_date,
        st.session_state.min_vel[0],st.session_state.min_vel[1],
        st.session_state.max_au[0], st.session_state.max_au[1],
        st.session_state.max_ld[0],st.session_state.max_ld[1],
        st.session_state.diam_min[0], st.session_state.diam_min[1],
        st.session_state.diam_max[0], st.session_state.diam_max[1],
        st.session_state.hazardous_filter
    ]
       
        # --- Run the Query ---
        curr.execute(query,params)
        rows = curr.fetchall()
        cols = [d[0] for d in curr.description]
        df = pd.DataFrame(rows, columns=cols)
        df.drop_duplicates(inplace=True) 
        st.subheader("📊 Filtered Results")
        st.dataframe(df)

    else:
        st.info("👆 Set filters and click Apply Filters to see results.")

elif menu_selection == "Queries":
    # --- QUERIES PAGE ---
    st.header("📄 Query Section")

    query_label = st.selectbox("Select a Query:", list(sql_queries.keys()))

    if st.button("🚀 Run Selected Query",key="run_query"):
        curr.execute(sql_queries[query_label])
        rows = curr.fetchall()
        cols = [d[0] for d in curr.description]
        df = pd.DataFrame(rows, columns=cols)

        st.subheader(f"📊 Results for {query_label}")
        AgGrid(df)
    else:
        st.info("👆 Select a query and click Run to show results.")
