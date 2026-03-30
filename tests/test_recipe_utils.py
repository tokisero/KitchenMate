import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))

from recipe_utils import filter_favorites_by_query, merge_missing_into_shopping


def test_filter_favorites_empty_query():
    assert filter_favorites_by_query([{"name": "Суп"}], "") == []


def test_filter_favorites_case_insensitive():
    favs = [{"name": "Борщ", "ingredients": ""}]
    assert filter_favorites_by_query(favs, "борщ")
    assert not filter_favorites_by_query(favs, "салат")


def test_merge_missing_skips_duplicate_names():
    existing = [{"name": "Молоко", "amount": "1л", "checked": False}]
    missing = [{"name": "молоко", "amount": "500мл"}, {"name": "Яйца", "amount": "6 шт"}]
    out = merge_missing_into_shopping(existing, missing)
    assert len(out) == 2
    names = [x["name"] for x in out]
    assert "Яйца" in names


def test_merge_missing_preserves_existing():
    existing = [{"name": "Хлеб", "amount": "", "checked": True}]
    out = merge_missing_into_shopping(existing, [])
    assert len(out) == 1
    assert out[0]["checked"] is True
