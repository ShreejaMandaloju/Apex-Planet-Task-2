# EDA + SQL Business Analysis

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Dataset
df = pd.read_csv("data.csv")

# Create Revenue Column
df["revenue"] = df["price"] * df["quantity"]

print("\nFirst 5 Rows:")
print(df.head())

print("\nSummary Statistics:")
print(df.describe())

# 2. Create SQLite Database
conn = sqlite3.connect("database.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

# 3. SQL QUERIES

# 1 - Top Products by Revenue
query1 = """
SELECT product,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;
"""
print("\nTop Products by Revenue:")
print(pd.read_sql_query(query1, conn))


# 2 - Revenue by Category
query2 = """
SELECT category,
    SUM(revenue) AS category_revenue
FROM sales
GROUP BY category
ORDER BY category_revenue DESC;
"""
print("\nRevenue by Category:")
print(pd.read_sql_query(query2, conn))


# 3 - Monthly Revenue
query3 = """
SELECT strftime('%Y-%m', order_date) AS month,
    SUM(revenue) AS monthly_revenue
FROM sales
GROUP BY month
ORDER BY month;
"""
print("\nMonthly Revenue:")
print(pd.read_sql_query(query3, conn))


# 4 - Total Business Revenue
query4 = """
SELECT SUM(revenue) AS total_business_revenue
FROM sales;
"""
print("\nTotal Business Revenue:")
print(pd.read_sql_query(query4, conn))


# 5 - Top Customers
query5 = """
SELECT customer_id,
    SUM(revenue) AS customer_revenue
FROM sales
GROUP BY customer_id
ORDER BY customer_revenue DESC
LIMIT 5;
"""
print("\nTop Customers:")
print(pd.read_sql_query(query5, conn))


# 4. VISUALIZATIONS

# Revenue by Product
plt.figure(figsize=(6,4))
sns.barplot(x="product", y="revenue", data=df)
plt.title("Revenue by Product")
plt.tight_layout()
plt.savefig("revenue_by_product.png")
plt.close()


# Revenue by Category
plt.figure(figsize=(6,4))
sns.barplot(x="category", y="revenue", data=df)
plt.title("Revenue by Category")
plt.tight_layout()
plt.savefig("revenue_by_category.png")
plt.close()


# Marketing Spend vs Revenue
plt.figure(figsize=(6,4))
sns.scatterplot(x="marketing_spend", y="revenue", data=df)
plt.title("Marketing Spend vs Revenue")
plt.tight_layout()
plt.savefig("marketing_vs_revenue.png")
plt.close()


# 5. Close Database
conn.close()

print("\nAnalysis Complete !")
print("Charts saved in project folder.")