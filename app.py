import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Student Analytics Dashboard",
    layout="wide"
)

# Title
st.title("🎓 Student Academic Performance & Placement Analytics")

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

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🎓 Total Students",
        total_students
    )

with col2:
    st.metric(
        "📊 Average CGPA",
        average_cgpa
    )

with col3:
    st.metric(
        "💼 Placed Students",
        placed_students
    )

with col4:
    st.metric(
        "🎯 Placement %",
        f"{placement_percentage}%"
    )

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