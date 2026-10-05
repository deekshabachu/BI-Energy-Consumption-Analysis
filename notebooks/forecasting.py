from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "cleaned" / "steel_industry_energy_cleaned.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "eda" / "energy_forecast_15min.csv"

df = pd.read_csv(INPUT_FILE)
df["DateTime"] = pd.to_datetime(df["DateTime"])

df = df.sort_values("DateTime").reset_index(drop=True)

df["Hour"] = df["DateTime"].dt.hour
df["Minute"] = df["DateTime"].dt.minute
df["Day_of_Week"] = df["DateTime"].dt.dayofweek
df["Month"] = df["DateTime"].dt.month
df["Day_of_Month"] = df["DateTime"].dt.day
df["Is_Weekend"] = (df["Day_of_Week"] >= 5).astype(int)

df["Time_Slot"] = df["Hour"] * 4 + (df["Minute"] // 15)

df["Lag_1"] = df["Energy_Consumption_kWh"].shift(1)
df["Lag_2"] = df["Energy_Consumption_kWh"].shift(2)
df["Lag_4"] = df["Energy_Consumption_kWh"].shift(4)
df["Lag_8"] = df["Energy_Consumption_kWh"].shift(8)
df["Lag_96"] = df["Energy_Consumption_kWh"].shift(96)
df["Lag_672"] = df["Energy_Consumption_kWh"].shift(672)

df["Rolling_4"] = (
    df["Energy_Consumption_kWh"]
    .shift(1)
    .rolling(4)
    .mean()
)

df["Rolling_96"] = (
    df["Energy_Consumption_kWh"]
    .shift(1)
    .rolling(96)
    .mean()
)

df["Rolling_672"] = (
    df["Energy_Consumption_kWh"]
    .shift(1)
    .rolling(672)
    .mean()
)

df = df.dropna().reset_index(drop=True)

features = [
    "Hour",
    "Minute",
    "Day_of_Week",
    "Month",
    "Day_of_Month",
    "Is_Weekend",
    "Time_Slot",
    "Lag_1",
    "Lag_2",
    "Lag_4",
    "Lag_8",
    "Lag_96",
    "Lag_672",
    "Rolling_4",
    "Rolling_96",
    "Rolling_672"
]

target = "Energy_Consumption_kWh"

split_index = int(len(df) * 0.8)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=18,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

actual = y_test.values
non_zero = actual != 0

mape = (
    np.mean(
        np.abs(
            (actual[non_zero] - predictions[non_zero])
            / actual[non_zero]
        )
    )
    * 100
)

print("\n15-MINUTE RANDOM FOREST FORECAST")
print("-" * 45)
print(f"Training observations : {len(train)}")
print(f"Testing observations  : {len(test)}")
print(f"MAE                   : {mae:.2f} kWh")
print(f"RMSE                  : {rmse:.2f} kWh")
print(f"MAPE                  : {mape:.2f}%")

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values(
    "Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE")
print("-" * 45)
print(importance.to_string(index=False))

print("\nTRAINING FINAL MODEL")
print("-" * 45)

final_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=18,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

final_model.fit(
    df[features],
    df[target]
)

history = df[
    ["DateTime", target]
].copy()

forecast_intervals = 7 * 96

future_rows = []

for i in range(forecast_intervals):

    next_datetime = (
        history["DateTime"].max()
        + pd.Timedelta(minutes=15)
    )

    values = history[target].tolist()

    hour = next_datetime.hour
    minute = next_datetime.minute
    day_of_week = next_datetime.dayofweek
    month = next_datetime.month
    day_of_month = next_datetime.day
    is_weekend = int(day_of_week >= 5)

    time_slot = hour * 4 + (minute // 15)

    lag_1 = values[-1]
    lag_2 = values[-2]
    lag_4 = values[-4]
    lag_8 = values[-8]
    lag_96 = values[-96]
    lag_672 = values[-672]

    rolling_4 = np.mean(values[-4:])
    rolling_96 = np.mean(values[-96:])
    rolling_672 = np.mean(values[-672:])

    X_future = pd.DataFrame([{
        "Hour": hour,
        "Minute": minute,
        "Day_of_Week": day_of_week,
        "Month": month,
        "Day_of_Month": day_of_month,
        "Is_Weekend": is_weekend,
        "Time_Slot": time_slot,
        "Lag_1": lag_1,
        "Lag_2": lag_2,
        "Lag_4": lag_4,
        "Lag_8": lag_8,
        "Lag_96": lag_96,
        "Lag_672": lag_672,
        "Rolling_4": rolling_4,
        "Rolling_96": rolling_96,
        "Rolling_672": rolling_672
    }])

    prediction = final_model.predict(X_future)[0]
    prediction = max(0, prediction)

    future_rows.append({
        "DateTime": next_datetime,
        "Forecast_Energy_kWh": prediction
    })

    history = pd.concat(
        [
            history,
            pd.DataFrame({
                "DateTime": [next_datetime],
                target: [prediction]
            })
        ],
        ignore_index=True
    )

forecast_df = pd.DataFrame(future_rows)

historical_df = df[
    ["DateTime", "Energy_Consumption_kWh"]
].copy()

historical_df = historical_df.rename(
    columns={
        "Energy_Consumption_kWh": "Actual_Energy_kWh"
    }
)

historical_df["Forecast_Energy_kWh"] = np.nan

forecast_df["Actual_Energy_kWh"] = np.nan

forecast_df = forecast_df[
    [
        "DateTime",
        "Actual_Energy_kWh",
        "Forecast_Energy_kWh"
    ]
]

historical_df = historical_df[
    [
        "DateTime",
        "Actual_Energy_kWh",
        "Forecast_Energy_kWh"
    ]
]

final_output = pd.concat(
    [
        historical_df,
        forecast_df
    ],
    ignore_index=True
)

final_output.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFORECAST CREATED")
print("-" * 45)
print(f"Forecast horizon : 7 days")
print(f"Forecast points  : {len(forecast_df)}")
print(f"Output file      : {OUTPUT_FILE}")
print(f"Forecast start   : {forecast_df['DateTime'].min()}")
print(f"Forecast end     : {forecast_df['DateTime'].max()}")

print("\nFIRST 20 FORECAST POINTS")
print("-" * 45)
print(
    forecast_df.head(20).to_string(index=False)
)