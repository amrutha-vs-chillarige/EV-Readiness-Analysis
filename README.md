EV Charging Readiness Dashboard – India

This project analyzes Electric Vehicle (EV) sales, charging station infrastructure, and population data to evaluate state-level EV readiness in India.

Tools Used
- Python (Pandas, MySQL)
- Power BI
- MySQL (local)

📁 Data Sources
- EV sales dataset (state-wise)
- Charging station count as of March 2024
- State population data (2011 Census)

📈 Key Metrics
- EVs per Charging Station
- Charging Stations per Million People
- EV Readiness Score (custom metric)

📌 Dashboard Insights
- Uttar Pradesh, Maharashtra, and Karnataka lead in EV sales.
- Delhi has dense charging infrastructure.
- Smaller states like Sikkim and Arunachal rank high in readiness due to better per capita infrastructure.

📊 Data Highlights

- Total EVs: ~4 million
- Charging Stations: ~16,000
- Avg. EVs per Station: ~412
- Avg. Stations per Million People: ~15.6

Data Processing (SQL)
This project used SQL to:
- Aggregate EV sales and charging station counts by state
- Calculate EV readiness metrics (EVs per station)
- Normalize station counts per million population

All queries can be found [here](./sql/ev_readiness_queries.sql)


📷 Screenshots

**Page 1: EV Sales by State**
![EV Sales by State Bar chart](screenshots/Page_1_-_EV Sales by State.png)

**Page 2: Charging Stations Distribution**
![Charging Stations Distribution Map](screenshots/Page_2_-_Charging Stations Distribution.png)

**Page 3: EV Readiness Score**
![EV Readiness Score Bar Chart](screenshots/Page_2_-_EV Readiness Score.png)

**Page 4: Metrics and KPIs**
![Metrics and KPIs](screenshots/Page_2_-_Metrics and KPIs.png)


🚀 How to Run
- Run `ev_pipeline.py` to clean and store data in MySQL
- Open `ev_dashboard.pbix` in Power BI

Author
Amrutha Venkata Sai Chillarige – Electrical and Electronics Engineering, NIT Warangal
