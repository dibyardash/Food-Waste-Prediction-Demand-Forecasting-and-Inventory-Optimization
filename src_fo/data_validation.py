import pandas as pd
import numpy as np
 

# LOAD DATA

 
file_path = "Food Waste.csv"
 
df = pd.read_csv(file_path)
 
print("=" * 60)
print("ORIGINAL DATASET INFO")
print("=" * 60)
 
print("Rows, Columns:", df.shape)
 

# MISSING VALUES

 
print("\nMissing Values")
 
print(df.isnull().sum())
 
missing_rows = df.isnull().any(axis=1).sum()
 
print(f"\nRows containing missing values: {missing_rows}")
 
# Remove missing values
df.dropna(inplace=True)
 

# DUPLICATES

 
duplicates = df.duplicated().sum()
 
print(f"\nDuplicate Rows Found: {duplicates}")
 
df.drop_duplicates(inplace=True)
 

# DATE VALIDATION

 
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)
 
invalid_dates = df["Date"].isna().sum()
 
print(f"\nInvalid Dates Found: {invalid_dates}")
 
df.dropna(
    subset=["Date"],
    inplace=True
)
 

# CATEGORICAL CLEANING

 
categorical_cols = [
 
    "Meal_Type",
    "Food_Item"
 
]
 
for col in categorical_cols:
 
    df[col] = (
 
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
 
    )
 

# NUMERIC VALIDATION

 
numeric_cols = [
 
    "Quantity_Prepared",
    "Quantity_Sold",
    "Quantity_Wasted",
    "Temperature",
    "Rainfall",
    "Previous_Day_Sales",
    "Previous_Day_Waste"
 
]
 
for col in numeric_cols:
 
    negative_count = (
        df[col] < 0
    ).sum()
 
    print(
        f"Negative values in {col}: {negative_count}"
    )
 
    df = df[
        df[col] >= 0
    ]
 

# BUSINESS RULE VALIDATION
 
# Sold should not exceed prepared
 
invalid_sales = (
 
    df["Quantity_Sold"]
 
    >
 
    df["Quantity_Prepared"]
 
).sum()
 
print(
    f"\nQuantity_Sold > Quantity_Prepared : {invalid_sales}"
)
 
df = df[
    df["Quantity_Sold"]
 
    <=
 
    df["Quantity_Prepared"]
]
 
# Wasted should not exceed prepared
 
invalid_waste = (
 
    df["Quantity_Wasted"]
 
    >
 
    df["Quantity_Prepared"]
 
).sum()
 
print(
    f"Quantity_Wasted > Quantity_Prepared : {invalid_waste}"
)
 
df = df[
    df["Quantity_Wasted"]
 
    <=
 
    df["Quantity_Prepared"]
]
 

# OUTLIER DETECTION

 
for col in [
 
    "Quantity_Prepared",
    "Quantity_Sold",
    "Quantity_Wasted"
 
]:
 
    Q1 = df[col].quantile(0.25)
 
    Q3 = df[col].quantile(0.75)
 
    IQR = Q3 - Q1
 
    lower = Q1 - 1.5 * IQR
 
    upper = Q3 + 1.5 * IQR
 
    outliers = (
 
        (df[col] < lower)
 
        |
 
        (df[col] > upper)
 
    ).sum()
 
    print(
        f"Outliers in {col}: {outliers}"
    )
 

# SORT DATE ASCENDING

 
df = df.sort_values(
 
    by="Date",
 
    ascending=True
 
)
 
# Keep adjacent columns together
df.reset_index(
    drop=True,
    inplace=True
)
 

# FINAL CHECK

 
print("\n" + "=" * 60)
print("FINAL DATASET")
print("=" * 60)
 
print("Shape:", df.shape)
 
print("\nMissing Values Remaining")
 
print(df.isnull().sum())
 
print("\nDate Range")
 
print("Start :", df["Date"].min())
 
print("End   :", df["Date"].max())
 

# SAVE CLEANED DATASET

 
output_file = "Food Waste Cleaned.csv"
 
df.to_csv(
    output_file,
    index=False
)
 
print(
    f"\n✅ Cleaned dataset saved as: {output_file}"
)