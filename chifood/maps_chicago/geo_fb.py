import food_banks
from covid import *
import geopandas
from geopy.geocoders import Nominatim
import pandas as pd
import matplotlib.pyplot as plt

chi_fb = food_banks.get_locations("https://www.chicagosfoodbank.org/find-food/")
chicago_zipcode = geopandas.read_file('Boundaries - ZIP Codes')
print(chicago_zipcode)

#code to get coordinates 
geolocator = Nominatim(user_agent="chifood")
lat = []
lon = []
for _, row in chi_fb.iterrows():
    loc = geolocator.geocode(row["address"])
    if loc != None:
        lat.append(loc.latitude)
        lon.append(loc.longitude)
    else:
        lat.append(pd.NaT)
        lon.append(pd.NaT)

chi_fb["Latitude"] = lat
chi_fb["Longitude"] = lon

chi_fb = chi_fb.dropna()
#There is one observation that "breaks" the map... Is it ok to just remove it?
chi_fb.drop(chi_fb[(chi_fb["Longitude"] == -76.1769221)].index, axis=0, inplace=True)
gdf_fb = geopandas.GeoDataFrame(
    chi_fb, geometry=geopandas.points_from_xy(chi_fb.Longitude, chi_fb.Latitude))

#to color the map for covid
api_request = build_request()
r = requests.get(api_request)
covid_data = r.json()
df_covid = process_data(covid_data)
df_covid.rename({"zip_code":"zip"}, axis=1, inplace=True)
covid_chi = chicago_zipcode.merge(df_covid[["zip", "death_rate_cumulative"]], how="inner", on="zip")

#now we graph
fig, ax = plt.subplots(figsize=(20, 15))
ax.set_title('Cichago ZIP Codes')
covid_chi.plot(ax=ax, column="death_rate_cumulative", legend=True)
gdf_fb.plot(ax=ax, marker='o', color='red', markersize=10)
fig.savefig("covid-fb.png")



