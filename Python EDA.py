import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

df = pd.read_excel(r'C:\Users\vk256\Documents\E-commerce Sales Dashboard\Dataset\orders_raw.xlsx')
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.describe())
print("Categories:",df['Category'].unique())
print("\nOrder_Status:",df['Order_Status'].unique())

print("\nPayment Methods:")
print(df["Payment_Method"].unique())

print("\nGender:")
print(df["Gender"].unique())

print("\nStates:")
print(df["State"].unique())

completed_df = df[df['Order_Status'] == 'Delivered'].copy()
print(completed_df.head())
print(completed_df.shape)
print(completed_df['Order_Status'].value_counts())

total_revenue = completed_df['Completed_Revenue'].sum()
print(f"Total Revenue from Completed Orders: ₹{total_revenue:,.2f}")

total_profit = completed_df['Completed_Profit'].sum()
print(f"Total Profit from Completed Orders: ₹{total_profit:,.2f}")

completed_orders = len(completed_df)
print(f"Total Completed Orders: {completed_orders}")

aov = total_revenue / completed_orders
print(f"Average Order Value (AOV): ₹{aov:,.2f}")

category_revenue = completed_df.groupby("Category")["Completed_Revenue"].sum().sort_values(ascending=False)
print(category_revenue.apply(lambda x: f"₹{x:,.2f}"))

plt.figure(figsize=(10,6))
category_revenue.plot(kind='bar', color='skyblue')

plt.title("Completed Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
# Remove scientific notation (1e8)
ax = plt.gca()
ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style='plain', axis='y')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

category_profit = completed_df.groupby("Category")["Completed_Profit"].sum().sort_values(ascending=False)
print(category_profit.apply(lambda x: f"₹{x:,.2f}"))

plt.figure(figsize=(10, 6))
category_profit.plot(kind='bar', color='lightgreen')
plt.title("Completed Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit (₹)")

# Remove scientific notation (1e8)
ax = plt.gca()
ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style="plain", axis="y")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

category_margin = ((category_profit / category_revenue) * 100).sort_values(ascending=False)
print(category_margin.apply(lambda x: f"{x:.2f}%"))

category_comparison = pd.DataFrame({
    "Revenue": category_revenue,
    "Profit": category_profit
})

print(category_comparison.to_string(formatters={
    "Revenue": "₹{:,.2f}".format,
    "Profit": "₹{:,.2f}".format
}))

category_comparison.plot(
    kind="bar",
    figsize=(10, 6)
)
plt.title("Revenue vs Profit by Category")
plt.xlabel("Category")
plt.ylabel("Amount (₹)")

# Remove scientific notation (1e8)
ax = plt.gca()
ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style="plain", axis="y")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

monthly_revenue = (
    completed_df
    .groupby("Order_Month")["Completed_Revenue"]
    .sum()
)

print(monthly_revenue.apply(lambda x: f"₹{x:,.2f}"))

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Completed Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")

ax = plt.gca()
ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style="plain", axis="y")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

status_counts = df["Order_Status"].value_counts()
print(status_counts)

status_percentage = (
    status_counts / status_counts.sum() * 100
).round(2)

print(status_percentage)

plt.figure(figsize=(8, 5))
status_counts.plot(kind="bar")
plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

product_revenue = (
    completed_df
    .groupby("Product Name")["Completed_Revenue"]
    .sum()
    .sort_values(ascending=False)
)
print(product_revenue.head(10).apply(lambda x: f"₹{x:,.2f}"))

top_10_products = product_revenue.head(10)
plt.figure(figsize=(10, 6))
top_10_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Completed Revenue")
plt.xlabel("Revenue (₹)")
plt.ylabel("Product")
ax = plt.gca()
ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style="plain", axis="x")
plt.tight_layout()
plt.show()

state_revenue = (completed_df.groupby("State")["Completed_Revenue"].sum().sort_values(ascending=False))
print(state_revenue.apply(lambda x: f"₹{x:,.2f}"))

plt.figure(figsize=(10, 6))
state_revenue.sort_values().plot(kind="barh")
plt.title("Completed Revenue by State")
plt.xlabel("Revenue (₹)")
plt.ylabel("State")
ax = plt.gca()
ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style="plain", axis="x")
plt.tight_layout()
plt.show()

customer_summary = (
    completed_df
    .groupby("Customer_ID")
    .agg(
        Completed_Orders=("Completed_Order_Flag", "sum"),
        Completed_Revenue=("Completed_Revenue", "sum"),
        Completed_Profit=("Completed_Profit", "sum")
    )
)

print(customer_summary.head())

customer_summary["Customer_Type"] = np.where(
    customer_summary["Completed_Orders"] == 1,
    "One-time",
    "Repeat"
)

print(customer_summary["Customer_Type"].value_counts())

print(customer_summary.shape)
print(customer_summary["Completed_Orders"].value_counts().sort_index())

customer_type_summary = (
    customer_summary
    .groupby("Customer_Type")
    .agg(
        Customers=("Customer_Type", "size"),
        Revenue=("Completed_Revenue", "sum"),
        Profit=("Completed_Profit", "sum")
    )
)

print(customer_type_summary)

total_revenue = customer_type_summary["Revenue"].sum()
total_profit = customer_type_summary["Profit"].sum()

customer_type_summary["Revenue_Contribution_%"] = (
    customer_type_summary["Revenue"] / total_revenue * 100
)

customer_type_summary["Profit_Contribution_%"] = (
    customer_type_summary["Profit"] / total_profit * 100
)

print(
    customer_type_summary[
        [
            "Customers",
            "Revenue",
            "Profit",
            "Revenue_Contribution_%",
            "Profit_Contribution_%"
        ]
    ].round(2)
)

customer_type_summary["Avg_Revenue_per_Customer"] = (
    customer_type_summary["Revenue"] /
    customer_type_summary["Customers"]
)

customer_type_summary["Avg_Profit_per_Customer"] = (
    customer_type_summary["Profit"] /
    customer_type_summary["Customers"]
)

print(
    customer_type_summary[
        [
            "Customers",
            "Avg_Revenue_per_Customer",
            "Avg_Profit_per_Customer"
        ]
    ].round(2)
)

revenue_ratio = (
    customer_type_summary.loc["Repeat", "Avg_Revenue_per_Customer"]
    / customer_type_summary.loc["One-time", "Avg_Revenue_per_Customer"]
)

profit_ratio = (
    customer_type_summary.loc["Repeat", "Avg_Profit_per_Customer"]
    / customer_type_summary.loc["One-time", "Avg_Profit_per_Customer"]
)

print(f"Repeat customer revenue is {revenue_ratio:.2f}x higher")
print(f"Repeat customer profit is {profit_ratio:.2f}x higher")

customer_type_summary["Profit_Margin_%"] = (
    customer_type_summary["Profit"]
    / customer_type_summary["Revenue"]
    * 100
)

print(
    customer_type_summary[
        ["Revenue", "Profit", "Profit_Margin_%"]
    ].round(2)
)

rfm = (
    completed_df
    .groupby("Customer_ID")
    .agg(
        Last_Purchase_Date=("Order_Date", "max"),
        Frequency=("Order_ID", "count"),
        Monetary=("Completed_Revenue", "sum")
    )
)

print(rfm.head(10))

reference_date = completed_df["Order_Date"].max() + pd.Timedelta(days=1)
print(reference_date)

rfm["Recency"] = (
    reference_date - rfm["Last_Purchase_Date"]
).dt.days

print(rfm.head(10))

all_customers = df["Customer_ID"].drop_duplicates()

rfm = (
    all_customers
    .to_frame()
    .merge(rfm, on="Customer_ID", how="left")
)

rfm["Frequency"] = rfm["Frequency"].fillna(0).astype(int)
rfm["Monetary"] = rfm["Monetary"].fillna(0)

print(rfm.shape)
print(rfm.tail())

print(rfm["Frequency"].value_counts().sort_index())

print("Total customers:", rfm["Customer_ID"].nunique())
print("Customers with completed purchase:", (rfm["Frequency"] > 0).sum())
print("Customers with no completed purchase:", (rfm["Frequency"] == 0).sum())

rfm["R_Score"] = np.nan
positive_recency = rfm["Recency"].notna()
rfm.loc[positive_recency, "R_Score"] = pd.qcut(
    rfm.loc[positive_recency, "Recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
)

rfm["R_Score"] = rfm["R_Score"].astype("Int64")

print(rfm[[
    "Customer_ID",
    "Recency",
    "R_Score"
]].head(20))

rfm["F_Score"] = np.nan

positive_frequency = rfm["Frequency"] > 0

rfm.loc[positive_frequency, "F_Score"] = pd.qcut(
    rfm.loc[positive_frequency, "Frequency"],
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop"
)

rfm["F_Score"] = rfm["F_Score"].astype("Int64")

print(rfm[[
    "Customer_ID",
    "Frequency",
    "F_Score"
]].head(20))

rfm["M_Score"] = np.nan

positive_monetary = rfm["Monetary"] > 0

rfm.loc[positive_monetary, "M_Score"] = pd.qcut(
    rfm.loc[positive_monetary, "Monetary"],
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop"
)

rfm["M_Score"] = rfm["M_Score"].astype("Int64")

print(rfm[[
    "Customer_ID",
    "Monetary",
    "M_Score"
]].head(20))

rfm["RFM_Score"] = (
    rfm["R_Score"].astype("string")
    + rfm["F_Score"].astype("string")
    + rfm["M_Score"].astype("string")
)

rfm.loc[
    rfm[["R_Score", "F_Score", "M_Score"]].isna().any(axis=1),
    "RFM_Score"
] = pd.NA

print(rfm[[
    "Customer_ID",
    "R_Score",
    "F_Score",
    "M_Score",
    "RFM_Score"
]].head(20))


rfm["Segment"] = "Others"

rfm.loc[
    (rfm["R_Score"] >= 4) &
    (rfm["F_Score"] >= 4) &
    (rfm["M_Score"] >= 4),
    "Segment"
] = "Champions"

rfm.loc[
    (rfm["R_Score"] >= 3) &
    (rfm["F_Score"] >= 4) &
    (rfm["M_Score"] >= 3) &
    ~(
        (rfm["R_Score"] >= 4) &
        (rfm["F_Score"] >= 4) &
        (rfm["M_Score"] >= 4)
    ),
    "Segment"
] = "Loyal Customers"

rfm.loc[
    (rfm["R_Score"] >= 4) &
    (rfm["F_Score"] <= 3) &
    (rfm["M_Score"] >= 3),
    "Segment"
] = "Potential Loyalists"

rfm.loc[
    (rfm["R_Score"] <= 2) &
    (rfm["F_Score"] >= 3) &
    (rfm["M_Score"] >= 3),
    "Segment"
] = "At Risk"

rfm.loc[
    (rfm["R_Score"] <= 2) &
    (rfm["F_Score"] <= 2) &
    (rfm["M_Score"] <= 2),
    "Segment"
] = "Lost Customers"

rfm.loc[
    rfm[["R_Score", "F_Score", "M_Score"]].isna().any(axis=1),
    "Segment"
] = pd.NA

print(rfm[[
    "Customer_ID",
    "RFM_Score",
    "Segment"
]].head(20))

print(rfm["Segment"].value_counts(dropna=False))

print(rfm["R_Score"].value_counts().sort_index())
print(rfm["F_Score"].value_counts().sort_index())
print(rfm["M_Score"].value_counts().sort_index())

rfm_revenue = (
    rfm.groupby("Segment", dropna=True)["Monetary"]
    .sum()
    .sort_values(ascending=False)
)

print(rfm_revenue.apply(lambda x: f"₹{x:,.2f}"))

rfm_revenue_percentage = ((
    rfm_revenue / rfm_revenue.sum()) * 100
).sort_values(ascending=False)

print(rfm_revenue_percentage.round(2))

rfm_segment_summary = (
    rfm[rfm["Segment"].notna()]
    .groupby("Segment")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Revenue=("Monetary", "sum")
    )
)

rfm_segment_summary["Avg_Revenue_Per_Customer"] = (
    rfm_segment_summary["Total_Revenue"]
    / rfm_segment_summary["Customers"]
)

print(
    rfm_segment_summary
    .sort_values("Avg_Revenue_Per_Customer", ascending=False)
    .round(2)
)

print(rfm.columns)


# Calculate total profit for each customer
customer_profit = (
    completed_df
    .groupby("Customer_ID")["Completed_Profit"]
    .sum()
    .reset_index()
)

# Add customer profit to the RFM table
rfm = rfm.merge(
    customer_profit,
    on="Customer_ID",
    how="left"
)

# Customers without completed purchases have zero profit
rfm["Completed_Profit"] = rfm["Completed_Profit"].fillna(0)

# Summarize profit by customer segment
rfm_profit_summary = (
    rfm[rfm["Segment"].notna()]
    .groupby("Segment")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Profit=("Completed_Profit", "sum")
    )
)

# Calculate average profit per customer
rfm_profit_summary["Avg_Profit_Per_Customer"] = (
    rfm_profit_summary["Total_Profit"]
    / rfm_profit_summary["Customers"]
)

print(
    rfm_profit_summary
    .sort_values("Avg_Profit_Per_Customer", ascending=False)
    .round(2)
)


import matplotlib.pyplot as plt

profit_chart = rfm_profit_summary.sort_values(
    "Avg_Profit_Per_Customer",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    profit_chart.index,
    profit_chart["Avg_Profit_Per_Customer"]
)

plt.title("Average Profit per Customer by RFM Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Average Profit per Customer (₹)")
plt.xticks(rotation=35, ha="right")

plt.tight_layout()
plt.show()


# Keep only completed (Delivered) orders
cohort_df = completed_df.copy()

# Extract the month of each order
cohort_df["Order_Month"] = (
    cohort_df["Order_Date"]
    .dt.to_period("M")
)

# Find each customer's first completed purchase month
cohort_df["Cohort_Month"] = (
    cohort_df.groupby("Customer_ID")["Order_Date"]
    .transform("min")
    .dt.to_period("M")
)

# Display the first five rows
print(
    cohort_df[
        ["Customer_ID", "Order_Date", "Order_Month", "Cohort_Month"]
    ].head()
)


# Calculate the number of months since the first purchase
cohort_df["Cohort_Index"] = (
    (cohort_df["Order_Month"].dt.year
     - cohort_df["Cohort_Month"].dt.year) * 12
    +
    (cohort_df["Order_Month"].dt.month
     - cohort_df["Cohort_Month"].dt.month)
)

# Display the results
print(
    cohort_df[
        ["Customer_ID", "Order_Month", "Cohort_Month", "Cohort_Index"]
    ].head(10)
)


# Count unique purchasing customers for each cohort and cohort index
cohort_counts = (
    cohort_df
    .groupby(["Cohort_Month", "Cohort_Index"])["Customer_ID"]
    .nunique()
    .reset_index(name="Customers")
)

# Convert the counts into a cohort matrix
cohort_table = cohort_counts.pivot(
    index="Cohort_Month",
    columns="Cohort_Index",
    values="Customers"
)

# Display the first five cohorts and first six months
print(cohort_table.iloc[:5, :6])


# Divide each month's customer count by the cohort's Month 0 count
cohort_retention = cohort_table.div(
    cohort_table.iloc[:, 0],
    axis=0
) * 100

# Round percentages to two decimal places
cohort_retention = cohort_retention.round(2)

# Display the first five cohorts and first six months
print(cohort_retention.iloc[:5, :6])


import matplotlib.pyplot as plt

plt.figure(figsize=(16, 9))

plt.imshow(
    cohort_retention,
    aspect="auto",
    cmap="YlGnBu",
    vmin=0,
    vmax=100
)

plt.colorbar(label="Retention Rate (%)")

plt.title("Customer Cohort Retention Analysis")
plt.xlabel("Months Since First Purchase")
plt.ylabel("First Purchase Cohort")

plt.xticks(
    range(len(cohort_retention.columns)),
    cohort_retention.columns
)

plt.yticks(
    range(len(cohort_retention.index)),
    cohort_retention.index.astype(str)
)

plt.tight_layout()
plt.show()

