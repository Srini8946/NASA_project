# NASA_project
## 🎯Project Objective!:
### * Build a data pipeline to analyze asteroid data from NASA’s API.
### * Extract, transform, and store 10,000+ NEO records.
### * Enable exploration through a Streamlit dashboard.

## Skills & Tools Used:
### Skills: API Integration, JSON Parsing, SQL, Streamlit, Data Analysis
### Tools: Python,MySQL, NASA API, Streamlit

## Business Use Cases:
###  Monitoring - Identify hazardous asteroids
###  Date-Based Trends - Discover patterns in asteroid visits
###  Orbit Analysis - Analyze orbiting bodies
###  Educational Access - Make data accessible to non-tech users

## 🔄 Data Pipeline Overview:
### 1. NASA API with Pagination
### 2. JSON Data Extraction & Cleaning
### 3. SQL Table Creation & Insertion
### 4. Dashboard Visualization via streamlit

## Database Design:
###  * Table 1: asteroids - General NEO data
###  * Table 2: close_approach - Per-approach data

## Streamlit Dashboard Features:
###  * Dropdown to run 15+ predefined SQL queries
###  * Filters: date range, velocity, distance, size
###  * Interactive UI with st.slider, st.selectbox, st.date_input
###  * Visual and tabular data presentation

## Challenges & Solutions:
### * Complex nested JSON → Used safe .get() access
### * Pagination logic → Automated with next link
### * Null/missing fields → Skipped or defaulted values

## Future Enhancements:
### * Live data updates
### * Orbit visualization
### * User-generated queries
### * Host on Streamlit Cloud

## Conclusion:
### This project converts raw space data into clear, actionable insights.
### A full-stack pipeline from API to dashboard — accessible to all.








