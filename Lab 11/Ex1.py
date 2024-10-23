# Read in CSV file with sales data, called sales_data.csv, nd print the first 5 rows.
# Need to install Pandas and pyarrow for this to work. 
import pandas as pd 

sales_data = pd.read_csv("./sales_data.csv").convert_dtypes(dtype_backend="pyarrow")

# We ask Pandas to parse he order_date field o turn it into  standard representation. 
sales_data['order_date'] = pd.to_datetime(sales_data["order_date"], format='mixed')

# Set display.max_columns to None, of force display of all columns
pd.set_option("display.max_columns", None)

# Print the first 10 rows 
print(sales_data.head(10))
