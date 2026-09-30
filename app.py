import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Student Analytics Dashboard",
    layout="wide"
)

# Professional Dashboard Styling

st.markdown("""
<style>

.stApp {
    background-color: #071A33;
}

[data-testid="stSidebar"] {
    background-color: #06152A;
}

[data-testid="stSidebar"] * {
    color: white;
}

h1 {
    color: white;
    font-size: 36px;
    font-weight: 700;
}

h2, h3 {
    color: white;
}

.stMetric {
    background-color: #0D2A4D;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1E4D7A;
}

.stMetric label {
    color: white !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: white;
}

div[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# Title
# Dashboard Header

st.markdown("""
<div style="
    background: linear-gradient(90deg, #082B55, #0B3B70);
    padding: 20px 25px;
    border-radius: 12px;
    margin-bottom: 20px;
">

<h1 style="
    margin: 0;
    color: white;
    font-size: 34px;
">
🎓 Student Academic Performance & Placement Analytics
</h1>

<p style="
    margin: 6px 0 0 0;
    color: #B9D9FF;
    font-size: 17px;
">
Data-Driven Insights for Better Decisions
</p>

</div>
""", unsafe_allow_html=True)

st.write("Student data analysis dashboard")

# Load dataset
df = pd.read_csv("data/students.csv")

# Show dataset
st.subheader("Student Dataset")

# Sidebar Project Info

st.sidebar.title("🎓 Student Analytics")

st.sidebar.write(
    "Academic Performance & Placement Dashboard"
)

st.sidebar.divider()

# Sidebar Filters

st.sidebar.header("🔎 Filters")

selected_department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

if selected_department != "All":
    df = df[df["Department"] == selected_department]

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

if selected_gender != "All":
    df = df[df["Gender"] == selected_gender]

selected_placement = st.sidebar.selectbox(
    "Select Placement Status",
    ["All"] + sorted(df["Placement_Status"].unique().tolist())
)

if selected_placement != "All":
    df = df[df["Placement_Status"] == selected_placement]

st.dataframe(df)
# Download Filtered Data

st.subheader("⬇️ Download Data")

csv_data = df.to_csv(index=False)

st.download_button(
    label="Download Student Data",
    data=csv_data,
    file_name="student_data.csv",
    mime="text/csv"
)

# Calculate KPI values

total_students = len(df)

average_cgpa = round(df["CGPA"].mean(), 2)

placed_students = (
    df["Placement_Status"] == "Placed"
).sum()

placement_percentage = round(
    (placed_students / total_students) * 100,
    2
)

# Create KPI columns

# KPI Cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0878E8, #1554C0);
        padding: 20px;
        border-radius: 12px;
        color: white;
        height: 120px;
    ">
        <div style="font-size: 17px;">👨‍🎓 Total Students</div>
        <div style="font-size: 32px; font-weight: bold;">
            {total_students}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #10B981, #059669);
        padding: 20px;
        border-radius: 12px;
        color: white;
        height: 120px;
    ">
        <div style="font-size: 17px;">🎓 Average CGPA</div>
        <div style="font-size: 32px; font-weight: bold;">
            {average_cgpa}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #7C3AED, #5B21B6);
        padding: 20px;
        border-radius: 12px;
        color: white;
        height: 120px;
    ">
        <div style="font-size: 17px;">💼 Placed Students</div>
        <div style="font-size: 32px; font-weight: bold;">
            {placed_students}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #F59E0B, #EA580C);
        padding: 20px;
        border-radius: 12px;
        color: white;
        height: 120px;
    ">
        <div style="font-size: 17px;">🎯 Placement Rate</div>
        <div style="font-size: 32px; font-weight: bold;">
            {placement_percentage}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# Department Analysis

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏫 Students by Department")

    department_count = df["Department"].value_counts()

    st.bar_chart(department_count)

with col2:
    st.subheader("📊 Average CGPA by Department")

    department_cgpa = (
        df.groupby("Department")["CGPA"]
        .mean()
        .round(2)
    )

    st.bar_chart(department_cgpa)

# Placement Analysis

col1, col2 = st.columns(2)

with col1:
    st.subheader("💼 Placement Status")

    placement_count = df["Placement_Status"].value_counts()

    st.bar_chart(placement_count)

with col2:
    st.subheader("🎓 Internship vs Placement")

    internship_placement = pd.crosstab(
        df["Internships"],
        df["Placement_Status"]
    )

    st.bar_chart(internship_placement)

# Attendance vs CGPA

st.subheader("📚 Attendance vs CGPA")

st.scatter_chart(
    df,
    x="Attendance",
    y="CGPA"
)

# About Project

st.divider()

st.subheader("📌 About This Project")

st.write(
    """
    This dashboard analyzes student academic performance
    and placement-related data.

    It provides insights into CGPA, attendance, internships,
    departments, and placement status.
    """
)

st.caption(
    "Built using Python, Pandas, NumPy, Matplotlib and Streamlit."
)

st.divider()

st.caption("👨‍💻 Developed by Lingeshwaran D")
st.caption("B.Tech Artificial Intelligence & Data Science")
st.caption("Student Analytics Dashboard • 2026")