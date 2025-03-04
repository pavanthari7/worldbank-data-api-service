import requests
import pandas as pd
import os
import time

# Ensure Data folder exists
os.makedirs('Data', exist_ok=True)

# List of 195 recognized countries (UN member states + 2 observers: Vatican City and Palestine)
ALLOWED_COUNTRY_CODES = [
    "AFG", "ALB", "DZA", "AND", "AGO", "ATG", "ARG", "ARM", "AUS", "AUT",
    "AZE", "BHS", "BHR", "BGD", "BRB", "BLR", "BEL", "BLZ", "BEN", "BTN",
    "BOL", "BIH", "BWA", "BRA", "BRN", "BGR", "BFA", "BDI", "CPV", "KHM",
    "CMR", "CAN", "CAF", "TCD", "CHL", "CHN", "COL", "COM", "COG", "CRI",
    "CIV", "HRV", "CUB", "CYP", "CZE", "COD", "DNK", "DJI", "DMA", "DOM",
    "ECU", "EGY", "SLV", "GNQ", "ERI", "EST", "SWZ", "ETH", "FJI", "FIN",
    "FRA", "GAB", "GMB", "GEO", "DEU", "GHA", "GRC", "GRD", "GTM", "GIN",
    "GNB", "GUY", "HTI", "HND", "HUN", "ISL", "IND", "IDN", "IRN", "IRQ",
    "IRL", "ISR", "ITA", "JAM", "JPN", "JOR", "KAZ", "KEN", "KIR", "PRK",
    "KOR", "KWT", "KGZ", "LAO", "LVA", "LBN", "LSO", "LBR", "LBY", "LIE",
    "LTU", "LUX", "MDG", "MWI", "MYS", "MDV", "MLI", "MLT", "MHL", "MRT",
    "MUS", "MEX", "FSM", "MDA", "MCO", "MNG", "MNE", "MAR", "MOZ", "MMR",
    "NAM", "NRU", "NPL", "NLD", "NZL", "NIC", "NER", "NGA", "MKD", "NOR",
    "OMN", "PAK", "PLW", "PAN", "PNG", "PRY", "PER", "PHL", "POL", "PRT",
    "QAT", "ROU", "RUS", "RWA", "KNA", "LCA", "VCT", "WSM", "SMR", "STP",
    "SAU", "SEN", "SRB", "SYC", "SLE", "SGP", "SVK", "SVN", "SLB", "SOM",
    "ZAF", "SSD", "ESP", "LKA", "SDN", "SUR", "SWE", "CHE", "SYR", "TJK",
    "THA", "TLS", "TGO", "TON", "TTO", "TUN", "TUR", "TKM", "TUV", "UGA",
    "UKR", "ARE", "GBR", "TZA", "USA", "URY", "UZB", "VUT", "VAT", "VEN",
    "VNM", "YEM", "ZMB", "ZWE", "PSE"  # Including Palestine and Vatican
]

def fetch_country_data():
    url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch country list: {response.status_code}")

    data = response.json()

    countries_data = []

    for country in data[1]:
        if country['id'] not in ALLOWED_COUNTRY_CODES:
            continue  # Skip non-country entities like aggregates or territories

        country_id = country['id']
        population = fetch_population(country_id)

        countries_data.append({
            "id": country_id,
            "name": country["name"],
            "region": country["region"]["value"],
            "incomeLevel": country["incomeLevel"]["value"],
            "capitalCity": country["capitalCity"],
            "longitude": float(country["longitude"]) if country["longitude"] else None,
            "latitude": float(country["latitude"]) if country["latitude"] else None,
            "population": population
        })

        time.sleep(0.3)  # Add delay to avoid hitting World Bank API limits

    return countries_data


def fetch_population(country_code):
    """
    Fetches latest population for a given country code.
    Returns None if population data is unavailable.
    """
    population = None
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?format=json&per_page=1"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch population for {country_code}: HTTP {response.status_code}")
        return population

    try:
        data = response.json()

        if not isinstance(data, list) or len(data) < 2 or not data[1]:
            print(f"⚠️ No population data for {country_code}")
            return population

        population = data[1][0].get('value')
        print(f"✅ Population for {country_code}: {population}")
        return population

    except (IndexError, KeyError, ValueError) as e:
        print(f"⚠️ Error parsing population for {country_code}: {e}")
        return population


if __name__ == "__main__":
    print("📥 Fetching data for 195 countries...")
    countries_data = fetch_country_data()

    df = pd.DataFrame(countries_data)
    df.to_csv("Data/countries_data.csv", index=False)
    print("✅ Data saved to Data/countries_data.csv (only 195 countries)")
