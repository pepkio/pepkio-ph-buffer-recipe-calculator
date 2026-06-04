"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env, override=True)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env, override=True)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "ph-buffer-recipe-calculator",
        "title": "pH Buffer Recipe Calculator",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "tris_50mM_1L",
                "input": {
                    "mode": "calculator",
                    "buffer_id": "tris",
                    "target_ph": 7.5,
                    "concentration_mM": 50,
                    "final_volume": 1,
                    "final_volume_unit": "L",
                    "prep_temp_c": 25,
                    "working_temp_c": 4,
                },
                "output": {"result": {"acid_mass_g": 3}},
            },
            {
                "name": "phosphate_100mM",
                "input": {
                    "mode": "calculator",
                    "buffer_id": "phosphate",
                    "target_ph": 7.4,
                    "concentration_mM": 100,
                    "final_volume": 500,
                    "final_volume_unit": "mL",
                    "prep_temp_c": 25,
                    "working_temp_c": 25,
                },
                "output": {"result": {"acid_mass_g": 1}},
            },
            {
                "name": "stock_tris_dilution",
                "input": {
                    "mode": "stock",
                    "buffer_id": "tris",
                    "target_ph": 7.5,
                    "concentration_mM": 50,
                    "stock_concentration_mM": 1000,
                    "final_volume": 100,
                    "final_volume_unit": "mL",
                    "prep_temp_c": 25,
                    "working_temp_c": 25,
                },
                "output": {"result": {"stock_volume_mL": 5}},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "mode": "calculator",
            "result": {"acid_mass_g": 3.0},
            "warnings": [],
            "protocol_steps": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
