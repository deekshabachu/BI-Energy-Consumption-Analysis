import pandas as pd
import numpy as np
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Steel_industry_data.csv"
CLEANED_FILE = PROJECT_ROOT / "data" / "cleaned" / "steel_industry_energy_cleaned.csv"


print("Raw file:", RAW_FILE)
print("Output file:", CLEANED_FILE)


df = pd.read_csv(RAW_FILE)

print("Dataset loaded successfully!")
print("Shape:", df.shape)

clean_df = df.copy()

clean_df.head()

print("Columns:")
for column in clean_df.columns:
    print(column)

clean_df.info()

missing_values = clean_df.isnull().sum()

print("Missing values:")
print(missing_values)


missing_percentage = (clean_df.isnull().sum() / len(clean_df)) * 100

print("Missing-value percentage:")
print(missing_percentage)

duplicate_count = clean_df.duplicated().sum()

print("Number of duplicate rows:", duplicate_count)

clean_df = clean_df.drop_duplicates()

clean_df["date"] = pd.to_datetime(
    clean_df["date"],
    format="%d/%m/%Y %H:%M",
    errors="coerce"
)

print(clean_df["date"].dtype)
print(clean_df["date"].head())

invalid_dates = clean_df["date"].isna().sum()

print("Invalid dates:", invalid_dates)

clean_df = clean_df.rename(columns={
    "date": "DateTime",
    "Usage_kWh": "Energy_Consumption_kWh",
    "Lagging_Current_Reactive.Power_kVarh": "Lagging_Reactive_Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh": "Leading_Reactive_Power_kVarh",
    "CO2(tCO2)": "CO2_tCO2",
    "Lagging_Current_Power_Factor": "Lagging_Power_Factor",
    "Leading_Current_Power_Factor": "Leading_Power_Factor",
    "NSM": "Seconds_From_Midnight",
    "WeekStatus": "Week_Status",
    "Day_of_week": "Day_of_Week",
    "Load_Type": "Load_Type"
})


print(clean_df.columns.tolist())

numeric_columns = [
    "Energy_Consumption_kWh",
    "Lagging_Reactive_Power_kVarh",
    "Leading_Reactive_Power_kVarh",
    "CO2_tCO2",
    "Lagging_Power_Factor",
    "Leading_Power_Factor",
    "Seconds_From_Midnight"
]

for column in numeric_columns:
    clean_df[column] = pd.to_numeric(
        clean_df[column],
        errors="coerce"
    )


negative_energy = (
    clean_df["Energy_Consumption_kWh"] < 0
).sum()

print("Negative energy readings:", negative_energy)


invalid_lagging_pf = (
    (clean_df["Lagging_Power_Factor"] < 0) |
    (clean_df["Lagging_Power_Factor"] > 100)
).sum()

invalid_leading_pf = (
    (clean_df["Leading_Power_Factor"] < 0) |
    (clean_df["Leading_Power_Factor"] > 100)
).sum()

print("Invalid lagging power factor:", invalid_lagging_pf)
print("Invalid leading power factor:", invalid_leading_pf)

negative_co2 = (
    clean_df["CO2_tCO2"] < 0
).sum()

print("Negative CO2 readings:", negative_co2)

clean_df["Year"] = clean_df["DateTime"].dt.year
clean_df["Month"] = clean_df["DateTime"].dt.month
clean_df["Month_Name"] = clean_df["DateTime"].dt.strftime("%B")
clean_df["Day"] = clean_df["DateTime"].dt.day
clean_df["Hour"] = clean_df["DateTime"].dt.hour
clean_df["Minute"] = clean_df["DateTime"].dt.minute



def get_time_period(hour):
    if 0 <= hour < 6:
        return "Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"

clean_df["Time_Period"] = clean_df["Hour"].apply(get_time_period)

clean_df["Day_of_Week_Number"] = clean_df["DateTime"].dt.dayofweek + 1

print("Cleaned dataset shape:")
print(clean_df.shape)

print("\nData types:")
print(clean_df.dtypes)

print("\nMissing values:")
print(clean_df.isnull().sum())

clean_df = clean_df.sort_values("DateTime").reset_index(drop=True)

print("Final duplicate rows:", clean_df.duplicated().sum())
print("Final row count:", len(clean_df))


clean_df.head(10)



clean_df.to_csv(
    CLEANED_FILE,
    index=False
)

print("Cleaned dataset saved successfully!")
print("Location:", CLEANED_FILE)



print()
print("FINAL DATA QUALITY REPORT")
print()

print(f"Rows: {clean_df.shape[0]:,}")
print(f"Columns: {clean_df.shape[1]}")

print(f"\nMissing values: {clean_df.isnull().sum().sum():,}")
print(f"Duplicate rows: {clean_df.duplicated().sum():,}")

print(
    f"\nDate range: "
    f"{clean_df['DateTime'].min()} → "
    f"{clean_df['DateTime'].max()}"
)

print(
    f"\nEnergy consumption range: "
    f"{clean_df['Energy_Consumption_kWh'].min():.2f} → "
    f"{clean_df['Energy_Consumption_kWh'].max():.2f} kWh"
)

print("\nLoad types:")
print(clean_df["Load_Type"].value_counts())

print("\nWeek status:")
print(clean_df["Week_Status"].value_counts())

print("\nTime periods:")
print(clean_df["Time_Period"].value_counts())





