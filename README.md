# Pepkio pH Buffer Recipe Calculator

Python client for the Pepkio pH Buffer Recipe Calculator API: weighed buffer recipes with temperature-corrected pH, ionic strength, stock dilution, and copy-ready protocols.

# Overview

Preparing a biological buffer at a specific pH and concentration is a routine task in molecular biology, biochemistry, and cell culture. Researchers commonly work with Tris-HCl, sodium phosphate, HEPES, MES, and other Good's buffers to maintain stable pH during protein purification, enzyme assays, electrophoresis, PCR, and storage. The correct recipe depends on the buffer's pKa, the ratio of acid and base forms, final concentration, total volume, and—critically—the temperature at which the buffer is prepared versus the temperature at which it will be used.

Calculating buffer recipes by hand or in a spreadsheet introduces several practical problems. pKa values in reference tables are often reported at 25 °C, but many experiments run at 4 °C (cold room, ice bath) or 37 °C (cell culture). Tris, in particular, shows a large pH shift with temperature; a buffer adjusted to pH 7.5 at room temperature can read near pH 9 on ice. Ionic strength affects effective pKa and enzyme activity, yet simple calculators rarely report it or offer NaCl adjustment to match conditions across buffers. When diluting a concentrated stock, pH and ionic strength can change after dilution, but generic dilution calculators do not warn you to re-measure.

The [Pepkio pH Buffer Recipe Calculator](https://www.pepkio.com/tools/ph-buffer-recipe-calculator) web application computes weighed recipes (grams of acid and base forms), temperature-corrected pKa, predicted working pH, ionic strength, optional NaCl addition, stock dilution volumes, gravimetric and titration preparation routes, and step-by-step protocols. This repository provides the **Python client** (`pepkio-ph-buffer-recipe-calculator`) that calls the same calculation engine through the Pepkio Tools REST API, so you can generate buffer recipes from scripts, Jupyter notebooks, or automated lab workflows.

If you prefer a graphical interface, use the hosted tool at [https://www.pepkio.com/tools/ph-buffer-recipe-calculator](https://www.pepkio.com/tools/ph-buffer-recipe-calculator). If you need reproducible, programmatic access, install the package from [PyPI](https://pypi.org/project/pepkio-ph-buffer-recipe-calculator/) and follow the Quick Start below.

# Features

## Buffer recipe calculation (API-backed)

- **Buffer systems:** Tris, sodium phosphate, HEPES, and other common laboratory buffers (selected by `buffer_id`)
- **Two modes:** `calculator` (prepare from dry reagents) and `stock` (dilute a concentrated stock to working concentration)
- **Temperature correction:** separate preparation temperature (`prep_temp_c`) and working temperature (`working_temp_c`) with van't Hoff pKa adjustment and predicted pH at use temperature
- **Weighed recipes:** grams of acid form and base form for gravimetric preparation
- **Dual preparation routes:** gravimetric (weigh acid + base) and titration (weigh acid form, titrate with NaOH or HCl)
- **Ionic strength:** estimated ionic strength (mM) with optional `target_ionic_strength_mM` or `added_salt_mM` for NaCl adjustment
- **Stock dilution:** `stock_concentration_mM`, stock volume, diluent volume, and pH re-check reminder
- **Protocol steps:** copy-ready bench instructions including temperature notes and predicted pH shift
- **Compatibility warnings:** flags common assay conflicts (for example Tris with aldehyde-reactive crosslinkers, phosphate with certain metal-dependent enzymes)
- **Shareable runs:** each API run returns a `permalink` that restores the exact recipe

## Python package

- Fetch the tool manifest and list named examples (`get_manifest`, `list_examples`, `get_example_input`)
- Run calculations synchronously (`run`) with custom JSON or manifest examples
- Poll runs for async tools (`get_run`, `wait_for_run`)
- CLI for manifest inspection and one-off runs (`pepkio-ph-buffer-recipe-calculator`)
- Configurable API base URL and API keys via environment variables

# Common Use Cases

### 50 mM Tris-HCl pH 7.5 in 1 L (`tris_50mM_1L`)

Prepare 1 L of 50 mM Tris buffer at pH 7.5, adjusted at 25 °C and used at 4 °C—typical for protein storage or cold-room chromatography where the working pH differs from the preparation pH.

### 100 mM sodium phosphate pH 7.4 (`phosphate_100mM`)

Make 500 mL of 100 mM phosphate buffer at pH 7.4 for biochemistry assays, enzyme kinetics, or general laboratory use at constant temperature.

### Dilute 1 M Tris stock to 50 mM (`stock_tris_dilution`)

Calculate how much 1 M Tris stock to pipette into water to obtain 50 mM in 100 mL, with a reminder to verify pH after dilution.

### Matching ionic strength across buffers

Set `target_ionic_strength_mM` so NaCl is added to align ionic conditions between Tris and phosphate buffers in a comparative enzyme assay.

### Methods section documentation

Generate a weighed recipe and protocol steps suitable for copying into a lab notebook or publication Methods section, including preparation and working temperature notes.

# Why This Tool Exists

Free online buffer calculators often return a single pH value at one temperature and omit ionic strength. They do not distinguish preparation temperature from working temperature, which matters for Tris and other buffers with large ΔpKa/°C. Desktop tools such as Liverpool BufferCalc provide accurate Henderson-Hasselbalch calculations but lack stock dilution mode, inline biological compatibility notes, and shareable web links.

Spreadsheets require manual lookup of pKa, acid/base molecular weights, and Henderson-Hasselbalch algebra. Errors in unit conversion (mM vs M, mL vs L) or using the wrong pKa temperature are common. When prep and use temperatures differ, researchers may discover at the bench that the buffer is outside the intended pH range.

The Pepkio pH Buffer Recipe Calculator applies van't Hoff temperature correction and simplified Debye-Hückel ionic strength adjustment, returns both gravimetric and titration routes, calculates stock dilution volumes with pH re-check guidance, and flags compatibility issues before mixing. Shareable permalinks record the parameters for a given recipe. The Python package in this repository calls the same API for scripted or automated workflows.

# Installation

Install from PyPI:

```bash
pip install pepkio-ph-buffer-recipe-calculator
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-ph-buffer-recipe-calculator
```

## API key

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production (or default) API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |
| `PEPKIO_SSL_VERIFY` | Set to `0` or `false` to disable TLS verify (local dev disables verify for `localtest.me` by default) |

Local development against a staging stack:

```bash
export PEPKIO_API_BASE_URL=https://tools.localtest.me
export PEPKIO_API_KEY="$LOCAL_PEPKIO_API_KEY"
```

Web UI (local): [https://www.localtest.me/tools/ph-buffer-recipe-calculator](https://www.localtest.me/tools/ph-buffer-recipe-calculator)

# Quick Start

Manifest inspection does **not** require an API key. Running the tool does.

### Python: manifest example

```python
from pepkio_ph_buffer_recipe_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("tris_50mM_1L")
    result = client.run(inp)
    print(result.status, result.permalink)
    inner = result.result["result"]
    print(f"Acid: {inner['acid_mass_g']:.3f} g {inner['acid_form_label']}")
    print(f"Base: {inner['base_mass_g']:.3f} g {inner['base_form_label']}")
    for step in result.result["protocol_steps"]:
        print(step)
```

### Python: custom calculator input

```python
from pepkio_ph_buffer_recipe_calculator import PepkioClient

inp = {
    "mode": "calculator",
    "buffer_id": "phosphate",
    "target_ph": 7.4,
    "concentration_mM": 100,
    "final_volume": 500,
    "final_volume_unit": "mL",
    "prep_temp_c": 25,
    "working_temp_c": 25,
}

with PepkioClient() as client:
    result = client.run(inp)
    assert result.status == "completed"
    print(result.result["metadata"]["ionic_strength_mM"])
```

### Python: stock dilution

```python
from pepkio_ph_buffer_recipe_calculator import PepkioClient

inp = {
    "mode": "stock",
    "buffer_id": "tris",
    "target_ph": 7.5,
    "concentration_mM": 50,
    "stock_concentration_mM": 1000,
    "final_volume": 100,
    "final_volume_unit": "mL",
    "prep_temp_c": 25,
    "working_temp_c": 25,
}

with PepkioClient() as client:
    result = client.run(inp)
    r = result.result["result"]
    print(f"Stock: {r['stock_volume_mL']} mL")
    print(f"Diluent: {r['diluent_volume_mL']} mL")
```

### CLI

```bash
# Manifest (no API key)
pepkio-ph-buffer-recipe-calculator manifest
pepkio-ph-buffer-recipe-calculator manifest --examples

# Run a named example (API key required)
pepkio-ph-buffer-recipe-calculator run --example tris_50mM_1L

# Run custom JSON input
pepkio-ph-buffer-recipe-calculator run --input-json '{"mode":"calculator","buffer_id":"tris","target_ph":7.5,"concentration_mM":50,"final_volume":1,"final_volume_unit":"L","prep_temp_c":25,"working_temp_c":4}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

A completed run for the `tris_50mM_1L` manifest example (50 mM Tris-HCl pH 7.5, 1 L, prepared at 25 °C, used at 4 °C) returns a structure similar to:

```json
{
  "run_id": "b82b7827-a96e-4609-b295-2c39fc6c12c1",
  "status": "completed",
  "permalink": "https://tools.pepkio.com/r/b82b7827-a96e-4609-b295-2c39fc6c12c1",
  "result": {
    "mode": "calculator",
    "buffer_label": "Tris (tris(hydroxymethyl)aminomethane)",
    "protocol_steps": [
      "Tris (tris(hydroxymethyl)aminomethane): 50 mM, pH 7.5, 1000.0 mL",
      "Prepared at 25°C; working temperature 4°C",
      "pKa (prep) = 8.06; ionic strength ≈ 20 mM",
      "Weigh 6.178 g Tris hydrochloride and 1.308 g Tris base.",
      "Dissolve in ~80% of final volume (1000 mL) using 25°C water.",
      "Adjust to final volume 1000.0 mL; verify pH at 25°C (target pH 7.5).",
      "At working temperature 4°C, expect pH ≈ 8.95 (Δ +1.45)."
    ],
    "metadata": {
      "pka_prep_c": 8.06,
      "pka_working_c": 9.51,
      "ionic_strength_mM": 19.6,
      "predicted_working_ph": 8.95,
      "ph_shift_prep_to_working": 1.45
    },
    "result": {
      "acid_form_label": "Tris hydrochloride",
      "base_form_label": "Tris base",
      "acid_mass_g": 6.178,
      "base_mass_g": 1.308,
      "concentration_mM": 50,
      "target_ph": 7.5,
      "routes": [
        {
          "method": "gravimetric",
          "steps": [
            "Weigh 6.178 g Tris hydrochloride and 1.308 g Tris base.",
            "Dissolve in ~80% of final volume (1000 mL) using 25°C water.",
            "Adjust to final volume 1000.0 mL; verify pH at 25°C (target pH 7.5).",
            "At working temperature 4°C, expect pH ≈ 8.95 (Δ +1.45)."
          ]
        },
        {
          "method": "titration",
          "steps": [
            "Weigh 6.178 g Tris hydrochloride (acid form).",
            "Dissolve in ~80% of final volume; titrate with NaOH or HCl to pH 7.5 at 25°C.",
            "Bring to 1000.0 mL final volume.",
            "Avoid overshooting pH — correcting back changes ionic strength and capacity."
          ]
        }
      ],
      "compatibility_warnings": [
        "Tris reacts with aldehydes and some amine-reactive crosslinkers; not ideal for protein carbonylation assays."
      ]
    }
  }
}
```

Stock mode (`stock_tris_dilution`) additionally returns `stock_volume_mL`, `diluent_volume_mL`, and `ph_recheck_required: true`.

The `permalink` field links to a saved run that colleagues can open in the browser to review the same parameters and protocol.

# Scientific Background

## Henderson-Hasselbalch equation

For a weak acid buffer, pH is related to the acid dissociation constant and the ratio of conjugate base to acid:

**pH = pKa + log([A⁻] / [HA])**

where pKa = −log₁₀(Ka), [A⁻] is the conjugate base concentration, and [HA] is the acid concentration. To prepare a buffer at a target pH, choose the acid/base ratio that satisfies this equation, then calculate the masses of each form needed for the desired total buffer concentration and volume.

## pKa and temperature (van't Hoff correction)

pKa changes with temperature. A common approximation uses the van't Hoff equation:

**d(pKa)/dT ≈ −ΔH° / (2.303 × R × T²)**

For Tris, the pH of a solution prepared and measured at 25 °C will read higher (more basic) when cooled to 4 °C. The Pepkio calculator accepts separate preparation and working temperatures and reports predicted working pH and ΔpH. Always verify pH with a calibrated meter at the temperature of use when precision matters.

## Ionic strength

Ionic strength I (mol/L) summarizes the effect of all ions in solution on electrostatic interactions:

**I = ½ Σ cᵢ zᵢ²**

where cᵢ is the molar concentration of ion i and zᵢ is its charge. Ionic strength shifts effective pKa (activity corrections) and can affect enzyme activity, binding assays, and protein stability. The calculator estimates ionic strength from the buffer composition and optionally adds NaCl via `target_ionic_strength_mM` or `added_salt_mM` to match conditions across experiments.

## Gravimetric vs titration preparation

**Gravimetric:** weigh calculated masses of acid and base forms, dissolve, and bring to final volume. This route is reproducible and avoids overshooting pH during titration.

**Titration:** weigh the acid form, dissolve partially, titrate with NaOH or HCl to target pH, then adjust to final volume. Useful when only one reagent form is on hand, but overshooting pH and correcting back changes ionic strength and buffer capacity.

## Stock dilution

Diluting a concentrated buffer stock with water (or diluent) reduces concentration by the dilution factor:

**C_working = C_stock × (V_stock / V_final)**

After dilution, pH and ionic strength may shift slightly. The stock mode calculates `stock_volume_mL` and `diluent_volume_mL` and recommends re-checking pH with a calibrated meter rather than assuming the stock pH is unchanged.

## Common buffer systems

| Buffer | Typical pH range | Notes |
|--------|------------------|-------|
| Tris-HCl | 7.0–9.0 | Large temperature coefficient; not ideal with aldehydes or some crosslinkers |
| Phosphate | 5.8–8.0 | Good buffering capacity near pKa₂; can interfere with some metal-dependent enzymes |
| HEPES | 6.8–8.2 | Often used in cell culture; lower temperature sensitivity than Tris |
| MES | 5.5–6.7 | Common for biochemical assays near neutral-to-acidic pH |

Select `buffer_id` in the API or web tool to match your system.

# Frequently Asked Questions

### How do I calculate how much Tris to weigh for a buffer?

Enter buffer system (`tris`), target pH, concentration in mM, final volume, and preparation/working temperatures. The calculator returns grams of Tris hydrochloride (acid form) and Tris base using the Henderson-Hasselbalch equation with temperature-corrected pKa. Example: 50 mM Tris pH 7.5 in 1 L at 25 °C requires approximately 6.18 g Tris-HCl and 1.31 g Tris base.

### Why does Tris pH change with temperature?

Tris has a large temperature coefficient (ΔpKa ≈ −0.03 per °C). A buffer adjusted to pH 7.5 at 25 °C can read near pH 9 at 4 °C. Always measure pH at the temperature of use, or use a calculator that accounts for preparation vs working temperature.

### What is the Henderson-Hasselbalch equation?

pH = pKa + log([base]/[acid]). It relates pH to the ratio of conjugate base to acid forms for a weak acid buffer. Given a target pH and pKa, you can calculate the required acid/base ratio and then the masses for a given concentration and volume.

### How do I prepare a phosphate buffer at pH 7.4?

Select `buffer_id: "phosphate"`, set `target_ph: 7.4`, enter concentration (for example 100 mM), final volume, and temperatures. The calculator returns weighed amounts of monobasic and dibasic phosphate forms (or titration instructions) and estimated ionic strength.

### How do I dilute a 1 M Tris stock to 50 mM?

Use stock mode: set `mode: "stock"`, `stock_concentration_mM: 1000`, `concentration_mM: 50`, and final volume. For 100 mL final volume, pipette 5 mL stock and add 95 mL diluent. Re-check pH after dilution; do not assume stock pH is unchanged.

### What is ionic strength and why does it matter?

Ionic strength measures total ion charge in solution. It affects effective pKa, enzyme kinetics, and protein stability. Matching ionic strength across buffers in comparative experiments reduces confounding variables. Use `target_ionic_strength_mM` to add NaCl to a specified level.

### What is the difference between gravimetric and titration buffer preparation?

Gravimetric preparation weighs both acid and base forms to the calculated ratio—fast and reproducible. Titration weighs one form and adjusts pH with NaOH or HCl—flexible when only one reagent is available, but overshooting pH can alter ionic strength.

### How do I match ionic strength between Tris and phosphate buffers?

Calculate each buffer with the same `target_ionic_strength_mM`. The tool adds the required NaCl to reach the target. Verify final ionic strength in the result metadata.

### Can I use this for HEPES or MES buffers?

Yes. Select the appropriate `buffer_id` (for example `hepes`). Supported systems include common Good's buffers used in molecular biology and cell culture.

### Why should I re-check pH after diluting a buffer stock?

Dilution changes ionic strength and activity coefficients, which can shift pH slightly. Activity and temperature effects are not always preserved linearly upon dilution. A calibrated pH meter at the working temperature is the definitive check.

### What pH should I use for protein purification?

Depends on the protein's pI and stability. Tris and HEPES near pH 7–8 are common for neutral proteins. Avoid buffers with known incompatibilities (for example Tris with aldehyde fixatives). Check compatibility warnings in the tool output.

### Is Tris compatible with all protein assays?

No. Tris reacts with aldehydes and some amine-reactive crosslinkers. Phosphate can chelate or interfere with metal-dependent enzymes. The calculator flags common compatibility issues for the selected buffer system.

### How does temperature correction work in this calculator?

The tool applies van't Hoff pKa correction from preparation temperature to working temperature and reports predicted working pH and ΔpH. pKa at preparation temperature is shown in metadata (`pka_prep_c`, `pka_working_c`).

### What units does the calculator use?

Concentration in mM, volume in mL or L (`final_volume_unit`), temperature in °C. Output masses are in grams. Ionic strength is reported in mM.

### Do I need an API key for the Python client?

No key is required for `get_manifest()` or the CLI `manifest` command. `run()` and the CLI `run` command require an API key with tools:run scope.

### Can I run the tool offline?

The Python package calls the hosted Pepkio Tools API; an internet connection and valid API key are required for runs. Calculations are not bundled for fully offline use in this package.

### How do I share a buffer recipe with a colleague?

Open the web tool and use the shareable link feature, or share the `permalink` returned from an API run. The link restores the same buffer system, pH, concentration, volume, and temperature settings.

### What is pKa and where do I find it?

pKa is the negative logarithm of the acid dissociation constant. Tabulated values are usually at 25 °C. The calculator uses built-in pKa data with temperature correction rather than requiring manual lookup.

### How accurate are calculated buffer masses?

Masses are computed from molecular weights and the Henderson-Hasselbalch ratio. Round to your balance precision (typically 0.001 g). Final pH should always be verified with a calibrated meter; small deviations from ideal behavior (non-ideality, water quality, CO₂ absorption) can shift measured pH.

### What is the difference between this and a simple buffer calculator?

Simple calculators often use fixed pKa at one temperature, omit ionic strength, lack stock dilution mode, and do not warn about biological incompatibilities. Pepkio pH Buffer Recipe Calculator adds temperature correction, ionic strength estimation, dual preparation routes, stock dilution with pH re-check guidance, and shareable protocols.

# Web Application

For interactive buffer planning without writing code, use the hosted Pepkio pH Buffer Recipe Calculator.

The web interface lets you choose a buffer system (Tris, phosphate, HEPES, and others), enter target pH, concentration, final volume, and separate preparation and working temperatures. Results update as you type: grams of acid and base forms, ionic strength, predicted pH at use temperature, and step-by-step gravimetric or titration instructions.

The web version provides an interactive interface with live-updating results, shareable links, copy-ready protocol text, and a Methods-style sentence for publications. You can optionally set a target ionic strength to add NaCl, or switch to stock mode to calculate how much concentrate to pipette and whether to re-check pH after dilution. Compatibility notes flag common assay conflicts before mixing.

**Web Application:** [https://www.pepkio.com/tools/ph-buffer-recipe-calculator](https://www.pepkio.com/tools/ph-buffer-recipe-calculator)

# Related Resources

- **GitHub Repository:** [https://github.com/pepkio/pepkio-ph-buffer-recipe-calculator](https://github.com/pepkio/pepkio-ph-buffer-recipe-calculator)
- **PyPI Package:** [https://pypi.org/project/pepkio-ph-buffer-recipe-calculator/](https://pypi.org/project/pepkio-ph-buffer-recipe-calculator/)
- **Web Application:** [https://www.pepkio.com/tools/ph-buffer-recipe-calculator](https://www.pepkio.com/tools/ph-buffer-recipe-calculator)

# About Pepkio

[Pepkio](https://www.pepkio.com) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (RNA-seq, single-cell RNA-seq, spatial transcriptomics, functional enrichment, and custom workflows).

# Citation

If you use Pepkio pH Buffer Recipe Calculator in a publication or protocol, cite the web tool and optionally the Python package version:

```bibtex
@misc{pepkio_ph_buffer_recipe_calculator,
  title        = {Pepkio pH Buffer Recipe Calculator},
  author       = {Pepkio},
  year         = {2026},
  howpublished = {\url{https://www.pepkio.com/tools/ph-buffer-recipe-calculator}},
  note         = {Python client: pepkio-ph-buffer-recipe-calculator on PyPI}
}
```

# License

See the [GitHub repository](https://github.com/pepkio/pepkio-ph-buffer-recipe-calculator) for license terms.

# Keywords

pH buffer calculator, buffer recipe calculator, Tris buffer calculator, Tris-HCl preparation, phosphate buffer pH 7.4, HEPES buffer recipe, Henderson-Hasselbalch calculator, buffer pKa temperature correction, van't Hoff pKa, ionic strength calculator, NaCl buffer adjustment, gravimetric buffer preparation, buffer titration protocol, stock buffer dilution, dilute Tris stock, Good's buffer calculator, biological buffer preparation, molecular biology buffer, biochemistry buffer recipe, protein buffer pH, enzyme assay buffer, cell culture buffer, cold room buffer pH, Tris temperature coefficient, sodium phosphate buffer, buffer compatibility warnings, buffer ionic strength mM, weigh Tris for pH 7.5, prepare 50 mM Tris, 100 mM phosphate buffer, buffer protocol generator, lab buffer calculator, Pepkio, pepkio-ph-buffer-recipe-calculator, Python buffer API, shareable buffer recipe, Methods section buffer, bench buffer protocol, pH meter buffer preparation, conjugate acid base ratio, buffer capacity, Debye-Hückel ionic strength, laboratory solution preparation

how to calculate Tris buffer pH at 4 degrees, how much Tris hydrochloride to weigh for 50 mM pH 7.5, prepare phosphate buffer pH 7.4 100 mM recipe, dilute 1 M Tris stock to 50 mM volume calculator, why Tris pH changes with temperature, Henderson-Hasselbalch equation buffer example, match ionic strength between Tris and phosphate buffers, gravimetric vs titration buffer preparation, how to add NaCl to reach target ionic strength, re-check pH after diluting buffer stock, Tris buffer for protein purification pH, HEPES buffer recipe for cell culture, phosphate buffer enzyme assay compatibility, calculate buffer acid and base grams, pKa correction for cold room buffer use, predicted working pH after temperature change, copy buffer protocol for lab notebook, shareable buffer recipe link for colleagues, Python script generate buffer recipe, API for laboratory buffer calculation, Pepkio pH buffer recipe calculator, Tris aldehyde crosslinker incompatibility, phosphate buffer metal enzyme interference, prepare 1 liter Tris buffer step by step, stock buffer dilution pH shift warning, temperature corrected pKa Tris HEPES, ionic strength of 50 mM Tris buffer, write Methods section buffer preparation, buffer calculator with prep and working temperature, online buffer recipe with weighed masses

# Contributing

Clone the repository, run `uv sync`, and execute `uv run pytest` for unit and integration tests. Integration tests require `PEPKIO_API_KEY` or `LOCAL_PEPKIO_API_KEY` in the environment.
