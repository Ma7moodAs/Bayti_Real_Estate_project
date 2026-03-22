import pandas as pd
import numpy as np
import re


def extract_data(text,patterns):# Data extraction function 
    if pd.isna(text):
        return np.nan
    
    for pattern in patterns:
        match_pattern = re.search(pattern=pattern,string=text)
        if match_pattern:
            value = match_pattern.group(1)
            value = value.replace(',','')
            return int(value)
    return np.nan


# extract the number of bathrooms from the description or specialities columns
def extract_bathrooms_num(text):
    patterns = [
        r'(\d+)\s*حمامات',
        r'حمامات\s*عدد\s*(\d+)',
        r'(\d+)\s*حمام'
    ]
    return extract_data(text,patterns)
    
def extract_annualy_price(text):
    patterns = [
        r'السعر\s*\(?سنوي\)?\s*[:\-]?\s*([\d,]+)',
        r'سنوي\s*[:\-]?\s*([\d,]+)',
        r'السعر\s*[:\-]?\s*([\d,]+)'
    ]
    return extract_data(text,patterns)

def extract_sale_price(text):
    patterns = [
        r'السعر\s*[:\-]?\s*([\d,]+)',
        r'سعر\s*\(?البيع\)?\s*[:\-]?\s*([\d,]+)'
    ]
    return extract_data(text,patterns)

def fill_bathrooms_num(row):
    if pd.notna(row['Bathrooms']):
        return row['Bathrooms']
    
    value = extract_bathrooms_num(row['Description'])
    if pd.isna(value):
        value = extract_bathrooms_num(row['Specialities'])
    return value 

def fill_annualy_price(row):
    if pd.notna(row['Price_annualy']):
        return row['Price_annualy']
    
    value = extract_annualy_price(row['Description'])
    if pd.isna(value):
        value = extract_annualy_price(row['Specialities'])
    return value 

def fill_sale_price(row):
    if pd.notna(row['Sale_price']):
        return row['Sale_price']
    
    value = extract_sale_price(row['Description'])
    if pd.isna(value):
        value = extract_sale_price(row['Specialities'])
    return value 

def recover_missing_values(df): # Feature recovery from unstructured data
    # Filling the missing values in the Bathrooms column
    bath_mask = df['Bathrooms'].isna()
    df.loc[bath_mask,'Bathrooms'] = df.loc[bath_mask,:].apply(fill_bathrooms_num,axis=1)

    # Filling the missing values in the Price_annualy column (rent listing type)
    annualy_price_mask = (df['Price_annualy'].isna()) & (df['Listing_type'] == 'rent')
    df.loc[annualy_price_mask,'Price_annualy'] = df.loc[annualy_price_mask,:].apply(fill_annualy_price,axis=1)

    # Filling the missing values in the Sale_price column (sale listing type)
    sale_price_mask = (df['Sale_price'].isna()) & (df['Listing_type'] == 'sale')
    df.loc[sale_price_mask,'Sale_price'] = df.loc[sale_price_mask,:].apply(fill_sale_price,axis=1)

    return df

# Function to handle the remaining missing values in the DataFrame after recovering some of them
def handle_missing_values(df):
    pass
