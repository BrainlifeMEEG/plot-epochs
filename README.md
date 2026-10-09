# Plot Average ERPs by Condition

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.894-blue.svg)](https://doi.org/10.25663/brainlife.app.894)

## Description

This Brainlife.io app reads epoched MEG/EEG data and computes the average ERP (Event-Related Potential/Field) for each condition/event type present in the epochs, using MNE-Python's `Epochs.average()` and `Evoked.plot_joint()`.

The app generates:
- One PNG plot per condition (joint ERP/butterfly + topography plot)
- An HTML report containing the evoked responses for all conditions
- A `product.json` with dataset statistics and the first few condition plots embedded for quick viewing

## Inputs

- **`epo`** (`neuro/meeg/mne/epochs`): epoched MEG/EEG data to average and plot by condition (required)

## Outputs

- **`out_figs/erp_<condition>.png`**: individual ERP plot for each condition found in the epochs
- **`out_report/report.html`** (`report/html`): HTML report with the evoked response for every condition
- **`product.json`**: dataset statistics (epoch count, conditions, channel count, sampling rate) and up to the first 6 condition plots, base64-embedded

## Configuration Parameters

This app reads no configuration parameters beyond its input file (see Inputs above).

## Usage

### Running on Brainlife.io

1. Select your epoched MEG/EEG dataset (e.g. produced by the `epoch` app) as the `epo` input.
2. Submit the process.
3. Review the generated ERP plots and HTML report, or the embedded plots in `product.json`, once the process completes.

### Local Testing

```bash
# Edit config.json to point "epo" at real epoched data, then:
python main.py
```

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

- Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
- Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project it is helpful to acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
