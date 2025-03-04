from fastapi import FastAPI, HTTPException
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from fastapi.responses import StreamingResponse

#Initialize FastAPI application
app = FastAPI()

# Load data
df = pd.read_csv("Data/countries_data.csv")

# Normalize column names 
df.columns = [col.strip().lower() for col in df.columns]

# Confirm country count
if len(df) != 195:
    print(f"⚠️ Warning: Expected 195 countries, but found {len(df)} in countries_data.csv")


# Endpoints 

@app.get("/")
def root():
    return {"message": "Welcome to the World Bank Country Data API"}

@app.get("/country/{country_name}")
def get_country_data(country_name: str):
    country_data = df[df['name'].str.lower() == country_name.lower()]
    if country_data.empty:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_data.to_dict(orient="records")[0]

@app.get("/metadata")
def get_metadata():
    return {
        "total_countries": len(df),
        "regions": df['region'].unique().tolist(),
        "income_levels": df['incomelevel'].unique().tolist(),
        "countries_with_capital": len(df[df['capitalcity'].notna() & (df['capitalcity'] != "")])
    }

@app.get("/visualization/population")
def population_chart():
    try:
        df['population'] = pd.to_numeric(df['population'], errors='coerce')
        top_countries = df[['name', 'population']].dropna().sort_values(by='population', ascending=False).head(20)

        plt.figure(figsize=(12, 6))
        plt.bar(top_countries['name'], top_countries['population'])
        plt.xticks(rotation=45, ha="right")
        plt.title('Top 20 Countries by Population')
        plt.xlabel('Country')
        plt.ylabel('Population')

        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization Error: {str(e)}")

@app.get("/visualization/region-distribution")
def region_distribution():
    try:
        region_counts = df['region'].value_counts()

        plt.figure(figsize=(8, 8))
        plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Countries by Region")

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization Error: {str(e)}")

@app.get("/visualization/income-levels")
def income_levels_chart():
    try:
        income_counts = df['incomelevel'].value_counts()

        plt.figure(figsize=(10, 6))
        plt.bar(income_counts.index, income_counts.values)
        plt.title('Number of Countries by Income Level')
        plt.xlabel('Income Level')
        plt.ylabel('Number of Countries')

        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization Error: {str(e)}")
