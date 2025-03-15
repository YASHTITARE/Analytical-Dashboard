# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11JzQAh4WUHD66vN2GTpYM1ljw85y3b7E
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set Streamlit Page Configuration
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
sections = [
    "1️⃣ Upload File",
    "2️⃣ Understand Data",
    "3️⃣ Data Info",
    "4️⃣ Exploratory Data Analysis (EDA)",
    "5️⃣ Basic Graphs",
    "6️⃣ Correlation Heatmap",
    "7️⃣ Pair Plot",
    "8️⃣ Histogram",
    "9️⃣ Geospatial Analysis"
]
selected_section = st.sidebar.radio("Go to:", sections)

# -------------------- 1️⃣ Upload File --------------------
if selected_section == "1️⃣ Upload File":
    st.title("📂 Upload Dataset")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state["df"] = df  # Save dataset in session state
        st.success("✅ File Uploaded Successfully!")

# -------------------- Load Dataset (Persistent) --------------------
if "df" in st.session_state:
    df = st.session_state["df"]
else:
    df = None

# -------------------- 2️⃣ Understand Data --------------------
if selected_section == "2️⃣ Understand Data" and df is not None:
    st.title("📊 Dataset Overview")
    st.write("### 🔍 Data Preview:")
    st.dataframe(df.head())
    st.write(f"**📊 Shape:** {df.shape[0]} rows, {df.shape[1]} columns")
    st.write("**🔢 Column Data Types:**")
    st.write(df.dtypes)
    st.write("**❗ Missing Values:**")
    st.write(df.isnull().sum())

# -------------------- 3️⃣ Data Info --------------------
if selected_section == "3️⃣ Data Info" and df is not None:
    st.title("📄 Data Information")
    st.write("### 🔍 Summary Statistics:")
    st.write(df.describe())

    st.write("### 🔄 Unique Values per Column:")
    for col in df.columns:
        st.write(f"**{col}:** {df[col].nunique()} unique values")

# -------------------- 4️⃣ Exploratory Data Analysis (EDA) --------------------
if selected_section == "4️⃣ Exploratory Data Analysis (EDA)" and df is not None:
    st.title("🔎 Exploratory Data Analysis")

    # Identify categorical and numerical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()

    # Display column types
    st.write(f"📌 **Categorical Columns:** {categorical_cols}")
    st.write(f"📌 **Numerical Columns:** {numerical_cols}")

# -------------------- 5️⃣ Basic Graphs (Without Dynamic Feature Selection) --------------------
if selected_section == "5️⃣ Basic Graphs" and df is not None:
    st.title("📈 Basic Graphs")

    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()

    # Bar Chart (For Categorical Columns)
    if categorical_cols:
        st.write("### 📊 Bar Chart")
        col = categorical_cols[0]
        fig = px.bar(df[col].value_counts().reset_index(), x="index", y=col, title=f"Bar Chart of {col}")
        st.plotly_chart(fig)

    # Boxplot (For Numerical Columns)
    if numerical_cols:
        st.write("### 📦 Boxplot")
        col = numerical_cols[0]
        fig = px.box(df, y=col, title=f"Boxplot of {col}")
        st.plotly_chart(fig)

# -------------------- 6️⃣ Correlation Heatmap (With Dynamic Feature Selection) --------------------
if selected_section == "6️⃣ Correlation Heatmap" and df is not None:
    st.title("🔥 Correlation Heatmap")

    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    selected_columns = st.multiselect("Select Columns for Correlation Heatmap", numerical_cols, default=numerical_cols[:2])

    if len(selected_columns) > 1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[selected_columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Please select at least two numerical columns!")

# -------------------- 7️⃣ Pair Plot (With Dynamic Feature Selection) --------------------
if selected_section == "7️⃣ Pair Plot" and df is not None:
    st.title("📊 Pair Plot")

    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    selected_columns = st.multiselect("Select Columns for Pair Plot", numerical_cols, default=numerical_cols[:2])

    if len(selected_columns) > 1:
        fig = sns.pairplot(df[selected_columns])
        st.pyplot(fig)
    else:
        st.warning("⚠️ Please select at least two numerical columns!")

# -------------------- 8️⃣ Histogram (With Dynamic Feature Selection) --------------------
if selected_section == "8️⃣ Histogram" and df is not None:
    st.title("📈 Histogram")

    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    column = st.selectbox("Select a Numerical Column", numerical_cols)

    fig = px.histogram(df, x=column, nbins=30, title=f"Distribution of {column}")
    st.plotly_chart(fig)

# -------------------- 9️⃣ Geospatial Analysis --------------------
if selected_section == "9️⃣ Geospatial Analysis" and df is not None:
    st.title("🌍 Geospatial Analysis")

    # Identify potential latitude and longitude columns
    lat_cols = [col for col in df.columns if "lat" in col.lower()]
    lon_cols = [col for col in df.columns if "lon" in col.lower() or "long" in col.lower()]

    if lat_cols and lon_cols:
        lat_col = st.selectbox("Select Latitude Column", lat_cols)
        lon_col = st.selectbox("Select Longitude Column", lon_cols)
        st.map(df[[lat_col, lon_col]].dropna())
    else:
        st.warning("⚠️ No latitude/longitude columns found in the dataset!")