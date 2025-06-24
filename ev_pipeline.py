import pandas as pd
import mysql.connector

# === STEP 1: Load Datasets ===
sales = pd.read_csv('../data/EV_Dataset.csv')
charging = pd.read_csv('../data/charging_by_state.csv')
population = pd.read_csv('../data/population.csv')

# === STEP 2: Clean EV Sales Data ===
sales = sales.dropna(subset=['EV_Sales_Quantity', 'State'])
sales_grouped = sales.groupby('State')['EV_Sales_Quantity'].sum().reset_index()

# === STEP 3: Clean Charging Station Data ===
charging = charging.rename(columns={
    charging.columns[0]: 'State',
    charging.columns[1]: 'Stations'
})
charging = charging[['State', 'Stations']]

# === STEP 4: Clean Population Data ===
population = population.rename(columns={
    population.columns[0]: 'State',
    population.columns[1]: 'Population'
})
population['Population'] = population['Population'].astype(int)

# === STEP 5: State Name Mapping ===
state_name_mapping = {
    "NCT of Delhi": "Delhi",
    "Orissa": "Odisha",
    "Dadra & Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Jammu & Kashmir": "Jammu and Kashmir",
    "Pondicherry": "Puducherry",
    "Andaman and Nicobar Islands": "Andaman & Nicobar Island",
    "Dadra and Nagar Haveli and Daman and Diu": "DNH and DD"
}

# Apply mapping and strip whitespace
for df in [sales_grouped, charging, population]:
    df['State'] = df['State'].str.strip()
    df['State'] = df['State'].replace(state_name_mapping)

# === DEBUG: Print unique state values before merge
print("States in sales_grouped:", sales_grouped['State'].unique())
print("States in charging:", charging['State'].unique())
print("States in population:", population['State'].unique())

# === STEP 6: Merge All Datasets ===
merged = pd.merge(sales_grouped, charging, on='State', how='left')
merged = pd.merge(merged, population, on='State', how='left')

# === STEP 7: Ensure Numeric Columns ===
merged['EV_Sales_Quantity'] = pd.to_numeric(merged['EV_Sales_Quantity'], errors='coerce')
merged['Stations'] = pd.to_numeric(merged['Stations'], errors='coerce')
merged['Population'] = pd.to_numeric(merged['Population'], errors='coerce')

# === STEP 8: Compute Metrics ===
merged['EVs_per_Station'] = round(merged['EV_Sales_Quantity'] / merged['Stations'], 2)
merged['Stations_per_Million'] = round((merged['Stations'] / merged['Population']) * 1e6, 2)

# === STEP 9: Save to CSV ===
merged.to_csv('../data/clean_ev_data.csv', index=False)
print("✅ CSV file created: clean_ev_data.csv")

# === STEP 10: Drop Nulls ===
print("🔍 Null counts before dropping:")
print(merged[['State', 'EV_Sales_Quantity', 'Stations', 'Population']].isnull().sum())
merged = merged.dropna(subset=['Stations', 'Population'])

# === DEBUG: Print remaining rows after dropping
print("🧾 After merging and dropping nulls, remaining rows:")
print(merged[['State', 'Stations', 'Population']])

# === Final check before inserting
print(f"📊 Number of rows ready to insert: {len(merged)}")
print(merged.head())

# === STEP 11: Insert Into MySQL ===
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='silver@13D',
    database='ev_project'
)
cursor = conn.cursor()

# Drop and recreate the table
cursor.execute("DROP TABLE IF EXISTS ev_readiness")
cursor.execute("""
CREATE TABLE ev_readiness (
    State VARCHAR(255),
    EV_Sales_Quantity INT,
    Stations INT,
    Population BIGINT,
    EVs_per_Station FLOAT,
    Stations_per_Million FLOAT
)
""")

# Insert data
for _, row in merged.iterrows():
    try:
        cursor.execute("""
            INSERT INTO ev_readiness (State, EV_Sales_Quantity, Stations, Population, EVs_per_Station, Stations_per_Million)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row['State'],
            int(row['EV_Sales_Quantity']),
            int(row['Stations']),
            int(row['Population']),
            float(row['EVs_per_Station']),
            float(row['Stations_per_Million'])
        ))
        print(f"✅ Inserted: {row['State']}")
    except Exception as e:
        print(f"❌ Error inserting row for {row['State']}: {e}")

conn.commit()
cursor.close()
conn.close()
print("✅ All data inserted into MySQL.")
