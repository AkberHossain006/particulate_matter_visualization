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
lat_long_display_data = [{'Latitude': entry['lat'], 'Longitude': entry['lon'], 'Display Name': entry['display_name']} for entry in result]
df = pd.DataFrame(lat_long_display_data)
df.to_csv('lat_long_display_data.csv', index=False)




def read_coordinates():
  with open('/content/lat_long_display_data.csv', "r") as f:
        return list(DictReader(f))

with open('pm_data.csv', 'w') as file:
        # Write the header row
        file.write('Latitude,Longitude,Display Name,PM\n')
lat_long_data=read_coordinates()
for i in lat_long_data:
    latitude=i['Latitude']
    longitude=(i['Longitude'])
    display_name=(i['Display Name'])

    url = f'https://api.openaq.org/v2/latest?coordinates={latitude},{longitude}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        if len(data['results']==0):
          pm=0.0
        else:
          parameter_list=data['results'][0]['measurements']
          for i in parameter_list:
              if i['parameter']=='pm25':
                pm=i['value']
              elif i['parameter']=='pm10':
                pm=i['value']
              else:
                pm=0.0



    else:
        print('Error:', response.status_code)


    file.write(f'{latitude},{longitude},{display_name},{pm}\n')

