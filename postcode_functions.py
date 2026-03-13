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
        raise TypeError(postcode, str)

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate")

    data = response.json()

    if response.status_code == 200:
        return data["result"]
    elif response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    else:
        raise TypeError("Function expects a string.")


def get_postcode_for_location(lat: float, long: float) -> str:

    if not isinstance(lat, float):
        raise TypeError("Function expects two floats.")
    if not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    response = req.get(
        f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"
    )

    data = response.json()

    if response.status_code == 200:
        return data["result"]
    elif response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    else:
        raise ValueError("No relevant postcode found.")


def get_postcode_completions(postcode_start: str) -> list[str]:
    pass


def get_postcodes_details(postcodes: list[str]) -> dict:
    pass
