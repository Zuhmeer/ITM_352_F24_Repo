# Read a file from a URL and write a local file "sales_data_test.csv"
# containing just the first 10 rows of data 
import pandas as pd 
import pyarrow # NOT NEEDED HERE 
import ssl 
import time 

ssl._create_default_https_context = ssl._create_unverified_context 
#pd.set_option("display.max_columns", None)

# Import the data file. This needs to be downloaded to be used by pandas. It is in CSV format. 
# It is in CSV format 
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA" 

def load_csv(file_path):
    # Attempt to read the CSV file 
    try:
        print("Reading CSV file...")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip") 
        load_time = start_time - time.time()
        print(f"File loaded in {load_time} seconds")
        print(f"The number of rows is {len(sales_data)}")
        print(f"Columns: {sales_data.columns.to_list()}")

        # List the required columns 
        required_columns = ['quantity', 'order_date', 'unit_price']

        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in sales_data.columns]
    
        if missing_columns:
            print("\nWarning: The following required columns are missing: {missing_columns}")
        else:
            print(f"\nAll required columns are present")
       
        # Ask pandas to prse the order_date field into a standard representation
        sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], format="mixed")

        # Save the first 10 rows of the data in the sales_data_test.csv
        sales_data.head(10).to_csv('sales_data_test.csv') 
    
    except Exception as e:
        print(f"An error has occurred: {e}") 


# Call load_csv to load the file 
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
#local_file = "sales_data_test.csv"
#load_csv(local_file)