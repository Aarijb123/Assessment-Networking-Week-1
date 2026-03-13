"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache_dict = json.load(f)
        return cache_dict


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)


def validate_postcode(postcode: str) -> bool:
    """returns a valid postcode"""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    cache = load_cache()
    if postcode in cache and "valid" in cache[postcode]:
        return cache[postcode]["valid"]

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()
    result = bool(data["result"])

    if postcode not in cache:
        cache[postcode] = {}
    cache[postcode]["valid"] = result
    save_cache(cache)

    return result


def get_postcode_for_location(lat: float, long: float) -> str:
    """returns the postcode when we enter the longitude and latitiude"""
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    response = req.get(
        f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"
    )

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if response.status_code == 200:
        if data["result"] is None:
            raise ValueError("No relevant postcode found.")
        return data["result"][0]["postcode"]
    else:
        raise ValueError("No relevant postcode found.")


def get_postcode_completions(postcode_start: str) -> list[str]:
    """returns completed postcode when user inputs start of their postcode"""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    cache = load_cache()
    if postcode_start in cache and "completions" in cache[postcode_start]:
        return cache[postcode_start]["completions"]

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()
    completions = data.get("result") or []

    if postcode_start not in cache:
        cache[postcode_start] = {}
    cache[postcode_start]["completions"] = completions
    save_cache(cache)

    return completions


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns postcode details when we input a list of postcodes"""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for p in postcodes:
        if not isinstance(p, str):
            raise TypeError("Function expects a list of strings.")

    response = req.post("https://api.postcodes.io/postcodes",
                        json={"postcodes": postcodes})

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if response.status_code == 200:
        return data["result"]
    else:
        raise ValueError("No postcode completions found.")
