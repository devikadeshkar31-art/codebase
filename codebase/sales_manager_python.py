"""
E-Commerce Sales Analyzer
Project: Programming Fundamentals and Logic Building Using Python

CSV columns:
Order_ID, Product, Category, Quantity, Price
Revenue for each row = Quantity * Price
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = Path(__file__).with_name("orders.csv")


def load_sales_data(file_path):
    """Read the CSV file, validate rows, and calculate revenue."""
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found: {file_path}")
        return pd.DataFrame()
    except Exception as error:
        print("Error reading CSV file:", error)
        return pd.DataFrame()

    required_columns = ["Order_ID", "Product", "Category", "Quantity", "Price"]
    missing = [column for column in required_columns if column not in data.columns]

    if missing:
        print("Invalid CSV. Missing column(s):", ", ".join(missing))
        return pd.DataFrame()

    # Convert numeric columns. Invalid text becomes NaN and is skipped.
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["Price"] = pd.to_numeric(data["Price"], errors="coerce")

    valid = (
        data["Order_ID"].notna()
        & data["Product"].notna()
        & data["Category"].notna()
        & data["Quantity"].notna()
        & data["Price"].notna()
        & (data["Quantity"] > 0)
        & (data["Price"] > 0)
    )

    invalid_count = int((~valid).sum())
    if invalid_count:
        print(f"\n{invalid_count} invalid row(s) skipped.")

    data = data.loc[valid].copy()
    data["Product"] = data["Product"].astype(str).str.strip()
    data["Category"] = data["Category"].astype(str).str.strip()
    data["Revenue"] = data["Quantity"] * data["Price"]

    # Remove rows where names are blank after trimming.
    data = data[
        (data["Product"] != "")
        & (data["Category"] != "")
        & (data["Order_ID"].astype(str).str.strip() != "")
    ]
    return data


def show_summary(data):
    """Display total revenue, orders, units, and top-selling product."""
    if data.empty:
        print("\nNo valid sales data available.")
        return

    total_revenue = data["Revenue"].sum()
    total_orders = data["Order_ID"].nunique()
    total_units = int(data["Quantity"].sum())
    product_revenue = data.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

    print("\n========== SALES SUMMARY ==========")
    print(f"Total Revenue: {total_revenue:g}")
    print(f"Orders: {total_orders}")
    print(f"Units sold: {total_units}")

    if not product_revenue.empty:
        top_product = product_revenue.index[0]
        top_revenue = product_revenue.iloc[0]
        print(f"Top product: {top_product} ({top_revenue:g})")

    print("\nTop 5 products by revenue:")
    print(product_revenue.head(5).to_string())


def show_category_revenue(data):
    """Display revenue earned by each category and show a pie chart."""
    if data.empty:
        print("\nNo valid sales data available.")
        return

    category_revenue = data.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    total = category_revenue.sum()

    print("\n======= CATEGORY-WISE REVENUE =======")
    for category, revenue in category_revenue.items():
        percentage = (revenue / total * 100) if total else 0
        print(f"{category}: {revenue:g} ({percentage:.2f}%)")

    # Pie chart
    plt.figure(figsize=(7, 6))
    plt.pie(
        category_revenue.values,
        labels=category_revenue.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Category-wise Revenue")
    plt.tight_layout()
    plt.show()


def show_top_products(data):
    """Display the five products with the highest revenue."""
    if data.empty:
        print("\nNo valid sales data available.")
        return

    top_products = (
        data.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    print("\n======= TOP 5 PRODUCTS BY REVENUE =======")
    print(top_products.to_string())


def show_charts(data):
    """Display a bar chart of product revenue and a pie chart of category revenue."""
    if data.empty:
        print("\nNo valid sales data available.")
        return

    product_revenue = (
        data.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    category_revenue = data.groupby("Category")["Revenue"].sum()

    # Bar chart
    plt.figure(figsize=(8, 5))
    product_revenue.plot(kind="bar")
    plt.title("Top 5 Products by Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Pie chart
    plt.figure(figsize=(7, 6))
    plt.pie(
        category_revenue.values,
        labels=category_revenue.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Category-wise Revenue")
    plt.tight_layout()
    plt.show()


def main():
    print("===================================")
    print("       E-COMMERCE SALES ANALYZER")
    print("===================================")

    sales_data = load_sales_data(CSV_FILE)
    if sales_data.empty:
        print("Please check orders.csv and add valid sales records.")
        return

    while True:
        print("\n--------------- MENU ---------------")
        print("1. Sales Summary")
        print("2. Category-wise Revenue")
        print("3. Top 5 Best-selling Products")
        print("4. Display Bar and Pie Charts")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            show_summary(sales_data)
        elif choice == "2":
            show_category_revenue(sales_data)
        elif choice == "3":
            show_top_products(sales_data)
        elif choice == "4":
            show_charts(sales_data)
        elif choice == "5":
            print("Thank you for using E-Commerce Sales Analyzer!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
