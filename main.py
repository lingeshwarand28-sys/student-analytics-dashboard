import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# Number of students
students = 500

# Create student data
data = {
    "Student_ID": [
        f"S{i:04d}" for i in range(1, students + 1)
    ],

    "Age": np.random.randint(
        18, 23, students
    ),

    "Gender": np.random.choice(
        ["Male", "Female"],
        students
    ),

    "Department": np.random.choice(
        ["AI&DS", "CSE", "ECE", "IT", "EEE"],
        students
    ),

    "Attendance": np.round(
        np.random.uniform(55, 98, students),
        1
    ),

    "CGPA": np.round(
        np.random.uniform(5.5, 9.8, students),
        2
    ),

    "Internships": np.random.randint(
        0, 4, students
    ),

    "Projects": np.random.randint(
        0, 6, students
    ),

    "Aptitude_Score": np.random.randint(
        40, 101, students
    ),

    "Technical_Score": np.random.randint(
        40, 101, students
    )
}

# Convert data into a DataFrame
df = pd.DataFrame(data)
# Create Placement Status
df["Placement_Status"] = np.where(
    (df["CGPA"] >= 7.0) &
    (df["Technical_Score"] >= 65) &
    (df["Aptitude_Score"] >= 60),
    "Placed",
    "Not Placed"
)

# Display first 5 students
print("===== STUDENT DATA =====")
print(df.head())

# Display number of rows and columns
print("\n===== DATASET SIZE =====")
print(df.shape)

# Save data as CSV
df.to_csv(
    "data/students.csv",
    index=False
)

print("\nDataset created successfully!")

# Check dataset information
print("\n===== DATA INFORMATION =====")
print(df.info())

# Check missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# Check duplicate records
print("\n===== DUPLICATE RECORDS =====")
print("Number of duplicate rows:", df.duplicated().sum())

# Basic statistics
print("\n===== BASIC STATISTICS =====")
print(df.describe())

# Department-wise student count
print("\n===== DEPARTMENT-WISE STUDENT COUNT =====")
print(df["Department"].value_counts())

# Department-wise average CGPA
print("\n===== DEPARTMENT-WISE AVERAGE CGPA =====")

department_cgpa = df.groupby("Department")["CGPA"].mean()

print(department_cgpa.round(2))

# Placement status analysis
print("\n===== PLACEMENT STATUS =====")

placement_count = df["Placement_Status"].value_counts()

print(placement_count)

# Calculate placement percentage
total_students = len(df)

placed_students = (df["Placement_Status"] == "Placed").sum()

placement_percentage = (
    placed_students / total_students
) * 100

print("\n===== PLACEMENT PERCENTAGE =====")
print("Total Students:", total_students)
print("Placed Students:", placed_students)
print("Placement Percentage:", round(placement_percentage, 2), "%")

# Attendance vs CGPA correlation
print("\n===== ATTENDANCE VS CGPA =====")

correlation = df["Attendance"].corr(df["CGPA"])

print("Correlation:", round(correlation, 2))

# Department-wise student count chart

department_count = df["Department"].value_counts()

plt.figure(figsize=(8, 5))

department_count.plot(kind="bar")

plt.title("Students by Department")
plt.xlabel("Department")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.show()

# Department-wise average CGPA chart

department_cgpa = df.groupby("Department")["CGPA"].mean()

plt.figure(figsize=(8, 5))

department_cgpa.plot(kind="bar")

plt.title("Average CGPA by Department")
plt.xlabel("Department")
plt.ylabel("Average CGPA")

plt.tight_layout()
plt.show()

# CGPA distribution

plt.figure(figsize=(8, 5))

plt.hist(df["CGPA"], bins=10)

plt.title("CGPA Distribution")
plt.xlabel("CGPA")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.show()

# Placement status pie chart

placement_count = df["Placement_Status"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    placement_count,
    labels=placement_count.index,
    autopct="%1.1f%%"
)

plt.title("Placement Status")

plt.show()

# Attendance vs CGPA scatter plot

plt.figure(figsize=(8, 5))

plt.scatter(
    df["Attendance"],
    df["CGPA"]
)

plt.title("Attendance vs CGPA")
plt.xlabel("Attendance (%)")
plt.ylabel("CGPA")

plt.tight_layout()
plt.show()

# Internship vs Placement analysis

internship_placement = pd.crosstab(
    df["Internships"],
    df["Placement_Status"]
)

print("\n===== INTERNSHIP VS PLACEMENT =====")
print(internship_placement)

# Internship vs Placement chart

internship_placement.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Internships vs Placement Status")
plt.xlabel("Number of Internships")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.show()

# Save department analysis result

department_cgpa = (
    df.groupby("Department")["CGPA"]
    .mean()
    .round(2)
)

department_cgpa.to_csv(
    "output/department_average_cgpa.csv"
)

print("\nDepartment analysis saved successfully!")

# Save placement analysis result

placement_count = (
    df["Placement_Status"]
    .value_counts()
    .reset_index()
)

placement_count.columns = [
    "Placement_Status",
    "Student_Count"
]

placement_count.to_csv(
    "output/placement_analysis.csv",
    index=False
)

print("\nPlacement analysis saved successfully!")

# Create SQLite database

connection = sqlite3.connect("student_analytics.db")

df.to_sql(
    "students",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("\nDatabase created successfully!")

# Run first SQL query

connection = sqlite3.connect("student_analytics.db")

query = """
SELECT *
FROM students
LIMIT 5;
"""

result = pd.read_sql_query(query, connection)

print("\n===== SQL QUERY RESULT =====")
print(result)

connection.close()

# Department-wise student count using SQL

connection = sqlite3.connect("student_analytics.db")

query = """
SELECT Department, COUNT(*) AS Student_Count
FROM students
GROUP BY Department
ORDER BY Student_Count DESC;
"""

result = pd.read_sql_query(query, connection)

print("\n===== SQL DEPARTMENT ANALYSIS =====")
print(result)

connection.close()

# Department-wise average CGPA using SQL

connection = sqlite3.connect("student_analytics.db")

query = """
SELECT
    Department,
    ROUND(AVG(CGPA), 2) AS Average_CGPA
FROM students
GROUP BY Department
ORDER BY Average_CGPA DESC;
"""

result = pd.read_sql_query(query, connection)

print("\n===== SQL AVERAGE CGPA =====")
print(result)

connection.close()

# Placement analysis using SQL

connection = sqlite3.connect("student_analytics.db")

query = """
SELECT
    Placement_Status,
    COUNT(*) AS Student_Count
FROM students
GROUP BY Placement_Status
ORDER BY Student_Count DESC;
"""

result = pd.read_sql_query(query, connection)

print("\n===== SQL PLACEMENT ANALYSIS =====")
print(result)

connection.close()

# Placement percentage using SQL

connection = sqlite3.connect("student_analytics.db")

query = """
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Placement_Status = 'Placed' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS Placement_Percentage
FROM students;
"""

result = pd.read_sql_query(query, connection)

print("\n===== SQL PLACEMENT PERCENTAGE =====")
print(result)

connection.close()

# Internship vs Placement using SQL

connection = sqlite3.connect("student_analytics.db")

query = """
SELECT
    Internships,
    Placement_Status,
    COUNT(*) AS Student_Count
FROM students
GROUP BY Internships, Placement_Status
ORDER BY Internships, Placement_Status;
"""

result = pd.read_sql_query(query, connection)

print("\n===== SQL INTERNSHIP VS PLACEMENT =====")
print(result)

connection.close()