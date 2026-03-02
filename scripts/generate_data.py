import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)

# -------------------
# CONFIG
# -------------------
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 200
NUM_SALES_REPS = 25
NUM_REGIONS = 5
NUM_SALES = 10000

# -------------------
# REGIONS
# -------------------
regions = pd.DataFrame({
    "region_id": range(1, NUM_REGIONS + 1),
    "region_name": ["North America", "Europe", "Asia", "Middle East", "Africa"]
})

# -------------------
# CUSTOMERS
# -------------------
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append([
        i,
        fake.company(),
        random.choice(["Technology", "Finance", "Healthcare", "Retail"]),
        random.choice(["Gold", "Silver", "Bronze"]),
        fake.country(),
        fake.city(),
        fake.date_between(start_date="-5y", end_date="today")
    ])

customers = pd.DataFrame(customers, columns=[
    "customer_id", "company_name", "industry",
    "customer_tier", "country", "city", "join_date"
])

# -------------------
# PRODUCTS
# -------------------
products = []
categories = ["Laptops", "Servers", "Networking", "Accessories"]

for i in range(1, NUM_PRODUCTS + 1):
    cost = round(random.uniform(50, 2000), 2)
    products.append([
        i,
        f"Product_{i}",
        random.choice(categories),
        cost,
        fake.date_between(start_date="-3y", end_date="today")
    ])

products = pd.DataFrame(products, columns=[
    "product_id", "product_name", "category",
    "unit_cost", "launch_date"
])

# -------------------
# SALES REPS
# -------------------
sales_reps = []
for i in range(1, NUM_SALES_REPS + 1):
    sales_reps.append([
        i,
        fake.name(),
        fake.date_between(start_date="-5y", end_date="today"),
        random.randint(1, NUM_REGIONS),
        random.randint(50000, 150000)
    ])

sales_reps = pd.DataFrame(sales_reps, columns=[
    "sales_rep_id", "rep_name",
    "hire_date", "region_id", "monthly_quota"
])

# -------------------
# SALES FACT TABLE
# -------------------
sales = []
start_date = datetime.now() - timedelta(days=730)

for i in range(1, NUM_SALES + 1):
    product = products.sample(1).iloc[0]
    quantity = random.randint(1, 20)
    unit_price = round(product["unit_cost"] * random.uniform(1.1, 1.5), 2)
    total_revenue = quantity * unit_price
    total_cost = quantity * product["unit_cost"]
    profit = total_revenue - total_cost

    sales.append([
        i,
        start_date + timedelta(days=random.randint(0, 730)),
        random.randint(1, NUM_CUSTOMERS),
        product["product_id"],
        random.randint(1, NUM_SALES_REPS),
        random.randint(1, NUM_REGIONS),
        quantity,
        unit_price,
        round(random.uniform(0, 0.2), 2),
        round(total_revenue, 2),
        round(total_cost, 2),
        round(profit, 2)
    ])

sales = pd.DataFrame(sales, columns=[
    "sales_id", "order_date", "customer_id",
    "product_id", "sales_rep_id", "region_id",
    "quantity", "unit_price", "discount",
    "total_revenue", "total_cost", "profit"
])

# -------------------
# SAVE CSV FILES
# -------------------
customers.to_csv("data/raw/dim_customer.csv", index=False)
products.to_csv("data/raw/dim_product.csv", index=False)
sales_reps.to_csv("data/raw/dim_sales_rep.csv", index=False)
regions.to_csv("data/raw/dim_region.csv", index=False)
sales.to_csv("data/raw/fact_sales.csv", index=False)

print("Dataset generated successfully!")
