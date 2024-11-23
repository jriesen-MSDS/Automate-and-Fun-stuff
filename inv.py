import polars as pl
import glob

# Path to the folder containing invoice files
invoices_folder = "invoices"

# Use glob to get a list of all CSV files in the "invoices" folder and sort them
invoice_files = sorted(glob.glob(f"{invoices_folder}/*.csv"))

# Initialize an empty DataFrame to store all invoice data
all_data = pl.DataFrame()

# Loop through each invoice file and concatenate the data
for file in invoice_files:
    # Read the CSV file into a Polars DataFrame
    df = pl.read_csv(file)

    # Concatenate the data to the all_data DataFrame
    all_data = pl.concat([all_data, df])

# Step 1: Calculate total sum of prices and number of invoices across all files
total_sum = all_data['Total Price'].sum()
invoice_count = all_data.height

# Print out the overall totals
print(f"Total number of invoices: {invoice_count}")
print(f"Total sum of all prices: ${total_sum:.2f}")
print("-" * 30)

# Step 2: Generate a summary report for each customer
customer_report = (
    all_data
    .group_by('Customer Name')
    .agg([
        pl.sum('Total Price').alias('Total Amount Spent'),
        pl.count('Invoice Number').alias('Number of Purchases')
    ])
    .sort('Total Amount Spent', descending=True)  # Sort by total amount spent
)

# Print out the customer report
print(customer_report)

# Step 3: Save the summary report to a CSV file
customer_report.write_csv("summary_report.csv")
print("Summary report saved to 'summary_report.csv'.")
