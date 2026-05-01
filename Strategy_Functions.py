######################################################################
# Case Study - Pablo Clemente Hevia / March 25th, 2026
######################################################################

######################################################################
# Imports
######################################################################
import pandas as pd
import numpy as np

######################################################################
# A. Function 1: USd to USD
######################################################################

# This function converts USd prices or quantities into USD equal amounts. 
def normalize_prices(df, price_column, currency_column, close_column):
    """
    Inputs
    -------
    df: dataframe           -> dataframe with the information of the prices
    price_column: string    -> name of the new column representing the price in USD
    currency_column: string -> name of the column representing the quoted currency
    close_column: string    -> name of the column representing the price of the contract (close)
    -------
    Outputs
    -------
    temp_df: dataframe      -> a copy of df with the price in USD as a new column
    -------
    
    """
    # We make a copy for not working on the original
    temp_df = df.copy()
    
    # We divide by 100 to convert USd into USD
    temp_df[price_column] = np.where(
        temp_df[currency_column] == 'USd', 
        temp_df[close_column] / 100, 
        temp_df[close_column]
    )
    
    print('\nThe normalize_prices function has been called. Prices quoted in USd has been converted to USD.')
    
    return temp_df

######################################################################
# B. Function 2: Roll yield calculation
######################################################################

# This function implements the roll yield formula
def calculate_roll_yield(contracts_df, mat_year_column, mat_month_column, price_usd_column):
    """
    Inputs
    -------
    contracts_df: dataframe  -> dataframe with the information of the contracts (after liquidity constraints)
    mat_year_column: string  -> name of the column representing the maturity year
    mat_month_column: string -> name of the column representing the maturity month
    price_usd_column: string -> name of the column representing the price in USD (close)
    -------
    Outputs
    -------
    contracts_df: dataframe  -> the input dataframe with the roll yield as a new column
    -------
    """
    
    # We sort the data
    contracts_df = contracts_df.sort_values([mat_year_column, mat_month_column])
    
    # Front contract information
    price_front = contracts_df[price_usd_column].iloc[0]
    months_front = contracts_df[mat_year_column].iloc[0] * 12 + contracts_df[mat_month_column].iloc[0]
    
    # Maturity in months
    contracts_df['total_months'] = contracts_df[mat_year_column] * 12 + contracts_df[mat_month_column]
    
    # Month difference
    contracts_df['month_diff'] = contracts_df['total_months'] - months_front
    
    # Roll yield formula implementation
    contracts_df['roll_yield'] = (
        (price_front / contracts_df[price_usd_column]) - 1
    ) / contracts_df['month_diff']
    
    # We eliminate NaN values from month_difference = 0 
    contracts_df['roll_yield'] = contracts_df['roll_yield'].fillna(0)
    
    return contracts_df

