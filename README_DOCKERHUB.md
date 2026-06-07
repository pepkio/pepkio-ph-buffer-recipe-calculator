# Pepkio pH Buffer Recipe Calculator

Run the Pepkio pH Buffer Recipe Calculator CLI in Docker to obtain weighed acid and base masses, predicted pH at use temperature, ionic strength, and stepwise preparation protocols through the hosted API.

# What It Does

The image runs `pepkio-ph-buffer-recipe-calculator`, a client for the Pepkio pH Buffer Recipe Calculator REST API. Choose a buffer system and mode (`calculator` for dry reagents or `stock` for concentrate dilution), set target pH, concentration, final volume, and separate preparation and working temperatures; receive grams of acid and base forms, ionic strength, optional NaCl adjustment, gravimetric and titration routes, protocol steps, compatibility warnings, and shareable permalinks.

Typical workflows include Tris and HEPES buffers for protein work, phosphate buffers for biochemistry assays, cold-room use after room-temperature preparation, stock dilution with pH re-check guidance, and matching ionic strength across experimental conditions. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Buffer systems: Tris, sodium phosphate, HEPES, acetate, cacodylate, MES, and PIPES (by `buffer_id`)
- Two modes: `calculator` (prepare from dry reagents) and `stock` (dilute a concentrated stock)
- Temperature correction: separate `prep_temp_c` and `working_temp_c` with van't Hoff pKa adjustment and predicted working pH
- Weighed recipes: grams of acid form and base form; gravimetric and titration preparation routes
- Ionic strength: estimated ionic strength (mM) with optional `target_ionic_strength_mM` or `added_salt_mM` for NaCl
- Stock dilution: stock volume, diluent volume, and predicted pH after dilution
- Protocol steps and compatibility warnings (for example phosphate with certain enzyme assays)
- Named manifest examples (`tris_50mM_1L`, `phosphate_100mM`, `stock_tris_dilution`)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/ph-buffer-recipe-calculator:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/ph-buffer-recipe-calculator:0.1.0 \
  pepkio-ph-buffer-recipe-calculator run --example tris_50mM_1L
```

Manifest only (no API key):

```bash
docker run --rm pepkio/ph-buffer-recipe-calculator:0.1.0 \
  pepkio-ph-buffer-recipe-calculator manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/ph-buffer-recipe-calculator:0.1.0 \
  pepkio-ph-buffer-recipe-calculator run --input-json \
  '{"mode":"calculator","buffer_id":"tris","target_ph":7.5,"concentration_mM":50,"final_volume":1,"final_volume_unit":"L","prep_temp_c":25,"working_temp_c":4}'
```

# Typical Use Cases

- 50 mM Tris-HCl pH 7.5 in 1 L prepared at 25 °C and used at 4 °C
- 100 mM sodium phosphate pH 7.4 in 500 mL for biochemistry assays
- Diluting 1 M Tris stock to 50 mM in 100 mL with pH re-check reminder
- Matching ionic strength across buffers with optional NaCl addition
- Writing reproducible Methods sections with preparation and working temperature notes
- CI or workflow runners that need a fixed client environment

# Scientific Background

For monoprotic buffers, the acid/base ratio follows the Henderson–Hasselbalch relation at the preparation temperature. pKa values are adjusted between preparation and working temperatures using van't Hoff thermodynamics, so buffers such as Tris that shift strongly with temperature report predicted pH at the use temperature.

Ionic strength is estimated with a simplified Debye–Hückel adjustment; optional NaCl can align ionic conditions between buffers. Stock mode computes dilution volumes and reminds you to verify pH after dilution, when ionic strength and pH can change.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/ph-buffer-recipe-calculator

The web UI adds live results as you type, copy-ready protocol and Methods-style export, shareable recipe links, and inline compatibility flags for common assay conflicts.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-ph-buffer-recipe-calculator

Web Application: https://www.pepkio.com/tools/ph-buffer-recipe-calculator

PyPI package: https://pypi.org/project/pepkio-ph-buffer-recipe-calculator/

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services.
