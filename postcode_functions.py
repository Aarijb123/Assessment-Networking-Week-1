"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def validate_postcode(postcode: str) -> bool:

    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if response.status_code == 200:
        return data["result"]
    else:
        raise TypeError("Function expects a string.")


def get_postcode_for_location(lat: float, long: float) -> str:

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
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()
    if response.status_code == 200:
        if data["result"] is None:
            raise ValueError("No postcode completions found.")
        return data["result"]
    else:
        raise ValueError("No postcode completions found.")


def get_postcodes_details(postcodes: list[str]) -> dict:
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
