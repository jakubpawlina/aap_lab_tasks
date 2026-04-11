# -*- coding: utf-8 -*-
"""conftest.py -- centralny plik konfiguracyjny pytest.

Fixtures zdefiniowane tutaj sa automatycznie dostepne we WSZYSTKICH
plikach testowych w tym katalogu (i podkatalogach).
Nie trzeba ich importowac -- pytest wykrywa je sam.
"""

import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    """Fixture tworzacy instancje Calculator -- dostepny globalnie."""
    return Calculator()


def pytest_addoption(parser):
    """Dodaje opcje wlaczajaca testy zadania dodatkowego."""
    parser.addoption(
        "--run-additional",
        action="store_true",
        default=False,
        help="uruchom testy oznaczone jako additional",
    )


def pytest_collection_modifyitems(config, items):
    """Domyslnie odfiltrowuje testy zadania dodatkowego."""
    if config.getoption("--run-additional"):
        return

    selected_items = []
    deselected_items = []
    for item in items:
        if "additional" in item.keywords:
            deselected_items.append(item)
        else:
            selected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items
