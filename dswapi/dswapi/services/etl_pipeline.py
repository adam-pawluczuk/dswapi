import os
import json
import math
import logging
import copy
import datetime
from typing import List, Dict
from pathlib import Path

import petl
import requests
from django.conf import settings

from dswapi.models import CSVFile

log = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG")
logging.getLogger("urllib3").setLevel('WARNING')

homeworld_cache = {}


def execute_pipeline():
    """
    Main function to execute full pipeline.
    """
    response = get_page()
    response = _enrich_response(response)

    download_dir = _get_download_dir()

    now = datetime.datetime.now()
    file_name = now.strftime('%Y%m%d_%H%M%S.csv')
    full_path = download_dir / file_name

    save_as_csv(response, file_path=full_path)
    csv_file = CSVFile(file_name=file_name, download_date=now, last_edited=now)
    csv_file.save()

    return response


def _enrich_response(response: List[Dict]) -> List[Dict]:
    global homeworld_cache

    enriched = []
    for elem in response:
        homeworld_url = elem["homeworld"]
        if not homeworld_url in homeworld_cache:
            response = call_api(homeworld_url)
            homeworld_cache[homeworld_url] = response["name"]
        elem["homeworld"] = homeworld_cache.get(homeworld_url)
        enriched.append(elem)

    return enriched


def _get_download_dir() -> str:
    download_dir = settings.BASE_DIR / settings.CSV_ROOT_PATH
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)

    return download_dir


def call_api(api_url: str) -> Dict:
    """
    Call api endpoint url and return a response.
    """
    log.debug(f"Calling {api_url}...")
    r = requests.get(api_url)
    response_json = json.loads(r.content)

    return response_json


def save_as_csv(data: List[Dict], file_path: str) -> None:
    """
    Saves a CSV to a filesystem.
    """
    csv_header = data[0].keys()
    csv_table = [csv_header]

    for row in data:
        csv_row = [row[row_name] for row_name in csv_header]
        csv_table.append(csv_row)

    petl.tocsv(csv_table, file_path)


def get_page() -> List[Dict]:
    """
    Gets the raw results from the API.
    Combines multiple requests' responses into one dict().
    """
    api_url = "https://swapi.dev/api/people"
    response_json = call_api(api_url)

    next_url = response_json["next"]

    assert next_url

    page_size = len(response_json["results"])
    count = response_json["count"]

    # How many times to call the requests to get the whole collection
    # (excluding the first request)
    pending_requests_count = math.ceil(count / page_size) - 1

    base_next_url, next_url_index = next_url.split("=")
    pending_urls = (f"{base_next_url}={int(next_url_index) + offset}" for offset in range(pending_requests_count))

    responses = []
    responses.extend(response_json["results"])
    for url in pending_urls:
        response = call_api(url)
        results = response["results"]
        log.debug(f"Extending with {len(results)}...")
        responses.extend(results)

    assert len(responses) == count

    return responses
