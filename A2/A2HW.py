import pandas as pd
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context

# Import the data file. This needs to be downloaded to be used by pandas.
# It is in CSV format 
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"

# Load and prepare data function
def load_csv(file_path):
    # Attempt to read the CSV file
    try:
        print("Reading CSV file...")
        start_time = time.time()
        
        # Load the data 
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip")
        load_time = time.time() - start_time
        print(f"File loaded in {load_time:.2f} seconds")
        print(f"The number of rows is {len(sales_data)}")
        print(f"Columns: {sales_data.columns.to_list()}")

        # List and check required columns
        required_columns = ['quantity', 'order_date', 'unit_price']
        missing_columns = [col for col in required_columns if col not in sales_data.columns]

        if missing_columns:
            print(f"\nWarning: The following required columns are missing: {missing_columns}")
            print("Some analytics may not work as expected due to missing fields.")
        else:
            print("\nAll required columns are present")

        # Parse 'order_date' field
        sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], format="mixed", errors='coerce')

        return sales_data
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")

        # Save the first 10 rows to a local CSV file
        sales_data.head(10).to_csv('sales_data_test.csv')
        
        return sales_data

    except FileNotFoundError:
        print("Error: File not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was an issue with parsing the file.")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")

# Display rows function
def display_rows(data):
    while True:
        numRows = len(data) - 1
        print("\nEnter number of rows to display:")
        print(f"- Enter a number between 1 and {numRows}")
        print("- To see all rows enter 'all'")
        print("- To skip, press Enter")
        user_choice = input("Your choice: ").strip().lower()

        if user_choice == '':
            print("Skipping preview")
            break
        elif user_choice == 'all':
            print(data)
            break
        elif user_choice.isdigit() and 1 <= int(user_choice) <= numRows:
            print(data.head(int(user_choice)))
            break
        else:
            print("Invalid input. Please re-enter.")

# Create a menu option that shows total sales by region and order type
def total_sales_by_region_order_type(data):
    result = data.groupby(['sales_region', 'order_type'])['quantity'].sum()
    print("\nTotal Sales by Region and Order Type:")
    print(result)
    

# Create a menu option that shows average sales by region with average by state and sale type
def average_sales_by_region_state_sale_type(data):
    result = data.groupby(['sales_region', 'customer_state', 'order_type'])['unit_price'].mean()
    print("\nAverage Sales by Region, State, and Sale Type:")
    print(result)

# Create a menu option that shows sales by customer type and order type by state
def sales_by_customer_type_order_type_by_state(data):
    
    result = data.groupby(['customer_type', 'order_type', 'customer_state'])['unit_price'].sum() 
    print("\nSales by customer type and order type by state:")                                 
    print(result)

# Create a menu option that shows total sales quantity and price by region and product
def total_sales_quantity_price_by_region_product(data):
    result = data.groupby(['sales_region', 'product_category'])[['quantity', 'unit_price']].sum()
    print("\nTotal Sales Quantity and Price by Region and Product:")
    print(result)

# Create a menu option that shows total sales quantity and price by customer type
def total_sales_quantity_price_by_customer_type(data):
    result = data.groupby('customer_type')[['quantity', 'unit_price']].sum()
    print("\nTotal Sales Quantity and Price by Customer Type:")
    print(result)

# Create a menu option that shows max and min Sales Price of Sales by Category
def max_min_sales_price_by_category(data):
    result = data.groupby('product_category')['unit_price'].agg(['max', 'min'])
    print("\nMax and Min Sales Price by Category:")
    print(result)

# Create a menu option that shows unique employees by region
def employees_by_region(data):
    unique_employees = data.groupby('sales_region')['employee_id'].nunique()
    print("\nNumber of Unique Employees by Region:")
    print(unique_employees)

# Display menu that interacts with user
def display_menu(data):
    menu_options = (
        ("Show the first n rows of data", display_rows),
        ("Total sales by region and order type", total_sales_by_region_order_type),
        ("Average sales by region with average sales by state and sale type", average_sales_by_region_state_sale_type),
        ("Sales by customer type and order type by state", sales_by_customer_type_order_type_by_state),
        ("Total sales quantity and price by region and product", total_sales_quantity_price_by_region_product),
        ("Total sales quantity and price by customer type", total_sales_quantity_price_by_customer_type),
        ("Max and Min Sales Price by Category", max_min_sales_price_by_category),
        ("Number of unique employees by region", employees_by_region),
        ("Exit the program", exit_program)
    )

    print("\n Sales Data Dashboard ")
    print("Please choose from these options:")
    
    for index, (description, _) in enumerate(menu_options):
        print(f"{index + 1}: {description}")

    num_choices = len(menu_options)
    choice = int(input(f"Select an option between 1 and {num_choices}: "))

    if 1 <= choice <= num_choices:
        action = menu_options[choice - 1][1]
        action(data)
    else:
        print("Invalid input. Please re-enter.")

# Exit the program
def exit_program(data):
    sys.exit(0)

# Load and read the CSV file
def load_csv(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Print the first n rows of sales data
def display_rows(data):
    n = int(input("Enter the number of rows to display: "))
    print(data.head(n))

# Print the total sales by region and order_type
def total_sales_by_region_order_type(data):
    pivot_table = pd.pivot_table(data, index="sales_region", columns="order_type", values="quantity", aggfunc="sum", fill_value=0)
    print("\nTotal Sales by Region and Order Type:")
    print(pivot_table)
    return pivot_table

# Print the average sales by region with average sales by state and sale type
def average_sales_by_region_state_sale_type(data):
    pivot_table = pd.pivot_table(data, index=["sales_region", "customer_state"], columns="order_type", values="unit_price", aggfunc="mean", fill_value=0)
    print("\nAverage Sales by Region, State, and Sale Type:")
    print(pivot_table)
    return pivot_table

# Print the sales by customer type and order type by state
def sales_by_customer_type_order_type_by_state(data):
    pivot_table = pd.pivot_table(data, index=["customer_type", "customer_state"], columns="order_type", values="unit_price", aggfunc="sum", fill_value=0)
    print("\nSales by Customer Type and Order Type by State:")
    print(pivot_table)
    return pivot_table

# Print the sales by customer type and order type by state
def sales_by_customer_type_order_type_by_state(data):
    pivot_table = pd.pivot_table(data, index=["customer_type", "customer_state"], columns="order_type", values="unit_price", aggfunc="sum", fill_value=0)
    print("\nSales by Customer Type and Order Type by State:")
    print(pivot_table)
    return pivot_table

# Print the total sales quantity and price by region and product
def total_sales_quantity_price_by_region_product(data):
    pivot_table = pd.pivot_table(data, index=["sales_region", "product_category"], values=["quantity", "unit_price"], aggfunc="sum", fill_value=0)
    print("\nTotal Sales Quantity and Price by Region and Product:")
    print(pivot_table)
    return pivot_table

# Print the total sales quantity and price by customer type
def total_sales_quantity_price_by_customer_type(data):
    pivot_table = pd.pivot_table(data, index="customer_type", values=["quantity", "unit_price"], aggfunc="sum", fill_value=0)
    print("\nTotal Sales Quantity and Price by Customer Type:")
    print(pivot_table)
    return pivot_table

# Print the max and min sales price of sales by category
def max_min_sales_price_by_category(data):
    pivot_table = pd.pivot_table(data, index="product_category", values="unit_price", aggfunc=[max, min], fill_value=0)
    print("\nMax and Min Sales Price by Category:")
    print(pivot_table)
    return pivot_table

# Print the number of unique employees per region
def employees_by_region(data):
    pivot_table = pd.pivot_table(data, index="sales_region", values="employee_id", aggfunc=pd.Series.nunique)
    print("\nNumber of Employees by Region")
    pivot_table.columns = ['Number of Employees']  
    print(pivot_table)
    return pivot_table

# Custom pivot table
def custom_pivot_table(data):
    print("Create a Custom Pivot Table:")
    try:
        # Prompt the user for an input then split by comma.
        # I use AI to help me with this part of making the pivot table, It helped me use .split to split the input by commas
        index = list(filter(None, input("Enter the column name(s) for the index (use a comma to separate multiple columns): ").split(",")))
        columns = list(filter(None, input("Enter the column name(s) for the columns (use a comma to separate multiple columns): ").split(",")))
        values = list(filter(None, input("Enter the column name(s) for the values (use a comma to separate multiple columns): ").split(",")))
        

        # Create and display the pivot table
        pivot_table = pd.pivot_table(data, index=index, columns=columns, values=values, aggfunc="sum", fill_value=0)
        print("\nCustom Pivot Table:")
        print(pivot_table)
        return pivot_table
    except Exception as e:
        print(f"Error creating pivot table: {e}")

# Display the menu
def display_menu(data):
    while True:
        print("\nSales Data Analysis Menu:")
        print("1. Show the first n rows of sales data")
        print("2. Total sales by region and order_type")
        print("3. Average sales by region with average sales by state and sale type")
        print("4. Sales by customer type and order type by state")
        print("5. Total sales quantity and price by region and product")
        print("6. Total sales quantity and price by customer type")
        print("7. Max and min sales price of sales by category")
        print("8. Number of unique employees by region")
        print("9. Create Custom Pivot Table") 
        print("0. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_rows(data)
        elif choice == '2':
            total_sales_by_region_order_type(data)
        elif choice == '3':
            average_sales_by_region_state_sale_type(data)
        elif choice == '4':
            sales_by_customer_type_order_type_by_state(data)
        elif choice == '5':
            total_sales_quantity_price_by_region_product(data)
        elif choice == '6':
            total_sales_quantity_price_by_customer_type(data)
        elif choice == '7':
            max_min_sales_price_by_category(data)
        elif choice == '8':
            employees_by_region(data)
        elif choice == '9':
            custom_pivot_table(data)  
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Load the data and start the interactive menu
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA" 
sales_data = load_csv(url)
if sales_data is not None:
    display_menu(sales_data)
