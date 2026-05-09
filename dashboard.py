# ============================================
# INTERACTIVE SALES DASHBOARD PROJECT
# ============================================

# Import Libraries
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import os

# ============================================
# CREATE VISUALIZATION FOLDER
# ============================================

if not os.path.exists("visualizations"):
    os.makedirs("visualizations")

# ============================================
# LOAD DATASET
# ============================================

df = pd.read_csv("sales_data.csv")

print("Dataset Loaded Successfully!\n")

print(df.head())

# ============================================
# DATASET INFORMATION
# ============================================

print("\nDataset Info:\n")

print(df.info())

print("\nMissing Values:\n")

print(df.isnull().sum())

# ============================================
# DATA CLEANING
# ============================================

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill missing numeric values
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Fill missing categorical values
categorical_cols = df.select_dtypes(include='object').columns

for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# ============================================
# DATE CONVERSION
# ============================================

df['Date'] = pd.to_datetime(df['Date'])

# Create Month Column
df['Month'] = df['Date'].dt.month_name()

# ============================================
# STYLE SETTINGS
# ============================================

sns.set_style("whitegrid")

plt.style.use("ggplot")

# ============================================
# 1. SALES TREND LINE CHART
# ============================================

sales_trend = df.groupby('Date')['Total_Sales'].sum()

plt.figure(figsize=(12,6))

plt.plot(
    sales_trend.index,
    sales_trend.values,
    marker='o'
)

plt.title("Sales Trend Over Time")

plt.xlabel("Date")

plt.ylabel("Total Sales")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("visualizations/sales_trend.png")

plt.show()

# ============================================
# 2. PRODUCT SALES BAR CHART
# ============================================

plt.figure(figsize=(10,6))

sns.barplot(
    x='Product',
    y='Total_Sales',
    data=df
)

plt.title("Sales by Product")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("visualizations/category_sales.png")

plt.show()

# ============================================
# 3. BOX PLOT
# ============================================

plt.figure(figsize=(10,6))

sns.boxplot(
    x='Product',
    y='Total_Sales',
    data=df
)

plt.title("Sales Distribution by Product")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# 4. VIOLIN PLOT
# ============================================

plt.figure(figsize=(10,6))

sns.violinplot(
    x='Product',
    y='Price',
    data=df
)

plt.title("Price Distribution by Product")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# 5. HEATMAP
# ============================================

plt.figure(figsize=(10,8))

correlation = df.select_dtypes(include=np.number).corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm'
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig("visualizations/heatmap.png")

plt.show()

# ============================================
# 6. REGION PIE CHART
# ============================================

region_counts = df['Region'].value_counts()

plt.figure(figsize=(8,8))

plt.pie(
    region_counts,
    labels=region_counts.index,
    autopct='%1.1f%%'
)

plt.title("Region Distribution")

plt.savefig("visualizations/customer_segment.png")

plt.show()

# ============================================
# 7. HISTOGRAM
# ============================================

plt.figure(figsize=(10,6))

sns.histplot(
    df['Total_Sales'],
    kde=True
)

plt.title("Total Sales Distribution")

plt.tight_layout()

plt.show()

# ============================================
# 8. SCATTER PLOT
# ============================================

plt.figure(figsize=(10,6))

sns.scatterplot(
    x='Quantity',
    y='Total_Sales',
    hue='Product',
    data=df
)

plt.title("Quantity vs Total Sales")

plt.tight_layout()

plt.show()

# ============================================
# 9. MULTI-PLOT DASHBOARD
# ============================================

fig, axes = plt.subplots(2,2, figsize=(15,10))

# Histogram
sns.histplot(
    df['Total_Sales'],
    kde=True,
    ax=axes[0,0]
)

axes[0,0].set_title("Sales Distribution")

# Count Plot
sns.countplot(
    x='Product',
    data=df,
    ax=axes[0,1]
)

axes[0,1].set_title("Product Count")

# Scatter Plot
sns.scatterplot(
    x='Quantity',
    y='Total_Sales',
    data=df,
    ax=axes[1,0]
)

axes[1,0].set_title("Quantity vs Sales")

# Box Plot
sns.boxplot(
    x='Product',
    y='Price',
    data=df,
    ax=axes[1,1]
)

axes[1,1].set_title("Price by Product")

plt.tight_layout()

plt.show()

# ============================================
# 10. INTERACTIVE PLOTLY SCATTER CHART
# ============================================

fig1 = px.scatter(
    df,
    x='Quantity',
    y='Total_Sales',
    color='Product',
    hover_data=df.columns,
    title='Interactive Quantity vs Sales'
)

fig1.show()

# ============================================
# 11. INTERACTIVE LINE CHART
# ============================================

daily_sales = df.groupby('Date')['Total_Sales'].sum().reset_index()

fig2 = px.line(
    daily_sales,
    x='Date',
    y='Total_Sales',
    title='Interactive Sales Trend'
)

fig2.show()

# ============================================
# 12. PROFESSIONAL DASHBOARD
# ============================================

fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        'Sales Trend',
        'Sales by Product',
        'Price Distribution',
        'Quantity vs Sales'
    )
)

# Sales Trend
fig.add_trace(
    go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Total_Sales'],
        mode='lines+markers',
        name='Sales Trend'
    ),
    row=1,
    col=1
)

# Product Sales
product_sales = df.groupby('Product')['Total_Sales'].sum().reset_index()

fig.add_trace(
    go.Bar(
        x=product_sales['Product'],
        y=product_sales['Total_Sales'],
        name='Product Sales'
    ),
    row=1,
    col=2
)

# Price Histogram
fig.add_trace(
    go.Histogram(
        x=df['Price'],
        name='Price Distribution'
    ),
    row=2,
    col=1
)

# Scatter Plot
fig.add_trace(
    go.Scatter(
        x=df['Quantity'],
        y=df['Total_Sales'],
        mode='markers',
        name='Quantity vs Sales'
    ),
    row=2,
    col=2
)

fig.update_layout(
    title='Interactive Sales Dashboard',
    height=800,
    width=1200,
    showlegend=True
)

# Save Interactive Dashboard
fig.write_html(
    "visualizations/interactive_dashboard.html"
)

fig.show()

# ============================================
# BUSINESS INSIGHTS
# ============================================

print("\n===== BUSINESS INSIGHTS =====")

# Total Sales
print("Total Sales:", df['Total_Sales'].sum())

# Average Sales
print("Average Sales:", df['Total_Sales'].mean())

# Best Product
best_product = df.groupby('Product')['Total_Sales'].sum().idxmax()

print("Best Performing Product:", best_product)

# Best Region
best_region = df.groupby('Region')['Total_Sales'].sum().idxmax()

print("Best Performing Region:", best_region)

print("\nDashboard Created Successfully!")

