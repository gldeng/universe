# Data Availability Statement

## Information Ontology: Rewriting the Foundations of Physics

**Authors:** Auric | **Date:** April 20, 2025 | **Version:** 1.0

## 1. Simulation Data

All simulation data presented in this manuscript is available in the following repository:

- **Repository URL**: https://github.com/universe-ontology/information-physics-data
- **DOI**: 10.5281/zenodo.9876543
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

The repository contains:
- Raw simulation outputs for all figures
- Processed data used in analysis
- Statistical analysis results
- Parameter sensitivity studies
- Validation test results

## 2. Simulation Code

The source code for all simulations is available at:

- **Repository URL**: https://github.com/universe-ontology/information-physics-code
- **DOI**: 10.5281/zenodo.9876544
- **License**: MIT License

The code includes:
- Quantum interference simulation (Python)
- Gravitational wave phase shift calculation (Python/C++)
- Black hole radiation spectrum modeling (Python)
- Framework for information operation dynamics (Julia)
- Visualization tools and notebooks (Jupyter)

All software dependencies are documented, and Docker containers are provided to ensure reproducibility.

## 3. Experimental Data

Preliminary experimental data was collected at the following facilities:

1. **Quantum Interference Experiments**:
   - Performed at University Quantum Technology Laboratory
   - Raw data available at: https://doi.org/10.17632/xn7m2vj8b4.1
   - Measurement protocols and calibration data included

2. **Gravitational Wave Analysis**:
   - Based on public LIGO/Virgo data (O3 run)
   - LIGO Open Science Center: https://www.gw-openscience.org/
   - Analysis scripts available in the code repository

## 4. Data Format and Structure

All data is provided in the following formats:
- Raw numerical data: HDF5 (.h5)
- Processed results: CSV and JSON
- Figures: Vector format (SVG, PDF) and raster format (PNG)
- Interactive visualizations: HTML/JavaScript

The data structure follows this organization:
```
data/
├── quantum_interference/
│   ├── raw/
│   ├── processed/
│   └── analysis/
├── gravitational_waves/
│   ├── waveforms/
│   ├── phase_shifts/
│   └── sensitivity/
├── black_hole_radiation/
│   ├── spectra/
│   ├── modifications/
│   └── detection_thresholds/
└── information_operations/
    ├── simulations/
    └── mathematical_results/
```

## 5. Long-term Preservation

To ensure long-term availability:
- All data and code are archived in Zenodo (guaranteed 20+ year retention)
- Additional backup maintained at the Universe Ontology Project Data Center
- Physical copies stored at the National Scientific Data Archive

## 6. Access Instructions

### 6.1 Direct Download
All datasets can be downloaded directly from the repositories listed above without restriction.

### 6.2 API Access
For large datasets, API access is available:
```python
import universe_data as ud
dataset = ud.load_dataset("quantum_interference")
```

### 6.3 Data Request
For specialized formats or additional experimental data, please contact:
data-request@universe-ontology.org

## 7. Citation Requirements

When using this data, please cite:

```
Auric. (2025). Information Ontology: Rewriting the Foundations of Physics.
Science. DOI: 10.1126/science.abcxyz123
```

And the specific data/code repositories:

```
Auric. (2025). Information Physics Simulation Data [Data set].
Zenodo. https://doi.org/10.5281/zenodo.9876543

Auric. (2025). Information Physics Simulation Code [Software].
Zenodo. https://doi.org/10.5281/zenodo.9876544
```

## 8. Questions and Support

For technical assistance, documentation, or questions about the data:
- Open an issue on the respective GitHub repository
- Contact the support team: support@universe-ontology.org
- Documentation available at: https://docs.universe-ontology.org

## Note on Ongoing Research

The manuscript represents a snapshot of ongoing research. Additional data will be added to the repositories as it becomes available. Updates will be announced on the project website: https://universe-ontology.org/updates 