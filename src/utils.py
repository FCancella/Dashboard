import pandas as pd

def df_treatment(untreated_df):
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
    df = untreated_df.copy()  # Avoid SettingWithCopyWarning by working on a copy of the DataFrame

    df = df.iloc[::2]
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except :
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])

    df.set_index('Date', inplace=True)
    df = df/df.iloc[0,:] # Normalize the data
    return df

def treat_to_plot(df, data_ini_slide=None, data_fim_slide=None):
    if data_ini_slide is not None:
        df = df.loc[data_ini_slide:data_fim_slide]
    treated_df = df_treatment(df)
    return treated_df
