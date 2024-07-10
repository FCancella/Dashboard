import pandas as pd

def df_treatment(df):
    """
    Treats the DataFrame by performing the following operations:
    
    1. Converts the 'Date' column to datetime format.
    2. Sets the 'Date' column as the DataFrame index.
    3. Normalizes the data by dividing by the first row, subtracting 1, and multiplying by 100.
    4. Resets the index and then sets the 'Date' column as the index again.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing a 'Date' column and numerical data columns to be treated.
    
    Returns:
    pd.DataFrame: The treated DataFrame with the 'Date' column as the index and normalized values.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.div(df.iloc[0]).subtract(1).multiply(100).reset_index()
    df.set_index('Date', inplace=True)
    return df
