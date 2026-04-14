import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Play Store Dashboard", layout="wide")

# Title
st.title("📊 Google Play Store Market Intelligence Dashboard")
st.markdown("Analyze app performance using installs, ratings, reviews and categories 🚀")

# =========================
# LOAD DATA (safe version)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("googleplaystore.csv")  # make sure file is in repo

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Clean Installs
    df['Installs'] = df['Installs'].astype(str).str.replace('+','', regex=False)
    df['Installs'] = df['Installs'].str.replace(',','', regex=False)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    # Clean Price
    df['Price'] = df['Price'].astype(str).str.replace('$','', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Reviews
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    # Rating
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Drop missing values
    df.dropna(inplace=True)

    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

category = st.sidebar.selectbox("Select Category", ["All"] + list(df["Category"].unique()))

if category != "All":
    df = df[df["Category"] == category]

# =========================
# KPI SECTION
# =========================
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Apps", len(df))
col2.metric("Avg Rating", round(df["Rating"].mean(), 2))
col3.metric("Total Installs", int(df["Installs"].sum()))
col4.metric("Avg Reviews", int(df["Reviews"].mean()))

# =========================
# DATA PREVIEW
# =========================
st.subheader("📋 Dataset Preview")
st.dataframe(df.head())

# =========================
# TOP CATEGORIES
# =========================
st.subheader("🏆 Top Categories by Installs")

top_cat = df.groupby("Category")["Installs"].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots()
ax1.barh(top_cat.index, top_cat.values)
ax1.set_xlabel("Installs")
ax1.set_ylabel("Category")
st.pyplot(fig1)

# =========================
# RATING DISTRIBUTION
# =========================
st.subheader("⭐ Rating Distribution")

fig2, ax2 = plt.subplots()
ax2.hist(df["Rating"], bins=20)
st.pyplot(fig2)

# =========================
# REVIEWS VS INSTALLS
# =========================
st.subheader("📈 Reviews vs Installs")

fig3, ax3 = plt.subplots()
ax3.scatter(df["Reviews"], df["Installs"])
ax3.set_xlabel("Reviews")
ax3.set_ylabel("Installs")
st.pyplot(fig3)

# =========================
# FREE VS PAID
# =========================
st.subheader("💰 Free vs Paid Apps")

type_count = df["Type"].value_counts()

fig4, ax4 = plt.subplots()
ax4.pie(type_count.values, labels=type_count.index, autopct="%1.1f%%")
st.pyplot(fig4)

# =========================
# INSIGHTS
# =========================
st.subheader("🧠 Key Insights")

st.success("""
✔ Game and Communication apps usually dominate installs  
✔ Higher reviews often lead to higher installs  
✔ Free apps dominate the market  
✔ Ratings impact app success significantly  
""")

# Footer
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Data Analytics Project by Shafiq")
