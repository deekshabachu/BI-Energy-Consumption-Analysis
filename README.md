\# Industrial Energy Consumption BI



\### Business Intelligence Case Study: Energy Monitoring, Anomaly Detection \& Demand Forecasting



\## Project Overview



This project presents a Business Intelligence (BI) solution for monitoring and analyzing industrial energy consumption.



The case study focuses on a steel manufacturing facility and uses historical electricity consumption data to identify consumption patterns, detect potential high-consumption events, analyze associated CO₂ emissions, and forecast short-term future energy demand.



The project combines data cleaning, exploratory data analysis, SQL-based analytics, statistical anomaly detection, machine learning-based forecasting, and interactive Tableau dashboards to transform raw energy data into actionable business insights.



\---



\## Business Problem



Industrial facilities consume large amounts of electricity across different operating conditions and time periods. Without proper monitoring and analysis, unusual consumption patterns and periods of high energy demand may be difficult to identify.



The objective of this case study is to develop a BI solution that helps an industrial facility:



\- Understand historical energy consumption patterns.

\- Identify periods of unusually high energy consumption.

\- Analyze energy consumption across different load conditions and time periods.

\- Understand the relationship between energy consumption and CO₂ emissions.

\- Forecast short-term future energy demand.

\- Support energy monitoring, planning, and operational decision-making.



\---



\## Objectives



1\. Analyze historical industrial energy consumption and identify major consumption patterns.

2\. Identify potential high-consumption events using statistical anomaly detection.

3\. Forecast short-term energy demand at 15-minute intervals.

4\. Translate analytical results into actionable recommendations for energy monitoring and planning.



\---



\## Dataset



The project uses the \*\*UCI Steel Industry Energy Consumption Dataset\*\*.



The dataset contains 15-minute interval energy consumption records from a steel industry facility in South Korea for the year 2018.



\### Dataset Characteristics



\- \*\*Records:\*\* 35,040

\- \*\*Time Period:\*\* January 2018 – December 2018

\- \*\*Frequency:\*\* 15-minute intervals

\- \*\*Industry:\*\* Steel Manufacturing

\- \*\*Location:\*\* South Korea



\### Main Variables



\- `DateTime` – Timestamp of the observation.

\- `Energy\_Consumption\_kWh` – Electricity consumption.

\- `Lagging\_Reactive\_Power\_kVarh` – Lagging reactive power.

\- `Leading\_Reactive\_Power\_kVarh` – Leading reactive power.

\- `CO2\_tCO2` – CO₂ emissions.

\- `Lagging\_Power\_Factor` – Lagging power factor.

\- `Leading\_Power\_Factor` – Leading power factor.

\- `Seconds\_From\_Midnight` – Seconds elapsed from midnight.

\- `Week\_Status` – Weekday or weekend.

\- `Day\_of\_Week` – Day of the week.

\- `Load\_Type` – Light, Medium, or Maximum load condition.



\---



\## Technology Stack



\- \*\*Python\*\* – Data cleaning, exploratory data analysis, anomaly detection, and forecasting.

\- \*\*Pandas\*\* – Data manipulation and preprocessing.

\- \*\*Scikit-learn\*\* – Random Forest forecasting model.

\- \*\*Oracle Database 21c XE\*\* – SQL-based data storage and analysis.

\- \*\*SQL\*\* – Analytical queries and business analysis.

\- \*\*Tableau\*\* – Interactive BI dashboards and visualization.

\- \*\*Git \& GitHub\*\* – Version control and project documentation.



\---



\# Project Workflow



The project follows a complete Business Intelligence workflow:



\*\*Data Source → Data Cleaning → Exploratory Data Analysis → SQL Analysis → Anomaly Detection → Forecasting → Tableau Dashboard → Business Insights \& Recommendations\*\*



\---



\## Data Cleaning \& Preparation



The raw dataset was processed using Python before being used for analytics.



\### Preparation Steps



\- Converted date/time values into a standardized `DateTime` field.

\- Standardized column names.

\- Checked for missing values.

\- Checked for duplicate records.

\- Validated energy consumption values.

\- Validated power-factor values.

\- Validated CO₂ emission values.

\- Added derived time-based features such as year, month, day, hour, minute, and time period.

\- Created weekday/weekend indicators.

\- Categorized observations into Night, Morning, Afternoon, and Evening time periods.



The cleaned dataset contains \*\*35,040 records and 19 analytical columns\*\* with no missing values or duplicate records.



\---



\## Exploratory Data Analysis



Exploratory Data Analysis (EDA) was performed using Python to understand the underlying energy consumption patterns.



The analysis included:



\- Monthly energy consumption.

\- Hourly energy consumption.

\- Day-of-week consumption.

\- Weekday versus weekend consumption.

\- Time-period consumption.

\- Load-type analysis.

\- CO₂ emission analysis.

\- Correlation analysis.

\- Identification of potential high-consumption observations.



\### Key EDA Findings



\- Average energy consumption was approximately \*\*27.39 kWh per 15-minute interval\*\*.

\- Peak recorded consumption was \*\*157.18 kWh\*\*.

\- Weekday consumption was substantially higher than weekend consumption.

\- Maximum-load periods showed the highest average energy consumption.

\- Morning and afternoon periods showed relatively higher energy demand.

\- Energy consumption showed a strong positive relationship with CO₂ emissions.

\- The highest monthly energy consumption occurred in \*\*January 2018\*\*.



\---



\## SQL Analysis



The cleaned data was loaded into an Oracle Database for structured analytical queries.



SQL analysis was used to examine:



\- Monthly energy consumption.

\- Monthly CO₂ emissions.

\- Energy consumption by load type.

\- CO₂ emissions by load type.

\- High-consumption events.

\- High-consumption events by hour.

\- High-consumption events by load condition.



This allowed the project to demonstrate the use of SQL as part of the BI data-analysis workflow.



\---



\## Anomaly Detection



Potential high-consumption events were identified using the \*\*Interquartile Range (IQR)\*\* statistical method.



The upper anomaly threshold was calculated as:



\*\*Upper Bound = Q3 + 1.5 × IQR\*\*



For the cleaned energy consumption data:



\- Q1 = \*\*3.20 kWh\*\*

\- Q3 = \*\*51.2375 kWh\*\*

\- IQR = \*\*48.0375 kWh\*\*

\- Upper threshold = \*\*123.29375 kWh\*\*



Observations above this threshold were classified as:



\*\*Potential High-Consumption Events\*\*



A total of \*\*328 potential high-consumption events\*\* were identified.



These events were analyzed by:



\- Load type.

\- Hour of the day.

\- Date/time.

\- Week status.



The project intentionally treats these observations as \*\*potential high-consumption events rather than confirmed equipment faults\*\*, since the available dataset does not provide equipment-level failure information.



\---



\## Predictive Analytics – Energy Demand Forecasting



Short-term energy demand forecasting was implemented using a \*\*Random Forest Regression model\*\*.



Instead of forecasting only daily totals, the final model predicts energy consumption at the original \*\*15-minute interval\*\*.



\### Forecasting Features



The model uses temporal and historical consumption features including:



\- Hour.

\- Minute.

\- Day of week.

\- Month.

\- Day of month.

\- Weekend indicator.

\- Time slot.

\- Previous energy consumption values.

\- Lagged consumption values.

\- Rolling consumption statistics.



\### Model Performance



The final 15-minute Random Forest model achieved:



| Metric | Result |

|---|---:|

| MAE | 4.32 kWh |

| RMSE | 9.08 kWh |

| MAPE | 18.44% |



The model was then retrained using the complete historical dataset and used to generate a \*\*7-day recursive energy demand forecast\*\* for January 2019.



\### 7-Day Forecast Summary



\- \*\*Forecast Period:\*\* January 1–7, 2019

\- \*\*Forecast Intervals:\*\* 672

\- \*\*Total Forecast Energy:\*\* 20,806.65 kWh

\- \*\*Average Forecast Energy:\*\* 30.96 kWh per 15-minute interval

\- \*\*Peak Forecast:\*\* 84.26 kWh

\- \*\*Peak Forecast Time:\*\* January 4, 2019 at 15:15



\---



\# Tableau BI Dashboards



The analytical results were transformed into four interactive Tableau dashboards.



\---



\## Dashboard 1 – Industrial Energy Consumption Overview



This dashboard provides a high-level overview of historical industrial energy consumption.



\### Key Performance Indicators



\- Total Energy Consumption

\- Average Energy Consumption

\- Peak Energy Consumption

\- Total CO₂ Emissions



\### Visualizations



\- Monthly Energy Trend

\- Hourly Consumption Pattern

\- Load Type Consumption



This dashboard provides a quick overview of the facility's overall energy usage and major consumption patterns.



\---



\## Dashboard 2 – Consumption Patterns



This dashboard focuses on understanding when and under what operating conditions energy consumption is highest.



\### Analysis



\- Weekday vs Weekend Consumption

\- Day-of-Week Consumption

\- Time Period Consumption

\- Load Type × Time Period Analysis



\### Filters



\- Month

\- Load Type

\- Week Status



The dashboard helps identify recurring operating patterns and periods of higher energy demand.



\---



\## Dashboard 3 – Potential High-Consumption Events



This dashboard focuses on observations that exceed the statistical high-consumption threshold.



\### Visualizations



\- Potential Event Count

\- Events by Load Type

\- Events by Hour

\- Potential Events Timeline



\### Key Finding



A total of \*\*328 potential high-consumption events\*\* were identified.



The distribution across load types was:



\- Maximum Load: \*\*149 events\*\*

\- Medium Load: \*\*146 events\*\*

\- Light Load: \*\*33 events\*\*



The highest number of potential events occurred during higher-demand operating hours, particularly around the morning and afternoon periods.



\---



\## Dashboard 4 – Energy Demand Forecast



This dashboard presents the short-term machine learning forecast.



\### Key Metrics



\- Forecast Total: \*\*20,806.65 kWh\*\*

\- Forecast Average: \*\*30.96 kWh\*\*

\- Peak Forecast: \*\*84.26 kWh\*\*



The dashboard includes:



\- 7-Day 15-Minute Energy Forecast

\- Daily Forecast Summary

\- Random Forest Model Performance



\### Model Performance



\*\*Random Forest – 15-minute forecasting\*\*



\- MAE: \*\*4.32 kWh\*\*

\- RMSE: \*\*9.08 kWh\*\*

\- MAPE: \*\*18.44%\*\*



\---



\# Key Business Insights



The analysis produced several important insights for industrial energy management:



1\. \*\*Energy demand varies significantly throughout the day.\*\*  

&#x20;  Morning and afternoon periods show higher energy consumption compared with nighttime periods.



2\. \*\*Weekdays consume considerably more energy than weekends.\*\*  

&#x20;  This reflects differences in industrial operating activity.



3\. \*\*Maximum-load conditions have the highest energy consumption.\*\*  

&#x20;  Load classification can therefore be useful for understanding operating demand.



4\. \*\*Energy consumption is strongly associated with CO₂ emissions.\*\*  

&#x20;  Reducing unnecessary electricity consumption can therefore contribute to reducing associated emissions.



5\. \*\*Potential high-consumption events are concentrated during higher-demand operating hours.\*\*  

&#x20;  These periods can be prioritized for monitoring and investigation.



6\. \*\*Short-term demand forecasting can support energy planning.\*\*  

&#x20;  Forecasting energy demand at 15-minute intervals provides more granular information than daily-level forecasting.



\---



\# Business Recommendations



Based on the analytical findings, the following actions can be recommended:



\### 1. Monitor High-Demand Periods



Energy managers should closely monitor morning and afternoon periods where consumption tends to be higher.



\### 2. Investigate Potential High-Consumption Events



Events exceeding the statistical threshold should be reviewed to determine whether they are associated with normal production activity, unusual operating conditions, or avoidable energy usage.



\### 3. Use Forecasts for Energy Planning



Short-term demand forecasts can help energy managers anticipate upcoming periods of higher consumption and plan operational activities accordingly.



\### 4. Focus on High-Load Operations



Maximum-load operating periods should receive greater attention because they contribute significantly to total energy consumption.



\### 5. Track Energy and Emissions Together



Energy consumption and CO₂ emissions should be monitored together to support both operational efficiency and sustainability goals.



\---



\# Project Structure



```text

BI\_project/

│

├── data/

│   ├── raw/

│   │   └── Steel\_industry\_data.csv

│   │

│   ├── cleaned/

│   │   └── steel\_industry\_energy\_cleaned.csv

│   │

│   └── eda/

│       ├── daily\_analysis.csv

│       ├── hourly\_analysis.csv

│       ├── monthly\_analysis.csv

│       ├── load\_type\_analysis.csv

│       ├── weekday\_weekend\_analysis.csv

│       ├── time\_period\_analysis.csv

│       ├── energy\_correlations.csv

│       ├── potential\_energy\_anomalies.csv

│       └── energy\_forecast\_15min.csv

│

├── notebooks/

│   ├── data\_cleaning.py

│   ├── eda.py

│   ├── forecasting.py

│   └── forecast\_check.py

│

├── sql/

│   └── analysis.sql

│

├── tableau/

│   └── BI case study.twb

│

├── scripts/

│

├── docs/

│

└── README.md

```markdown



\---

\## Conclusion



This project demonstrates how Business Intelligence can be applied to industrial energy management by combining historical analysis, statistical anomaly detection, SQL analytics, machine learning-based forecasting, and interactive visualization.



The final solution transforms raw 15-minute energy consumption data into meaningful business insights that can support energy monitoring, operational planning, anomaly investigation, and demand forecasting.



The project also demonstrates an end-to-end BI workflow, from raw data preparation and database analysis to predictive analytics and dashboard-based business decision support.



\---



\## Future Improvements



Possible future extensions include:



\- Incorporating real-time energy meter data.

\- Adding equipment-level monitoring.

\- Developing more advanced anomaly detection techniques.

\- Comparing multiple forecasting algorithms.

\- Extending the forecast horizon.

\- Adding energy-cost analysis using real electricity tariffs.

\- Implementing automated alerts for high-consumption events.

\- Integrating the Tableau dashboard with continuously updated data sources.

