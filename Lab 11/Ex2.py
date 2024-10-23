# Read in CSV file with sales data, called sales_data.csv, nd print the first 5 rows.
# create a pivot table, aggregating sales by region, with columns defined by order_type (which is 
# either Retail or Wholesale).
import pandas as pd 

sales_data = pd.read_csv("./sales_data.csv").convert_dtypes(dtype_backend="pyarrow")

# We ask Pandas to parse he order_date field o turn it into  standard representation. 
sales_data['order_date'] = pd.to_datetime(sales_data["order_date"], format='mixed')

# create a pivot table 
pivot = sales_data.pivot_table(
    values = "sale_price", index='customer_state',
columns = ['customer_type','order_type'],
    aggfunc= 'mean'
)

# Set display.max_columns to None, of force display of all columns
pd.set_option("display.max_columns", None)

# Print the first 5 rows 
print(sales_data.head(5))
print("\nPivot Table:\n", pivot)

