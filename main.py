from csv import DictReader, DictWriter
from time import sleep
import pandas as pd


import requests
from tqdm import tqdm


base_url = "https://nominatim.openstreetmap.org/search?"


def nominatim_geocode(address, format="json", limit=1, **kwargs):
    """thin wrapper around nominatim API.

    Documentation: https://wiki.openstreetmap.org/wiki/Nominatim#Parameters
    """
    params = {"q": address, "format": format, "limit": limit, **kwargs}
    headers = {"Accept-Language": "en"}
    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()  # will raise exception if status is unsuccessful

    sleep(1)  # sleep
    return response.json()


def read_csv(path):
    """read csv and return it as a list of dictionaries, one per row"""
    with open(path, "r") as f:
        return list(DictReader(f))


def write_csv(data, path, mode="w"):
    """write data to csv or append to existing one"""
    if mode not in "wa":  # 'a' mode will append to the existing file, if it exists
        raise ValueError("mode should be either 'w' or 'a'")

    with open(path, mode) as f:
        writer = DictWriter(f, fieldnames=data[0].keys())
        if mode == "w":
            writer.writeheader()

        for row in data:
            writer.writerow(row)


def geocode_bulk(data, column="address", verbose=False):
    """assuming data is an iterable of dicts, will attempt to geocode each,
    treating {column} as an address. Returns 2 iterables - result and errored rows"""
    result, errors = [], []

    for row in tqdm(data):
        try:
            search = nominatim_geocode(row[column], limit=1)
            if len(search) == 0:  # no location found:
                result.append(row)
                if verbose:
                    print(f"Can't find anything for {row[column]}")

            else:
                info = search[0]  # most "important" result
                info.update(row)  # merge two dicts
                result.append(info)
        except Exception as e:
            if verbose:
                print(e)
            row["error"] = e
            errors.append(row)

    if len(errors) > 0 and verbose:
        print(f"{len(errors)}/{len(data)} rows failed")

    return result, errors


data=read_csv('/content/cities (1).csv')
result_not_filtered=geocode_bulk(data, column='name', verbose=True)


result=result_not_filtered[0]
print(result)
lat_long_display_data = [{'Latitude': entry['lat'], 'Longitude': entry['lon'], 'Display Name': entry['name']} for entry in result]
df = pd.DataFrame(lat_long_display_data)
df.to_csv('lat_long_display_data.csv', index=False)





with open('pm_data.csv', 'w') as file:
        # Write the header row
        file.write('Latitude,Longitude,City,PM\n')

def read_coordinates():
  with open('/content/lat_long_display_data.csv', "r") as f:
        return list(DictReader(f))

lat_long_data=read_coordinates()

api_key = "91bdc7e8c526ca22ee37b861da1ea6295e14925d18c95160fdb7f1c78918f566"
for i in lat_long_data:
    latitude=i['Latitude']
    longitude=(i['Longitude'])
    display_name=(i['Display Name'])

    
    url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token=yourtoken"
    

# Send the request with the API key included in the headers
    response = requests.get(url)
    sleep(1)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'forecast' in data['data'] and 'daily' in data['data']['forecast']:
            pm10_values = data['data']['forecast']['daily']['pm10']
            if pm10_values:
                latest_pm10 = pm10_values[-1]['avg']
            else:
                latest_pm10 = 0.0
            

            with open('pm_data.csv', 'a') as file:
                file.write(f'{latitude},{longitude},{display_name},{latest_pm10}\n')
        else:
            print(f"No PM10 data available for")
    else:
        print(f"Error fetching data for {response.status_code}")








