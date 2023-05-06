import requests
import re
import pandas
from sqlalchemy import create_engine
from urllib.parse import urlparse

DATABASE_UPLOAD = True

poi_end_point = "https://api.tomtom.com/search/2/poiSearch/charging%20Station.json"
availability_end_point = "https://api.tomtom.com/search/2/chargingAvailability.json"

poi_request_data = {
    "lat": 38,
    "lon": -122,
    "radius": 13500,  # radius of downtown San Francisco
    "view": "Unified",
    "relatedPois": "off",
    "key": "NbiuShqBuFQ8H7v5h62BcuiCfl9bepll",
}

df = pandas.DataFrame(
    columns=[
        "id",
        "network_name",
        "num_available",
        "num_total",
        "rated_power",
        "lat",
        "lon",
    ]
)

try:
    response = requests.get(poi_end_point, poi_request_data)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:  # Bad Response
    raise SystemExit(err)
except requests.exceptions.RequestException as err:  # Anything else
    raise SystemExit(err)

poi_results = response.json()["results"]
for res in poi_results:
    station_name = res["poi"]["name"]  # get station name
    url_home = urlparse("https://" + res["poi"]["url"]).netloc  # get url name
    url_home = url_home.removesuffix(".com").removeprefix(
        "www."
    )  # remove .www and .com
    if (
        station_name.lower() in url_home
    ):  # if the station name is in the url, it most likely is just the network name
        network_name = station_name
    else:  # otherwise use the url name
        network_name = url_home
    id = res["id"]  # used as primary key in database

    rated_power_stats = []
    for connector in res["chargingPark"]["connectors"]:
        rated_power_stats.append(connector["ratedPowerKW"])

    lat = res["position"]["lat"]
    lon = res["position"]["lon"]

    availability_request_data = {
        "chargingAvailability": re.sub(
            "[^0-9]", "", res["info"]
        ),  # this is also available in the "datasources" header, but it isn't in every response,
        # so pulling it from here is more consistent
        "key": "NbiuShqBuFQ8H7v5h62BcuiCfl9bepll",
    }

    try:
        availability_response = requests.get(
            availability_end_point, availability_request_data
        )
        availability_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    availability_results = availability_response.json()["connectors"]

    num_total = 0
    num_available = 0
    for res in availability_results:
        num_available += res["availability"]["current"][
            "available"
        ]  # sum all available connectors
        num_total += res["total"]

    df.loc[len(df.index)] = [
        id,
        network_name,
        num_available,
        num_total,
        rated_power_stats[0],
        lat,
        lon,
    ]
df = df.set_index("id")
df.to_csv("results.csv")

if DATABASE_UPLOAD:  # uploads data to database, based on flag
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    )

    df.to_sql("charger_data", con=engine, if_exists="append")
