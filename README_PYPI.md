# Pepkio pH Buffer Recipe Calculator

Python client for the Pepkio pH Buffer Recipe Calculator API: weighed buffer recipes with temperature-corrected pH, ionic strength, and stock dilution from scripts or notebooks.

# What It Does

Preparing Tris, phosphate, HEPES, and other biological buffers at a target pH requires the correct acid/base ratio, masses for the final volume, and—when prep and use temperatures differ—a realistic estimate of pH at the bench.

Manual Henderson-Hasselbalch calculations and spreadsheets often use pKa at 25 °C only, omit ionic strength, and do not warn when a buffer made at room temperature will read a different pH on ice. Diluting a concentrated stock without re-checking pH is another common source of error.

This package calls the same Pepkio Tools calculation engine as the hosted web application. Use `PepkioClient.run()` from Python, Jupyter, or automation pipelines to obtain grams of acid and base forms, temperature-corrected pKa, predicted working pH, ionic strength, gravimetric and titration routes, stock dilution volumes, protocol steps, and shareable run links.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- Buffer systems: Tris, sodium phosphate, HEPES, and other common laboratory buffers (`buffer_id`)
- Modes: `calculator` (weigh from dry reagents) and `stock` (dilute concentrated stock)
- Separate preparation and working temperatures with van't Hoff pKa correction and predicted pH at use temperature
- Weighed recipes: acid and base masses (g) plus gravimetric and titration preparation routes
- Ionic strength estimate (mM) with optional `target_ionic_strength_mM` or `added_salt_mM` for NaCl adjustment
- Stock dilution: `stock_volume_mL`, `diluent_volume_mL`, and pH re-check guidance
- Compatibility warnings for common assay conflicts
- Manifest and named examples: `get_manifest`, `list_examples`, `get_example_input`
- CLI: `pepkio-ph-buffer-recipe-calculator manifest` and `run`
- Configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-ph-buffer-recipe-calculator
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_ph_buffer_recipe_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("tris_50mM_1L")
    result = client.run(inp)
    inner = result.result["result"]
    print(inner["acid_mass_g"], inner["acid_form_label"])
    print(inner["base_mass_g"], inner["base_form_label"])
    print(result.result["metadata"]["predicted_working_ph"])
```

CLI:

```bash
pepkio-ph-buffer-recipe-calculator run --example tris_50mM_1L
```

Manifest inspection does not require an API key.

# Typical Use Cases

- 50 mM Tris-HCl pH 7.5 in 1 L with preparation at 25 °C and use at 4 °C
- 100 mM sodium phosphate pH 7.4 for biochemistry or enzyme assays
- Diluting 1 M Tris stock to 50 mM working concentration
- Matching ionic strength across buffers with optional NaCl
- Gravimetric vs titration buffer preparation planning
- Copy-ready protocol steps for lab notebooks or Methods sections

# Scientific Background

For a weak acid buffer, **pH = pKa + log([base]/[acid])**. Given a target pH and temperature-corrected pKa, the calculator determines the acid/base ratio and masses for the requested concentration and volume.

Tris and some other buffers have a large pH shift with temperature. A solution adjusted to pH 7.5 at 25 °C can read substantially higher when cooled to 4 °C. Verify pH with a calibrated meter at the temperature of use when precision matters.

Ionic strength affects effective pKa and enzyme behavior. Stock dilution reduces concentration by C_working = C_stock × (V_stock / V_final); pH should be re-measured after dilution rather than assumed unchanged.

# Web Application

For researchers who prefer a graphical interface, an interactive [pH Buffer Recipe Calculator](https://www.pepkio.com/tools/ph-buffer-recipe-calculator) is available in the browser.

The web interface provides live-updating results, optional ionic strength adjustment, stock dilution mode, compatibility notes, copy-ready protocol text, a Methods-style sentence, and shareable links that restore the same recipe as API `permalink` values.

# Documentation and Resources

Full documentation, examples, and issue tracking: [github.com/pepkio/pepkio-ph-buffer-recipe-calculator](https://github.com/pepkio/pepkio-ph-buffer-recipe-calculator)

Web tool: [pepkio.com/tools/ph-buffer-recipe-calculator](https://www.pepkio.com/tools/ph-buffer-recipe-calculator)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

pH buffer calculator, buffer recipe calculator, Tris buffer calculator, Tris-HCl preparation, phosphate buffer pH 7.4, HEPES buffer recipe, Henderson-Hasselbalch calculator, buffer pKa temperature correction, ionic strength buffer, NaCl buffer adjustment, gravimetric buffer preparation, buffer titration, stock buffer dilution, dilute Tris stock, Good's buffer, biological buffer preparation, molecular biology buffer, biochemistry buffer, protein buffer pH, enzyme assay buffer, cold room buffer pH, sodium phosphate buffer, buffer protocol generator, pepkio-ph-buffer-recipe-calculator, Python buffer API, shareable buffer recipe, laboratory buffer calculator, Pepkio, how to calculate Tris buffer grams for pH 7.5, prepare 50 mM Tris buffer recipe, phosphate buffer 100 mM pH 7.4 preparation, dilute 1 M Tris to 50 mM volume, Tris pH change with temperature explained, match ionic strength between buffers, gravimetric vs titration buffer prep, re-check pH after diluting buffer stock, Python script buffer recipe API, temperature corrected pKa Tris, weigh Tris hydrochloride and Tris base amounts, buffer recipe for protein purification, HEPES buffer cell culture preparation, stock buffer dilution calculator laboratory
