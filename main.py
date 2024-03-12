from config import (
    LOAN_INTEREST_PERCENT,
    DOWN_PAYMENT_PERCENT,
    PROPERTY_MGMT_PERCENT,
    VACANCY_PERCENT,
    MAINTENANCE_PERCENT,
    CAPEX_PERCENT,
    INSURANCE_PERCENT,
    PROPERTY_TAX_PERCENT,
    RAPID_API_HOST,
    RAPID_API_KEY
)
import traceback
import pandas as pd
import os
from datetime import datetime

from data.api import fetch_house_listings
from analysis.calculations import calculate_expenses, calculate_lending, cash_to_close, calculate_returns
# from analysis.visualizations import plot_cash_on_cash_return, plot_monthly_cash_flow

def main():
    # Set up search parameters
    location = "Oakland County, MI"
    status = "forSale"
    singlefamily=True

    try:
        # Fetch house listings fr om the Zillow API
        house_listings = fetch_house_listings(
            location,
            status,
            singlefamily,
            RAPID_API_KEY=RAPID_API_KEY,
            RAPID_API_HOST=RAPID_API_HOST
        )

        df = pd.DataFrame(house_listings)
        # Convert the 'price' column to numeric
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        print(df.head())

        # Calculate expenses for each listing
        expenses_df = df.apply(calculate_expenses, axis=1)

        # Concatenate the expenses DataFrame with the original DataFrame
        df = pd.concat([df, expenses_df], axis=1)
        print(df.head())

        # Calculate lending details for each listing
        lending_df = df.apply(calculate_lending, axis=1)

        # Concatenate the lending DataFrame with the existing DataFrame
        df = pd.concat([df, lending_df], axis=1)
        print(df.head())

        # Calculate cash to close for each listing
        cashtoclose_df = df.apply(cash_to_close, axis=1)

        # Concatenate the cash to close DataFrame with the existing DataFrame
        df = pd.concat([df, cashtoclose_df], axis=1)
        print(df.head())
        
        # Calculate returns for each listing
        returns_df = df.apply(calculate_returns, axis=1)

        # Concatenate the returns DataFrame with the existing DataFrame
        df = pd.concat([df, returns_df], axis=1)
        
        # Create the directory if it doesn't exist
        directory = "data/datasets/processed"
        os.makedirs(directory, exist_ok=True)

        # Save the final DataFrame as a JSON file
        
        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Generate the filename with the current date
        filename = f"house_listings_processed_{current_date}.json"
        filepath = os.path.join(directory, filename)
        
        df.to_json(filepath, orient="records")

        print("Calculations Complete")
        
        # Select the main data for each house
        main_data = df[['streetAddress', 'Cash on Cash Return %', 'Monthly Cash Flow', 'Cap Rate', 'Down Payment', 'Loan Amount']]

        # Convert the relevant columns to appropriate data types
        main_data['Cash on Cash Return %'] = main_data['Cash on Cash Return %'].astype(float)
        main_data['Monthly Cash Flow'] = main_data['Monthly Cash Flow'].astype(float)
        main_data['Cap Rate'] = main_data['Cap Rate'].astype(float)
        main_data['Down Payment'] = main_data['Down Payment'].astype(float)
        main_data['Loan Amount'] = main_data['Loan Amount'].astype(float)

        # Calculate the Cash to Close
        main_data.loc[:, 'Cash to Close'] = main_data['Down Payment'] + main_data['Loan Amount']

        # Rename the columns for better readability
        main_data.columns = ['Address', 'CoC', 'Monthly Cash Flow', 'Cap Rate', 'Down Payment', 'Loan Amount', 'Cash to Close']

        # Format the data for display
        main_data.loc[:, 'CoC'] = main_data['CoC'].apply(lambda x: f"{x:.2f}%")
        main_data.loc[:, 'Monthly Cash Flow'] = main_data['Monthly Cash Flow'].apply(lambda x: f"${x:,.0f}")
        main_data.loc[:, 'Cap Rate'] = main_data['Cap Rate'].apply(lambda x: f"{x:.2%}")
        main_data.loc[:, 'Down Payment'] = main_data['Down Payment'].apply(lambda x: f"${x:,.0f}")
        main_data.loc[:, 'Loan Amount'] = main_data['Loan Amount'].apply(lambda x: f"${x:,.0f}")
        main_data.loc[:, 'Cash to Close'] = main_data['Cash to Close'].apply(lambda x: f"${x:,.0f}")

        # Select the desired columns for display
        main_data = main_data[['Address', 'CoC', 'Monthly Cash Flow', 'Cap Rate', 'Cash to Close']]

        # Display the main data in a table format
        print("House Analysis Summary:")
        print("----------------------")
        print(main_data.to_string(index=False))


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()