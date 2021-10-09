"""Contains all data load fixtures"""
import json
import os

import pytest


@pytest.fixture(scope="session")
def animals_page_one():
    """Returns data for Animal category Page 1"""
    path = os.path.join(os.path.dirname(__file__), "data", "animals_page_one.json")
    with open(path) as fp:
        data = json.load(fp)
    return data


@pytest.fixture(scope="session")
def animals_page_two():
    """Returns data for Animal category Page 2"""
    path = os.path.join(os.path.dirname(__file__), "data", "animals_page_two.json")
    with open(path) as fp:
        data = json.load(fp)
    return data


@pytest.fixture(scope="session")
def categories_page_one():
    """Returns data for category for  Page 1"""
    path = os.path.join(os.path.dirname(__file__), "data", "categories_page_one.json")
    with open(path) as fp:
        data = json.load(fp)
    return data


@pytest.fixture(scope="session")
def categories_page_two():
    """Returns data for category for  Page 2"""
    path = os.path.join(os.path.dirname(__file__), "data", "categories_page_two.json")
    with open(path) as fp:
        data = json.load(fp)
    return data
