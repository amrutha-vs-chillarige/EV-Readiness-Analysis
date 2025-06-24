CREATE DATABASE IF NOT EXISTS ev_project;
USE ev_project;

-- 1. View full dataset
SELECT * FROM ev_readiness;

-- 2. Sort by EVs per Charging Station (higher = more pressure on stations)
SELECT State, EV_Sales_Quantity, Stations, EVs_per_Station
FROM ev_readiness
ORDER BY EVs_per_Station DESC;

-- 3. Sort by Stations per Million People (higher = better accessibility)
SELECT State, Stations, Population, Stations_per_Million
FROM ev_readiness
ORDER BY Stations_per_Million DESC;