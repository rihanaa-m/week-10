# Brent Oil Price Change Point Analysis

## Overview
This project analyzes how major geopolitical and economic events affect Brent oil prices using Bayesian change point detection. The analysis focuses on identifying structural breaks in oil prices and associating them with historical events such as political decisions, conflicts, economic sanctions, and OPEC policy changes.

## Business Context
**Client**: Birhan Energies - A leading consultancy firm specializing in data-driven insights for the energy sector

**Objective**: Provide actionable intelligence to support decision-making for investors, policymakers, and energy companies by understanding how major events influence oil market dynamics.

## Challenge Details
- **Program**: 10 Academy - KAIM 9 - Week 10
- **Topic**: Change Point Analysis and Statistical Modeling of Time Series Data
- **Dates**: July 8-14, 2026
- **Interim Submission**: July 12, 2026, 8:00 PM UTC
- **Final Submission**: July 14, 2026, 8:00 PM UTC

## Project Structure
```
week 10/
├── .vscode/                  # VS Code configuration
├── .github/                  # GitHub workflows
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── ANALYSIS_WORKFLOW.md    # Detailed analysis workflow
├── ASSUMPTIONS_LIMITATIONS.md # Methodological assumptions
├── INTERIM_REPORT.md       # Interim submission report
├── src/                    # Source code
├── notebooks/              # Jupyter notebooks
│   ├── 01_eda.ipynb       # Explatory data analysis
│   └── README.md
├── tests/                  # Unit tests
├── scripts/                # Analysis scripts
├── data/                   # Data files
│   ├── key_events_oil_prices.csv
│   └── brent_oil_prices_sample.csv
└── plots/                  # Generated visualizations
```

## Key Deliverables

### Task 1: Laying the Foundation (Completed)
- ✅ Analysis workflow documentation
- ✅ Structured events database (15 major events, 1990-2022)
- ✅ Assumptions and limitations documentation
- ✅ Initial EDA framework
- ✅ Interim report

### Task 2: Change Point Modeling (In Progress)
- Bayesian change point detection using PyMC
- Model diagnostics and convergence assessment
- Event correlation analysis
- Impact quantification

### Task 3: Interactive Dashboard (Pending)
- Flask backend for data serving
- React frontend for visualization
- Interactive exploration tools

## Dataset

### Brent Oil Prices
- **Period**: May 20, 1987 - September 30, 2022
- **Frequency**: Daily
- **Variables**: Date, Price (USD per barrel)

### Key Events Database
15 major events categorized by type:
- **Geopolitical Conflicts**: Wars, civil conflicts, regional instabilities
- **OPEC Decisions**: Production changes and policy shifts
- **Economic Shocks**: Financial crises, pandemics
- **Economic Sanctions**: Trade restrictions and policy changes

## Methodology

### Statistical Approach
- **Bayesian Change Point Detection**: Using PyMC for probabilistic modeling
- **MCMC Sampling**: Markov Chain Monte Carlo for posterior estimation
- **Time Series Analysis**: Stationarity testing, volatility analysis, trend decomposition
- **Event Correlation**: Temporal proximity analysis between change points and events

### Key Concepts
- **Change Point Models**: Identify structural breaks in time series
- **Bayesian Inference**: Incorporate prior knowledge and quantify uncertainty
- **Log Returns**: Achieve stationarity for reliable statistical analysis
- **Volatility Clustering**: Examine patterns in variance over time

## Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Setup
```bash
# Clone repository
git clone <repository-url>
cd week-10

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running Exploratory Data Analysis
```bash
jupyter notebook notebooks/01_eda.ipynb
```

### Running Tests
```bash
pytest tests/
```

### Key Files
- `ANALYSIS_WORKFLOW.md`: Detailed step-by-step analysis plan
- `ASSUMPTIONS_LIMITATIONS.md`: Methodological considerations and limitations
- `INTERIM_REPORT.md`: Task 1 findings and deliverables
- `data/key_events_oil_prices.csv`: Compiled events database

## Dependencies

### Core Packages
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `matplotlib`, `seaborn`: Visualization
- `pymc`: Bayesian modeling
- `arviz`: Model diagnostics
- `scipy`, `statsmodels`: Statistical analysis

### Development
- `jupyter`, `notebook`: Interactive analysis
- `pytest`: Testing
- `flask`, `flask-cors`: Web framework (Task 3)

## Team

**Tutors**:
- Kerod
- Feven
- Mahbubah

**Communication**: Slack channel #all-week10  
**Office Hours**: Mon–Fri, 08:00–15:00 UTC

## Important Notes

### Correlation vs. Causation
This analysis identifies statistical correlations between events and price changes but cannot definitively prove causal relationships. All findings should be interpreted with this distinction in mind.

### Limitations
- Daily data granularity may miss intraday dynamics
- Event timing precision may vary
- Multiple confounding factors influence oil prices simultaneously
- Historical patterns may not generalize to future conditions

### Ethical Considerations
- Findings are for analytical purposes only
- Not suitable for specific investment recommendations
- Uncertainty and limitations should be clearly communicated
- Analysis should be reproducible and transparent

## License
This project is part of the 10 Academy KAIM 9 Week 10 challenge.

## Acknowledgments
- 10 Academy for the challenge framework
- Birhan Energies for the business context
- Tutors and support staff for guidance and feedback