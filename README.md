# World Bank Country Data API

This project fetches data for **195 recognized countries** using the **World Bank API**, processes it, and exposes a FastAPI-based API that:

- Provides country-level data.
- Returns population, region, and income-level visualizations.
- Supports interactive Swagger documentation.


## Project Structure

WebScrapping project/
├── Data/
│   ├── countries_data.csv           # Created by fetch_data.py 
├── fetch_data.py                    # Fetches data
├── main.py                          # FastAPI app
├── requirements.txt                 # Dependencies
├── challenge.md



## Install Python dependencies
Run the following command in the terminal to install all the dependecies require for the project

- pip install -r requirements.txt



## Fetch Data (ETL Process)
Run the following command in the terminal to fetch data for 195 countries and save it to Data/countries_data.csv.

-  python fetch_data.py

This will:

Scrape country data from the World Bank API.
Filter out non-countries (aggregates, territories, etc).
Save the data to Data/countries_data.csv.



## Run FastAPI Application
Run the following command in the terminal to start the FastAPI server

- python -m uvicorn main:app --reload


## API Documentation
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc


## Visualizations
You can view the following charts directly in your browser after running the FastAPI application:

Visualization Endpoints
Top 20 Countries by Population - http://localhost:8000/visualization/population
Countries by Region	           - http://localhost:8000/visualization/region-distribution
Countries by Income Level      - http://localhost:8000/visualization/income-levels


## API Endpoints
Method	Endpoint	                                  Description
GET	    /	                                          Welcome message
GET	    /country/{country_name}	                      Fetch data for a specific country
GET	    /metadata	                                  Metadata (total countries, regions, income levels)
GET	    /visualization/ population	                  Population chart (Top 20)
GET	    /visualization/region-distribution	          Pie chart of countries by region
GET	    /visualization/income-levels	              Bar chart of countries by income level
