import pandas as pd
import numpy as np
import numpy_financial as npf

from config import (
    PROPERTY_MGMT_PERCENT,
    MAINTENANCE_PERCENT,
    CAPEX_PERCENT,
    INSURANCE_PERCENT,
    PROPERTY_TAX_PERCENT,
    VACANCY_PERCENT,
    DOWN_PAYMENT_PERCENT,
    LOAN_INTEREST_PERCENT,
    LOAN_TERM_YEARS,
    CLOSING_COSTS_PERCENT,
)

def calculate_expenses(row):
    # Extract the necessary information from the row
    price = row['price']
    rent = row['rentZestimate']

    # Calculate individual expense categories
    property_mgmt = rent * PROPERTY_MGMT_PERCENT
    vacancy = rent * VACANCY_PERCENT
    maintenance_repairs = rent * MAINTENANCE_PERCENT
    capex = rent * CAPEX_PERCENT
    insurance = price * INSURANCE_PERCENT
    property_taxes = price * PROPERTY_TAX_PERCENT

    # Calculate the expenses subtotal
    expenses_subtotal = property_mgmt + vacancy + maintenance_repairs + capex + insurance + property_taxes

    # Return the expenses as a dictionary
    return pd.Series({
        'Property Mgmt': property_mgmt,
        'Vacancy': vacancy,
        'Maintenance/Repairs': maintenance_repairs,
        'CapEx': capex,
        'Insurance': insurance,
        'Property Taxes': property_taxes,
        'Expenses Subtotal': expenses_subtotal
    })

def calculate_lending(row):
    # Extract the necessary information from the row
    price = row['price']

    # Check if the price is not NaN
    if pd.notnull(price):
        # Calculate the down payment amount
        down_payment = price * DOWN_PAYMENT_PERCENT

        # Calculate the loan amount
        loan_amount = price - down_payment

        # Convert the loan term from years to months
        loan_term_months = LOAN_TERM_YEARS * 12

        # Calculate the monthly interest rate
        monthly_interest_rate = LOAN_INTEREST_PERCENT / 12

        # Calculate the monthly mortgage payment using the pmt function from numpy_financial
        monthly_mortgage_payment = -npf.pmt(monthly_interest_rate, loan_term_months, loan_amount)
    else:
        # If the price is NaN, set the lending details to NaN
        down_payment = np.nan
        loan_amount = np.nan
        monthly_mortgage_payment = np.nan

    # Return the lending details as a dictionary
    return pd.Series({
        'Down Payment': down_payment,
        'Loan Amount': loan_amount,
        'Monthly Mortgage Payment': monthly_mortgage_payment
    })

def cash_to_close(row):
    price = row['price']
    down_payment = row['Down Payment']
    closing_costs = price * CLOSING_COSTS_PERCENT

    cash_to_close = round(closing_costs + down_payment)
    # Return the lending details as a dictionary
    return pd.Series({
        'Closing Costs': closing_costs,
        'Cash To Close': cash_to_close
    })
    
def calculate_returns(row):
    # Extract the necessary information from the row
    price = row['price']
    rent = row['rentZestimate']
    expenses_subtotal = row['Expenses Subtotal']
    down_payment = row['Down Payment']
    loan_amount = row['Loan Amount']
    monthly_mortgage_payment = row['Monthly Mortgage Payment']

    # Calculate the annual rental income
    annual_rental_income = rent * 12

    # Calculate the annual expenses
    annual_expenses = expenses_subtotal * 12

    # Calculate the annual cash flow
    annual_cash_flow = annual_rental_income - annual_expenses - (monthly_mortgage_payment * 12)

    # Replace NaN with 0 before rounding
    monthly_cash_flow = round(np.nan_to_num(annual_cash_flow / 12))

    # Calculate the total investment
    total_investment = down_payment + loan_amount

    # Calculate the Cash on Cash Return %
    if total_investment != 0:
        cash_on_cash_return = round((annual_cash_flow / total_investment) * 100, 1)
    else:
        cash_on_cash_return = 0

    # Calculate the Cap Rate
    if price != 0:
        cap_rate = round(((annual_rental_income - annual_expenses) / price) * 100, 1)
    else:
        cap_rate = 0

    # Return the returns as a dictionary
    return pd.Series({
        'Cash on Cash Return %': cash_on_cash_return,
        'Cap Rate': cap_rate,
        'Monthly Cash Flow': monthly_cash_flow
    })