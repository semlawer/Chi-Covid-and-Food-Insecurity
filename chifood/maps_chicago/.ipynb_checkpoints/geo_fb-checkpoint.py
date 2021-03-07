import food_banks
import geopandas

chi_fb = food_banks.get_locations("https://www.chicagosfoodbank.org/find-food/")
fb_maps = geopandas.GeoDataFrame(chi_fb)
chicago_zipcode = geopandas.read_file('Boundaries - ZIP Codes')
chicago_zipcode.plot()