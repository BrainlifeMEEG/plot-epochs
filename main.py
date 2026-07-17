"""
Plot average ERP/Fs from epochs by condition for Brainlife.io

This app reads epochs from MNE-Python format and generates average ERP/F plots
for each condition/event type present in the data. Creates visualizations
and an HTML report with all plots.

Inputs:
    - meg-epo.fif: Epoched MEG/EEG data in MNE format

Outputs:
    - out_figs/erp_*.png: Individual ERP plots for each condition
    - out_report/report.html: HTML report with all ERP visualizations
    - product.json: Brainlife.io product metadata including all figures
"""

# Copyright (c) 2026 brainlife.io
#
# This app plots average ERPs from epochs by condition.
#
# Authors:
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
import os.path as op
import matplotlib.pyplot as plt
import numpy as np

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    save_figure_with_base64
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()

# == LOAD EPOCHS ==
# Read epochs file
epochs_file = config['epo']
epochs = mne.read_epochs(epochs_file, preload=True, verbose=False)

print(f"Loading epochs from: {epochs_file}")
print(f"Total epochs: {len(epochs)}")
print(f"Event names: {epochs.event_id}")

# == COMPUTE AVERAGE ERPs BY CONDITION ==
# Get unique event types/conditions
event_id = epochs.event_id
conditions = {name: id_val for name, id_val in event_id.items()}

# Create report for storing all plots
report = mne.Report(title='Average ERPs by Condition')

# Track product items
product_items = []

# Plot evoked response for each condition
evokeds = []
titles = []
skipped_conds = 0
for idx, (condition_name, condition_id) in enumerate(sorted(conditions.items(), key=lambda x: x[1])):
    print(f"Processing condition: {condition_name}")
    
    # Extract epochs for this condition
    condition_epochs = epochs[condition_name]
    
    if len(condition_epochs) == 0:
        print(f"  Warning: No epochs for condition {condition_name}")
        continue
    
    # Compute average
    evoked = condition_epochs.average()
    evoked.comment = condition_name
    evokeds.append(evoked)
    titles.append(condition_name)
    
    # Create figure for this condition
    fig = evoked.plot_joint(show=False)
    fig.suptitle(f'Average ERP - {condition_name}', fontsize=14, fontweight='bold')
    
    # Save figure
    fig_name = f"erp_{condition_name.replace('/', '_').replace(' ', '_')}.png"
    fig_path = op.join('out_figs', fig_name)
    fig_base64 = save_figure_with_base64(fig, fig_path, dpi_file=150, dpi_base64=80)
    
    if idx < 6:  # Add first 6 conditions to report for visualization
        # add to product
        add_image_to_product(product_items, fig_name, base64_data=fig_base64)
    else:
        skipped_conds += 1
        print(f"  Note: Condition {condition_name} has been saved but not added here due to file size limits. Check out_figs/ for all condition plots.")
    
    print(f"  Saved: {fig_name} ({len(condition_epochs)} epochs averaged)")

# == ADD INFO AND SUMMARY ==
# Add dataset info
add_info_to_product(product_items, f"Processed {len(epochs)} epochs")
add_info_to_product(product_items, f"Conditions: {', '.join(titles)}")
add_info_to_product(product_items, f"Channels: {len(epochs.ch_names)}")
add_info_to_product(product_items, f"Sampling rate: {epochs.info['sfreq']} Hz")
add_info_to_product(product_items, f"{skipped_conds} conditions skipped in pictures below due to file size limits (see out_figs/).", msg_type='warning')

# == GENERATE HTML REPORT ==
if evokeds:
    report.add_evokeds(evokeds=evokeds, titles=titles)
    report.save('out_report/report.html', overwrite=True, verbose=False)
    print("HTML report saved to out_report/report.html")

# == CREATE PRODUCT.JSON ==
create_product_json(product_items)
print("Product JSON created successfully")
print("App completed successfully!")
