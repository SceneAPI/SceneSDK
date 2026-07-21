# SPDX-License-Identifier: Apache-2.0
"""Unit tests for scenesdk._ergonomics.iter_paginated."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from scenesdk._ergonomics import iter_paginated


def test_iter_paginated_dict_pages_walks_until_no_token() -> None:
    pages: dict[str | None, dict[str, Any]] = {
        None: {"items": [1, 2, 3], "next_page_token": "p2"},
        "p2": {"items": [4, 5], "next_page_token": "p3"},
        "p3": {"items": [6], "next_page_token": None},
    }
    assert list(iter_paginated(lambda token: pages[token])) == [1, 2, 3, 4, 5, 6]


def test_iter_paginated_attr_style_pages() -> None:
    # The generated SDK returns attrs-style objects, not dicts. The
    # helper must handle attribute access just as well as dict access.
    pages: dict[str | None, Any] = {
        None: SimpleNamespace(items=["a", "b"], next_page_token="p2"),
        "p2": SimpleNamespace(items=["c"], next_page_token=None),
    }
    assert list(iter_paginated(lambda token: pages[token])) == ["a", "b", "c"]


def test_iter_paginated_dict_items_method_does_not_shadow_payload() -> None:
    # Regression: getattr(dict_obj, "items", None) returns dict.items
    # method, not the items key value. The helper must check dict-ness
    # first to dispatch through .get() instead of getattr().
    page = {"items": [1, 2], "next_page_token": None}
    assert list(iter_paginated(lambda _token: page)) == [1, 2]


def test_iter_paginated_empty_page() -> None:
    assert list(iter_paginated(lambda _t: {"items": [], "next_page_token": None})) == []


def test_iter_paginated_single_page_no_token() -> None:
    assert list(iter_paginated(lambda _t: {"items": [42], "next_page_token": None})) == [42]


def test_iter_paginated_missing_items_key_does_not_crash() -> None:
    # A page object with neither attr nor key for items is treated as
    # empty rather than raising.
    pages = {
        None: {"next_page_token": "p2"},  # no items
        "p2": {"items": ["last"], "next_page_token": None},
    }
    assert list(iter_paginated(lambda t: pages[t])) == ["last"]


def test_iter_paginated_falsy_token_terminates() -> None:
    # Tokens "" and None and 0 all terminate iteration (the API contract
    # documents next_page_token as nullable string).
    for terminal in (None, "", 0):
        page = {"items": [1], "next_page_token": terminal}
        assert list(iter_paginated(lambda _t, p=page: p)) == [1]


def test_iter_paginated_stringifies_non_string_tokens() -> None:
    # If a server returns a non-string token (e.g. int seq), the helper
    # coerces to str before the next fetch (the contract is str but
    # defensive code is cheap).
    pages = {
        None: {"items": [1], "next_page_token": 42},
        "42": {"items": [2], "next_page_token": None},
    }
    assert list(iter_paginated(lambda t: pages[t])) == [1, 2]


def test_iter_paginated_propagates_fetch_errors() -> None:
    # Errors from fetch_page bubble through the generator; the helper
    # does not swallow or retry.
    def fetch(_token: str | None) -> Any:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        list(iter_paginated(fetch))
