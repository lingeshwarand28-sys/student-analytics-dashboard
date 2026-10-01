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

# =========================
# KPI CARDS
# =========================

total_students = len(df)

average_cgpa = round(df["CGPA"].mean(), 2)

average_attendance = round(
    df["Attendance"].mean(), 1
)

placed_students = (
    df["Placement_Status"] == "Placed"
).sum()

placement_rate = round(
    (placed_students / total_students) * 100,
    1
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🎓 Total Students",
        total_students
    )

with col2:
    st.metric(
        "🎓 Average CGPA",
        average_cgpa
    )

with col3:
    st.metric(
        "📅 Average Attendance",
        f"{average_attendance}%"
    )

with col4:
    st.metric(
        "💼 Placement Rate",
        f"{placement_rate}%"
    )

# =========================
# PLACEMENT STATUS CHART
# =========================

st.subheader("💼 Placement Status")

placement_count = (
    df["Placement_Status"]
    .value_counts()
    .reset_index()
)

placement_count.columns = [
    "Placement_Status",
    "Student_Count"
]

fig = px.pie(
    placement_count,
    names="Placement_Status",
    values="Student_Count",
    hole=0.5,
    title="Placement Status Distribution"
)

fig.update_traces(
    textinfo="percent+label"
)

fig.update_layout(
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# DEPARTMENT-WISE AVERAGE CGPA
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Department-wise Average CGPA")

department_cgpa = (
    df.groupby("Department")["CGPA"]
    .mean()
    .round(2)
    .reset_index()
)

fig_cgpa = px.bar(
    department_cgpa,
    x="CGPA",
    y="Department",
    orientation="h",
    text="CGPA",
    title="Average CGPA by Department"
)

fig_cgpa.update_traces(
    textposition="outside"
)

fig_cgpa.update_layout(
    height=400,
    xaxis_title="Average CGPA",
    yaxis_title="Department"
)

st.plotly_chart(
    fig_cgpa,
    use_container_width=True
)

# =========================
# STUDENTS BY DEPARTMENT
# =========================
with col2:
    st.subheader("🏫 Students by Department")

department_count = (
    df["Department"]
    .value_counts()
    .reset_index()
)

department_count.columns = [
    "Department",
    "Student_Count"
]

fig_dept = px.bar(
    department_count,
    x="Department",
    y="Student_Count",
    text="Student_Count",
    title="Students by Department"
)

fig_dept.update_traces(
    textposition="outside"
)

fig_dept.update_layout(
    height=400,
    xaxis_title="Department",
    yaxis_title="Number of Students"
)

st.plotly_chart(
    fig_dept,
    use_container_width=True
)

# =========================
# CGPA DISTRIBUTION
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 CGPA Distribution")

    fig_cgpa_dist = px.histogram(
        df,
        x="CGPA",
        nbins=12,
        title="CGPA Distribution",
        marginal="box"
    )

    fig_cgpa_dist.update_layout(
        height=450,
        xaxis_title="CGPA",
        yaxis_title="Number of Students"
    )

    st.plotly_chart(
        fig_cgpa_dist,
        use_container_width=True
    )

# =========================
# ATTENDANCE VS CGPA
# =========================

st.subheader("📚 Attendance vs CGPA")

fig_attendance = px.scatter(
    df,
    x="Attendance",
    y="CGPA",
    hover_data=[
        "Student_ID",
        "Department",
        "Placement_Status"
    ],
    title="Attendance vs CGPA"
)

fig_attendance.update_traces(
    marker=dict(size=9)
)

fig_attendance.update_layout(
    height=450,
    xaxis_title="Attendance (%)",
    yaxis_title="CGPA"
)

st.plotly_chart(
    fig_attendance,
    use_container_width=True
)

# Sidebar Project Info

st.sidebar.title("🎓 Student Analytics")

st.sidebar.write(
    "Academic Performance & Placement Dashboard"
)
st.sidebar.divider()

st.sidebar.title("🎓 Student Analytics")
st.sidebar.write("Academic Performance & Placement")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📋 Student Data"]
)

if page == "📋 Student Data":

    st.title("📋 Student Data")

    st.write("Complete student academic and placement records")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
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

selected_dept = st.selectbox(
    "🏫 Filter by Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

if selected_dept != "All":
    df = df[df["Department"] == selected_dept]

selected_placement = st.selectbox(
    "💼 Filter by Placement Status",
    ["All"] + sorted(df["Placement_Status"].unique().tolist())
)

if selected_placement != "All":
    df = df[df["Placement_Status"] == selected_placement]

selected_gender = st.selectbox(
    "👤 Filter by Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

if selected_gender != "All":
    df = df[df["Gender"] == selected_gender]

search_student = st.text_input(
    "🔎 Search Student ID",
    placeholder="Enter Student ID"
)

if search_student:
    df = df[
        df["Student_ID"].astype(str).str.contains(
            search_student,
            case=False,
            na=False
        )
    ]

st.download_button(
        label="⬇️ Download Student Data",
        data=df.to_csv(index=False),
        file_name="student_data_filtered.csv",
        mime="text/csv"
    )

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.stop()

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

st.caption(
    f"Showing {len(df)} student records based on selected filters."
)

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

    placement_count = (
        df["Placement_Status"]
        .value_counts()
        .reset_index()
    )

    placement_count.columns = [
        "Placement_Status",
        "Student_Count"
    ]

    fig_placement = px.pie(
        placement_count,
        names="Placement_Status",
        values="Student_Count",
        hole=0.5,
        title="Placement Status Distribution"
    )

    fig_placement.update_traces(
        textinfo="percent+label"
    )

    fig_placement.update_layout(
        height=400
    )

    st.plotly_chart(
    fig_placement,
    use_container_width=True,
    key="placement_status_chart"
)

with col2:
    st.subheader("🎓 Internship vs Placement")

    internship_placement = pd.crosstab(
        df["Internships"],
        df["Placement_Status"]
    )

    internship_placement = internship_placement.reset_index()

    fig_internship = px.bar(
        internship_placement,
        x="Internships",
        y="Placed",
        title="Internships vs Placed Students",
        text="Placed"
    )

    fig_internship.update_traces(
        textposition="outside"
    )

    fig_internship.update_layout(
        height=400,
        xaxis_title="Number of Internships",
        yaxis_title="Placed Students"
    )

    st.plotly_chart(
        fig_internship,
        use_container_width=True
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