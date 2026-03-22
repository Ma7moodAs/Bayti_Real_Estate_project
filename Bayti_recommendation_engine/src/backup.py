import pandas as pd
import numpy as np
import re


ARABIC_DIGIT_TRANSLATION = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def normalize_text(text):
    if pd.isna(text):
        return None
    normalized = str(text).translate(ARABIC_DIGIT_TRANSLATION)
    return re.sub(r"\s+", " ", normalized).strip()


def extract_number_from_patterns(text, patterns):
    normalized_text = normalize_text(text)
    if normalized_text is None:
        return None

    for pattern in patterns:
        match = re.search(pattern, normalized_text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1).replace(",", ""))
    return None


def extract_bathrooms_num(text):
    patterns = [
        r"(?:عدد\s*)?حمامات?\s*[:\-]?\s*(\d+)",
        r"(\d+)\s*حمامات?",
        r"(\d+)\s*حمام",
    ]
    return extract_number_from_patterns(text, patterns)


def extract_annualy_price(text):
    patterns = [
        r"(?:الايجار|الإيجار|السعر|القيمة)[^\n\r]{0,40}?(?:سنوي|سنويا|سنويًا)[^\d]{0,10}([\d,]+)",
        r"(?:سنوي|سنويا|سنويًا)[^\d]{0,10}([\d,]+)",
        r"([\d,]+)\s*(?:دينار|د\.?\s*ا)[^\n\r]{0,20}?(?:سنوي|سنويا|سنويًا)",
    ]
    return extract_number_from_patterns(text, patterns)


def extract_sale_price(text):
    patterns = [
        r"(?:سعر\s*البيع|السعر|الثمن|السعر\s*البيعي)[^\d]{0,10}([\d,]+)",
        r"(?:للبيع|بيع)[^\n\r]{0,30}?([\d,]+)\s*(?:دينار|د\.?\s*ا)",
        r"([\d,]+)\s*(?:دينار|د\.?\s*ا)[^\n\r]{0,20}?(?:للبيع|بيع)",
    ]
    return extract_number_from_patterns(text, patterns)


def fill_bathrooms_num(row):
    if pd.notna(row["Bathrooms"]):
        return row["Bathrooms"]

    value = extract_bathrooms_num(row["Description"])
    if value is None:
        value = extract_bathrooms_num(row["Specialities"])
    return value


def fill_annually_price(row):
    if pd.notna(row["Price_annualy"]):
        return row["Price_annualy"]

    value = extract_annualy_price(row["Specialities"])
    if pd.isna(value):
        value = extract_annualy_price(row["Description"])
    return value


def fill_sale_price(row):
    if pd.notna(row["Sale_price"]):
        return row["Sale_price"]

    value = extract_sale_price(row["Description"])
    if pd.isna(value):
        value = extract_sale_price(row["Specialities"])
    return value


def fill_bathrooms_from_text(df):
    result = df.copy()
    bathroom_mask = result["Bathrooms"].isna()
    result.loc[bathroom_mask, "Bathrooms"] = result.loc[bathroom_mask].apply(
        fill_bathrooms_num,
        axis=1,
    )
    return result


def fill_annual_price_from_text(df):
    result = df.copy()
    rent_mask = (result["Listing_type"] == "rent") & (result["Price_annualy"].isna())
    result.loc[rent_mask, "Price_annualy"] = result.loc[rent_mask].apply(
        fill_annually_price,
        axis=1,
    )
    return result


def fill_sale_price_from_text(df):
    result = df.copy()
    sale_mask = (result["Listing_type"] == "sale") & (result["Sale_price"].isna())
    result.loc[sale_mask, "Sale_price"] = result.loc[sale_mask].apply(
        fill_sale_price,
        axis=1,
    )
    return result


def run_feature_extraction_pass(df):
    result = df.copy()
    result = fill_bathrooms_from_text(result)
    result = fill_annual_price_from_text(result)
    result = fill_sale_price_from_text(result)
    return result


def cleaning_report(before_df, after_df):
    tracked_columns = ["Bathrooms", "Price_annualy", "Sale_price"]
    report = {}

    for column in tracked_columns:
        before_missing = int(before_df[column].isna().sum())
        after_missing = int(after_df[column].isna().sum())
        report[column] = {
            "missing_before": before_missing,
            "missing_after": after_missing,
            "filled": before_missing - after_missing,
        }

    return report


def clean_data(df):
    extracted_df = run_feature_extraction_pass(df)
    report = cleaning_report(df, extracted_df)
    return extracted_df, report



