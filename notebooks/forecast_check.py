from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "eda" / "energy_forecast_15min.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "eda" / "forecast_check.png"

df = pd.read_csv(INPUT_FILE)
df["DateTime"] = pd.to_datetime(df["DateTime"])

forecast = df[df["Forecast_Energy_kWh"].notna()].copy()

forecast["Date"] = forecast["DateTime"].dt.date
forecast["Hour"] = forecast["DateTime"].dt.hour

daily_forecast = (
    forecast
    .groupby("Date")["Forecast_Energy_kWh"]
    .sum()
)

hourly_forecast = (
    forecast
    .groupby("Hour")["Forecast_Energy_kWh"]
    .mean()
)

print("\nFORECAST SUMMARY")
print("-" * 45)

print(f"Forecast mean : {forecast['Forecast_Energy_kWh'].mean():.2f} kWh")
print(f"Forecast min  : {forecast['Forecast_Energy_kWh'].min():.2f} kWh")
print(f"Forecast max  : {forecast['Forecast_Energy_kWh'].max():.2f} kWh")
print(f"Forecast total: {forecast['Forecast_Energy_kWh'].sum():.2f} kWh")

print("\nDAILY FORECAST")
print("-" * 45)
print(daily_forecast.to_string())

print("\nPEAK FORECAST")
print("-" * 45)

peak_row = forecast.loc[
    forecast["Forecast_Energy_kWh"].idxmax()
]

print(f"DateTime : {peak_row['DateTime']}")
print(f"Energy  : {peak_row['Forecast_Energy_kWh']:.2f} kWh")

plt.figure(figsize=(14, 6))

plt.plot(
    forecast["DateTime"],
    forecast["Forecast_Energy_kWh"]
)

plt.title("7-Day Forecasted Energy Consumption")
plt.xlabel("Date")
plt.ylabel("Energy Consumption (kWh)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=150
)

plt.show()

print(f"\nChart saved to: {OUTPUT_FILE}")