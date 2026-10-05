from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_FILE = PROJECT_ROOT / "data" / "cleaned" / "steel_industry_energy_cleaned.csv"
EDA_FOLDER = PROJECT_ROOT / "data" / "eda"

EDA_FOLDER.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CLEANED_FILE, parse_dates=["DateTime"])

print("\nDATASET")
print("=" * 60)
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nDESCRIPTIVE STATISTICS")
print("=" * 60)
print(df[
    [
        "Energy_Consumption_kWh",
        "Lagging_Reactive_Power_kVarh",
        "Leading_Reactive_Power_kVarh",
        "CO2_tCO2",
        "Lagging_Power_Factor",
        "Leading_Power_Factor"
    ]
].describe())

print("\nENERGY STATISTICS")
print("=" * 60)
energy = df["Energy_Consumption_kWh"]

print("Mean:", energy.mean())
print("Median:", energy.median())
print("Minimum:", energy.min())
print("Maximum:", energy.max())
print("Standard Deviation:", energy.std())

print("\nMONTHLY ENERGY CONSUMPTION")
print("=" * 60)
monthly = df.groupby(["Month", "Month_Name"])["Energy_Consumption_kWh"].agg(
    Total_Energy="sum",
    Average_Energy="mean",
    Maximum_Energy="max"
).reset_index().sort_values("Month")

print(monthly.to_string(index=False))

print("\nDAILY ENERGY CONSUMPTION")
print("=" * 60)
daily = df.groupby(df["DateTime"].dt.date)["Energy_Consumption_kWh"].agg(
    Total_Energy="sum",
    Average_Energy="mean",
    Maximum_Energy="max"
).reset_index()

print(daily.head(10).to_string(index=False))

print("\nHOURLY ENERGY CONSUMPTION")
print("=" * 60)
hourly = df.groupby("Hour")["Energy_Consumption_kWh"].agg(
    Average_Energy="mean",
    Maximum_Energy="max",
    Total_Energy="sum"
).reset_index()

print(hourly.to_string(index=False))

print("\nLOAD TYPE ANALYSIS")
print("=" * 60)
load_analysis = df.groupby("Load_Type")["Energy_Consumption_kWh"].agg(
    Total_Energy="sum",
    Average_Energy="mean",
    Maximum_Energy="max",
    Standard_Deviation="std"
).reset_index()

print(load_analysis.to_string(index=False))

print("\nWEEKDAY VS WEEKEND")
print("=" * 60)
week_analysis = df.groupby("Week_Status")["Energy_Consumption_kWh"].agg(
    Total_Energy="sum",
    Average_Energy="mean",
    Maximum_Energy="max"
).reset_index()

print(week_analysis.to_string(index=False))

print("\nDAY OF WEEK ANALYSIS")
print("=" * 60)
day_analysis = df.groupby(
    ["Day_of_Week_Number", "Day_of_Week"]
)["Energy_Consumption_kWh"].agg(
    Total_Energy="sum",
    Average_Energy="mean",
    Maximum_Energy="max"
).reset_index().sort_values("Day_of_Week_Number")

print(day_analysis.to_string(index=False))

print("\nTIME PERIOD ANALYSIS")
print("=" * 60)
period_analysis = df.groupby("Time_Period")["Energy_Consumption_kWh"].agg(
    Total_Energy="sum",
    Average_Energy="mean",
    Maximum_Energy="max"
).reset_index()

print(period_analysis.to_string(index=False))

print("\nCO2 ANALYSIS")
print("=" * 60)
print(df["CO2_tCO2"].describe())

print("\nPOWER FACTOR ANALYSIS")
print("=" * 60)
print(
    df[
        [
            "Lagging_Power_Factor",
            "Leading_Power_Factor"
        ]
    ].describe()
)

print("\nCORRELATION WITH ENERGY CONSUMPTION")
print("=" * 60)

numeric_columns = [
    "Energy_Consumption_kWh",
    "Lagging_Reactive_Power_kVarh",
    "Leading_Reactive_Power_kVarh",
    "CO2_tCO2",
    "Lagging_Power_Factor",
    "Leading_Power_Factor"
]

correlation = df[numeric_columns].corr()["Energy_Consumption_kWh"].sort_values(
    ascending=False
)

print(correlation)

print("\nHIGH CONSUMPTION ANALYSIS")
print("=" * 60)

q1 = energy.quantile(0.25)
q3 = energy.quantile(0.75)
iqr = q3 - q1

upper_bound = q3 + 1.5 * iqr
lower_bound = q1 - 1.5 * iqr

print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Upper Bound:", upper_bound)
print("Lower Bound:", lower_bound)

anomalies = df[
    (df["Energy_Consumption_kWh"] > upper_bound) |
    (df["Energy_Consumption_kWh"] < lower_bound)
].copy()

print("Potential energy anomalies:", len(anomalies))

print("\nTOP 20 HIGHEST CONSUMPTION PERIODS")
print("=" * 60)

top_20 = df.nlargest(
    20,
    "Energy_Consumption_kWh"
)[
    [
        "DateTime",
        "Energy_Consumption_kWh",
        "Load_Type",
        "Week_Status",
        "Day_of_Week",
        "Hour",
        "Time_Period",
        "CO2_tCO2"
    ]
]

print(top_20.to_string(index=False))

print("\nSAVING EDA TABLES")
print("=" * 60)

monthly.to_csv(EDA_FOLDER / "monthly_analysis.csv", index=False)
daily.to_csv(EDA_FOLDER / "daily_analysis.csv", index=False)
hourly.to_csv(EDA_FOLDER / "hourly_analysis.csv", index=False)
load_analysis.to_csv(EDA_FOLDER / "load_type_analysis.csv", index=False)
week_analysis.to_csv(EDA_FOLDER / "weekday_weekend_analysis.csv", index=False)
day_analysis.to_csv(EDA_FOLDER / "day_of_week_analysis.csv", index=False)
period_analysis.to_csv(EDA_FOLDER / "time_period_analysis.csv", index=False)
correlation.to_csv(EDA_FOLDER / "energy_correlations.csv")
anomalies.to_csv(EDA_FOLDER / "potential_energy_anomalies.csv", index=False)

print("EDA tables saved to:", EDA_FOLDER)

plt.figure(figsize=(12, 6))
plt.plot(
    daily["DateTime"],
    daily["Total_Energy"]
)
plt.title("Daily Energy Consumption")
plt.xlabel("Date")
plt.ylabel("Total Energy Consumption (kWh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(EDA_FOLDER / "daily_energy_consumption.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(
    hourly["Hour"],
    hourly["Average_Energy"],
    marker="o"
)
plt.title("Average Energy Consumption by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average Energy Consumption (kWh)")
plt.xticks(range(24))
plt.grid(True)
plt.tight_layout()
plt.savefig(EDA_FOLDER / "hourly_energy_consumption.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(
    monthly["Month_Name"],
    monthly["Total_Energy"]
)
plt.title("Monthly Energy Consumption")
plt.xlabel("Month")
plt.ylabel("Total Energy Consumption (kWh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(EDA_FOLDER / "monthly_energy_consumption.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(
    load_analysis["Load_Type"],
    load_analysis["Average_Energy"]
)
plt.title("Average Energy Consumption by Load Type")
plt.xlabel("Load Type")
plt.ylabel("Average Energy Consumption (kWh)")
plt.tight_layout()
plt.savefig(EDA_FOLDER / "load_type_energy_consumption.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(
    week_analysis["Week_Status"],
    week_analysis["Average_Energy"]
)
plt.title("Average Energy Consumption: Weekday vs Weekend")
plt.xlabel("Week Status")
plt.ylabel("Average Energy Consumption (kWh)")
plt.tight_layout()
plt.savefig(EDA_FOLDER / "weekday_weekend_energy.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(
    period_analysis["Time_Period"],
    period_analysis["Average_Energy"]
)
plt.title("Average Energy Consumption by Time Period")
plt.xlabel("Time Period")
plt.ylabel("Average Energy Consumption (kWh)")
plt.tight_layout()
plt.savefig(EDA_FOLDER / "time_period_energy.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(
    df["Energy_Consumption_kWh"],
    df["CO2_tCO2"],
    alpha=0.3
)
plt.title("Energy Consumption vs CO2 Emissions")
plt.xlabel("Energy Consumption (kWh)")
plt.ylabel("CO2 (tCO2)")
plt.tight_layout()
plt.savefig(EDA_FOLDER / "energy_vs_co2.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(
    df["Energy_Consumption_kWh"],
    df["Lagging_Reactive_Power_kVarh"],
    alpha=0.3
)
plt.title("Energy Consumption vs Lagging Reactive Power")
plt.xlabel("Energy Consumption (kWh)")
plt.ylabel("Lagging Reactive Power (kVarh)")
plt.tight_layout()
plt.savefig(EDA_FOLDER / "energy_vs_reactive_power.png", dpi=300)
plt.show()

print("\nEDA COMPLETED SUCCESSFULLY!")