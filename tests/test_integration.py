"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_ph_buffer_recipe_calculator.client import PepkioClient
from pepkio_ph_buffer_recipe_calculator.exceptions import PepkioAPIError

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        try:
            client.get_manifest(refresh=True)
        except PepkioAPIError as exc:
            if exc.status_code == 404 and exc.code == "TOOL_NOT_FOUND":
                pytest.skip(f"Tool not deployed on {env_name} ({base_url})")
            raise
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "ph-buffer-recipe-calculator"
    names = live_client.list_examples()
    for expected in ("tris_50mM_1L", "phosphate_100mM", "stock_tris_dilution"):
        assert expected in names


def test_run_tris_50mM_1L(live_client: PepkioClient):
    inp = live_client.get_example_input("tris_50mM_1L")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("mode") == "calculator"
    inner = result.result.get("result")
    assert isinstance(inner, dict)
    acid_mass_g = inner.get("acid_mass_g")
    assert isinstance(acid_mass_g, (int, float))
    assert acid_mass_g > 0
    assert result.result.get("error") is None


def test_run_phosphate_100mM(live_client: PepkioClient):
    inp = live_client.get_example_input("phosphate_100mM")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mode") == "calculator"
    acid_mass_g = result.result.get("result", {}).get("acid_mass_g")
    assert isinstance(acid_mass_g, (int, float))
    assert acid_mass_g > 0


def test_run_stock_tris_dilution(live_client: PepkioClient):
    inp = live_client.get_example_input("stock_tris_dilution")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mode") == "stock"
    vol = result.result.get("result", {}).get("stock_volume_mL")
    assert isinstance(vol, (int, float))
    assert abs(vol - 5.0) < 0.5
