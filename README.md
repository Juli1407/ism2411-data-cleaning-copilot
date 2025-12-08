# ism2411-data-cleaning-copilot
Beginner Sales data cleaning project

This project cleans a raw sales CSV file, getting it ready for analysis by standardizing column names and text, handling missing values in price and quantity, removing invalid rows, and parsing dates into a more understandable format.
The script follows these steps to do so:
  Step 1: load data 
        using pandas, it reads and transforms sales_data_raw.csv into a dataframe using the load_data(file_path) function 
        
  Step 2: Standardize column names, it strips whitespace from column headers, converts them to lowercase, and replaces spaces with underscores (for example, ProdName → prodname, date_sold → date_sold).​

Step 3: Clean text fields, it converts ProdName and Category to string type, and trims leading/trailing spaces and converts values to lowercase so that variants like " electronics " and "Electronics" are treated as the same category.​

Step 4: Handling missing values, it counts missing values in price and qty to report how many entries are affected. Within each product–category group, uses forward and backward fill to infer missing prices or quantities when there are nearby valid values. For any remaining gaps, fills with the overall mean and adds indicator columns (for example, is_price_imputed) so imputed values can be identified later.​

Step 5: Remove invalid rows, it drops rows where price is not positive or qty is negative, since these are clearly invalid for sales data and would distort totals.​

Step 6: Parse dates, it uses pd.to_datetime to convert the date_sold column to a proper datetime type, coercing invalid date strings to missing values (NaT).​

Step 7: Save cleaned data, it writes the cleaned DataFrame to sales_data_clean.csv without the index.

How to run the script
From the project folder, run: data_cleaning.py

The script expects sales_data_raw.csv in the same directory and will create sales_data_clean.csv in the same location. The input and output paths can be modified at the top of data_cleaning.py if needed.

from data_cleaning import clean_sales_data:
df_clean = clean_sales_data("path/to/sales_data_raw.csv")
This will return a cleaned pandas DataFrame that you can use for summaries, visualizations, or modeling.
