# Final Report: Brent Oil Price Change Point Analysis
## Bayesian Change Point Detection and Event Correlation Analysis

**Date**: July 15, 2026  
**Challenge**: 10 Academy - KAIM 9 - Week 10  
**Focus**: Change Point Analysis and Statistical Modeling of Time Series Data

---

## Executive Summary

This report presents a comprehensive analysis of Brent oil price dynamics using Bayesian change point detection to identify structural breaks in the market and correlate them with major geopolitical and economic events. The analysis reveals a significant structural shift in February 2005, characterized by a 252.9% increase in mean price levels, driven by broader market dynamics rather than any single event in our database.

### Key Findings

- **Major Change Point**: February 24, 2005 (95% HDI: February 16 - March 7, 2005)
- **Price Impact**: Mean price increased from $21.43 to $75.60 (252.9% increase)
- **Model Performance**: Excellent convergence (R-hat = 1.00)
- **Event Correlation**: No direct correlation with single events; suggests broader market dynamics
- **Data Coverage**: 9,011 daily observations from May 20, 1987 to November 14, 2022

---

## 1. Introduction and Business Context

### 1.1 Business Need

As data scientists at Birhan Energies, we analyzed Brent oil price dynamics to help stakeholders navigate the complexities of the global energy market. The oil market's inherent volatility makes it challenging for investors, policymakers, and energy companies to make informed decisions regarding risk management, investment strategies, and operational planning.

### 1.2 Research Objectives

1. Identify key events that have significantly impacted Brent oil prices over the past decade
2. Quantify how much these events affect price changes using statistical methods
3. Provide clear, data-driven insights to guide investment strategies, policy development, and operational planning

### 1.3 Methodological Approach

We employed Bayesian change point detection using PyMC to identify structural breaks in the price series, providing full posterior distributions for all parameters and quantifying uncertainty in our estimates. This approach offers several advantages over traditional methods:

- **Probabilistic Framework**: Natural incorporation of prior knowledge and uncertainty quantification
- **Flexibility**: Can model various types of structural breaks (mean, variance, both)
- **Interpretability**: Results are intuitive and can be explained to stakeholders

---

## 2. Data Analysis and Exploratory Findings

### 2.1 Dataset Overview

**Brent Oil Price Data**
- **Period**: May 20, 1987 to November 14, 2022
- **Frequency**: Daily observations
- **Total Observations**: 9,011 data points
- **Price Range**: $9.10 to $143.95 per barrel
- **Mean Price**: $48.42
- **Standard Deviation**: $32.86

**Key Events Database**
- **Total Events**: 15 major geopolitical and economic events (1990-2022)
- **Event Categories**:
  - Geopolitical Conflicts (6 events)
  - OPEC Decisions (3 events)
  - Economic Shocks (2 events)
  - Economic Sanctions (4 events)

### 2.2 Exploratory Data Analysis Results

#### Price Statistics
- **Mean**: $48.42
- **Median**: $38.57
- **Standard Deviation**: $32.86
- **Minimum**: $9.10
- **Maximum**: $143.95
- **Total Change**: $74.96 (402.4% increase over the period)

#### Stationarity Analysis
- **Raw Price Series**: Non-stationary (ADF p-value: 0.2893, KPSS p-value: 0.0100)
- **Log Returns**: Stationary (ADF p-value: 0.0000, KPSS p-value: 0.1000)

This confirms that log returns transformation achieves stationarity, making them suitable for change point analysis.

#### Volatility Analysis
- **Mean Daily Volatility**: 0.0255
- **Maximum Daily Gain**: 0.4120
- **Maximum Daily Loss**: -0.6437
- **30-Day Rolling Volatility**: Mean of 0.0216, ranging from 0.0058 to 0.1873

The volatility analysis reveals significant clustering of high volatility periods, particularly during major market disruptions.

### 2.3 Key Observations from EDA

1. **Non-stationarity**: Raw prices exhibit clear trending behavior, requiring transformation for statistical analysis
2. **Volatility Clustering**: Periods of high volatility cluster around major market events
3. **Fat-tailed Distribution**: Log returns show significant kurtosis (65.9), indicating extreme price movements are more common than in normal distributions
4. **Long-term Trend**: Overall upward trend with periodic significant corrections

---

## 3. Bayesian Change Point Analysis

### 3.1 Model Specification

We implemented a single change point model focusing on mean shifts:

**Model Structure**:
```
tau ~ DiscreteUniform(lower=0.25n, upper=0.75n)
mu_before ~ Normal(mu=50, sigma=20)
mu_after ~ Normal(mu=50, sigma=20)
sigma ~ HalfNormal(sigma=10)
mu = switch(time_indices < tau, mu_before, mu_after)
price ~ Normal(mu=mu, sigma=sigma)
```

**Model Justification**:
- Restricted change point to middle 50% of data to avoid edge effects
- Used weakly informative priors to let data drive the inference
- Single change point model as starting point for analysis

### 3.2 Model Diagnostics

**Convergence Assessment**:
- **R-hat Values**: [1.00, 1.00, 1.00, 1.00] - All parameters show excellent convergence
- **Sampling Efficiency**: 2,000 draws with 1,000 tuning iterations per chain
- **Computational Performance**: Sampling completed in ~10 seconds

**Parameter Estimates**:
| Parameter | Mean | Standard Deviation |
|-----------|------|-------------------|
| tau (change point index) | 4,521 | 3.2 |
| mu_before (mean before) | $21.43 | $0.28 |
| mu_after (mean after) | $75.60 | $0.28 |
| sigma (standard deviation) | $18.59 | $0.14 |

### 3.3 Change Point Results

**Primary Finding**:
- **Change Point Date**: February 24, 2005
- **95% Highest Density Interval**: February 16 to March 7, 2005
- **Change Point Index**: 4,521 (approximately 50% through the dataset)

**Quantified Impact**:
- **Mean Price Before**: $21.43
- **Mean Price After**: $75.60
- **Absolute Change**: $54.17
- **Percentage Change**: 252.9%

This represents a fundamental structural shift in oil market dynamics, with the mean price level more than tripling after the change point.

### 3.4 Interpretation of Results

The detected change point corresponds to a period of significant transformation in global oil markets:

**Market Context (2004-2006)**:
- Rapid economic growth in China and other emerging markets
- Increased global demand for energy
- Speculative investment in commodity markets
- Geopolitical tensions in major oil-producing regions
- Beginning of the commodities supercycle

The analysis suggests that this structural change was driven by broader market dynamics rather than any single event, highlighting the complexity of factors influencing oil prices.

---

## 4. Event Correlation Analysis

### 4.1 Temporal Proximity Analysis

We examined the temporal relationship between the detected change point (February 24, 2005) and the 15 major events in our database:

**Events within 1 year of change point**: None
**Events within 30 days of change point**: None

### 4.2 Key Events Analysis

**Notable Events and Their Proximity to Change Point**:

1. **Iraq War (March 20, 2003)**: 2 years before change point
2. **OPEC Production Increase (July 3, 2008)**: 3 years after change point
3. **Global Financial Crisis (September 15, 2008)**: 3.5 years after change point

The absence of events immediately surrounding the change point suggests that the structural shift was not triggered by a single geopolitical or economic event but rather by broader market dynamics.

### 4.3 Causal Inference Limitations

**Critical Distinction**: Our analysis identifies statistical correlations but cannot definitively prove causal relationships.

**Key Limitations**:
- **Temporal Proximity ≠ Causation**: Just because a price change follows an event doesn't prove the event caused the change
- **Confounding Variables**: Multiple factors often influence oil prices simultaneously
- **Reverse Causality**: Price movements may precipitate political or economic responses
- **Omitted Variable Bias**: Unmeasured factors (inventory levels, production capacity, demand shifts) may be true drivers

**Interpretation Framework**: We frame findings as "associations" and "correlations" rather than definitive causal claims, using language like "consistent with" rather than "caused by."

---

## 5. Dashboard Development

### 5.1 Technical Architecture

**Backend (Flask)**:
- RESTful API endpoints for data serving
- Endpoints for prices, events, change point results, and EDA findings
- CORS-enabled for cross-origin requests
- Health check endpoint for monitoring

**Frontend (React)**:
- Responsive dashboard interface
- Real-time data fetching from Flask API
- Interactive components for data visualization
- Mobile-responsive design

### 5.2 Dashboard Features

**Key Capabilities**:
1. **Price Summary Display**: Real-time summary statistics
2. **Change Point Results**: Bayesian analysis results with uncertainty quantification
3. **Events Database**: Interactive table of 15 major events
4. **Analysis Notes**: Interpretation of findings and methodology
5. **Responsive Design**: Works on desktop, tablet, and mobile devices

### 5.3 Implementation Details

**API Endpoints**:
- `/api/health` - Health check
- `/api/prices` - Historical price data with optional date filtering
- `/api/prices/summary` - Price summary statistics
- `/api/events` - Events database
- `/api/change-point` - Change point analysis results
- `/api/analysis/eda` - EDA results
- `/api/plots` - List available visualizations

**Frontend Components**:
- Summary cards for key metrics
- Interactive events table
- Analysis notes section
- Responsive layout with gradient design

---

## 6. Methodological Considerations and Limitations

### 6.1 Model Limitations

**Single Change Point Assumption**:
- The model assumes a single structural break, which may oversimplify complex market dynamics
- Real markets may experience multiple simultaneous or sequential structural breaks
- Future work should explore multiple change point models

**Parameter Stationarity**:
- Assumes constant parameters between change points
- May not capture gradual transitions or evolving dynamics
- Volatility clustering not explicitly modeled

**Prior Specification**:
- Used weakly informative priors, but results could be sensitive to prior choices
- Sensitivity analysis recommended for robust conclusions

### 6.2 Data Limitations

**Event Database Scope**:
- Limited to 15 major events, subjective selection criteria
- Event timing precision may vary
- Event magnitude not quantified beyond binary classification
- Geographic focus may miss regional influences

**Data Granularity**:
- Daily data may miss intraday volatility and precise timing
- Weekend and holiday effects not explicitly modeled
- Exchange rate effects not isolated from fundamental oil market dynamics

### 6.3 Generalizability Limitations

**Historical Specificity**:
- Patterns identified may not generalize to future market conditions
- Structural market changes (shale revolution, energy transition) limit historical comparability
- Market dynamics may have different characteristics across time periods

### 6.4 Mitigation Strategies

**Methodological**:
- Test multiple model specifications to assess robustness
- Use temporal cross-validation for predictive performance assessment
- Conduct sensitivity analysis on prior choices and assumptions
- Report uncertainty quantification for all parameter estimates

**Interpretation**:
- Use conservative language when describing event-price relationships
- Consider economic theory alongside statistical findings
- Present findings in broader market context
- Acknowledge alternative explanations for observed patterns

---

## 7. Conclusions and Recommendations

### 7.1 Key Conclusions

1. **Structural Break Identified**: The analysis identified a significant structural break in Brent oil prices on February 24, 2005, characterized by a 252.9% increase in mean price levels.

2. **Broad Market Dynamics**: The change point does not correlate with any single event in our database, suggesting it was driven by broader market dynamics including increased global demand (particularly from China), commodity market speculation, and long-term supply-demand shifts.

3. **Model Performance**: The Bayesian change point model achieved excellent convergence and reliable results, demonstrating the effectiveness of probabilistic approaches for time series analysis.

4. **Complex Market Dynamics**: The absence of direct event correlation highlights the complexity of oil market dynamics and the limitations of event-driven analysis for understanding structural changes.

### 7.2 Recommendations for Stakeholders

**For Investors**:
- Recognize that structural market changes can occur without obvious triggering events
- Incorporate long-term demand-supply dynamics into investment strategies
- Use probabilistic approaches to quantify uncertainty in market forecasts
- Diversify across energy sources to mitigate structural risk

**For Policymakers**:
- Focus on long-term structural factors rather than short-term event responses
- Develop strategies that account for fundamental market transformations
- Monitor leading indicators of structural change (demand growth, capacity constraints)
- Build strategic reserves to buffer against structural supply disruptions

**For Energy Companies**:
- Incorporate structural change detection into strategic planning
- Develop flexible operational strategies that can adapt to market regime changes
- Invest in scenario analysis for different structural market conditions
- Maintain financial flexibility to navigate structural transitions

### 7.3 Future Research Directions

**Model Extensions**:
- Implement multiple change point models to identify complex patterns
- Incorporate variance change detection alongside mean changes
- Develop regime-switching models with explicit transition dynamics
- Integrate macroeconomic variables (GDP, inflation, exchange rates)

**Data Enhancements**:
- Expand events database to include more events and quantitative measures
- Incorporate higher-frequency data for intraday analysis
- Include additional oil benchmarks (WTI, Dubai) for comparative analysis
- Integrate alternative data sources (shipping data, inventory levels)

**Methodological Improvements**:
- Explore online change point detection for real-time monitoring
- Develop causal inference methods to address correlation vs. causation limitations
- Implement machine learning approaches for pattern recognition
- Develop ensemble methods combining multiple change point algorithms

---

## 8. Appendix

### 8.1 Technical Implementation

**Software Stack**:
- Python 3.9+
- PyMC 6.1.0 (Bayesian modeling)
- ArviZ 1.2.0 (model diagnostics)
- Pandas/NumPy (data manipulation)
- Matplotlib/Seaborn (visualization)
- Flask (backend API)
- React (frontend dashboard)

**Computational Resources**:
- Sampling completed in ~10 seconds on standard hardware
- Model converged with 2 chains, 2,000 draws each
- Total computational time: <1 hour for complete analysis

### 8.2 Reproducibility

**Code Availability**:
- All analysis code available in GitHub repository
- Jupyter notebooks for EDA and change point analysis
- Flask backend and React frontend for dashboard
- Complete requirements.txt for dependency management

**Data Access**:
- Brent oil price data from standard financial data sources
- Events database compiled from historical records
- All data processing steps documented in code

### 8.3 Assumptions Documentation

**Key Assumptions**:
1. Historical price data is accurate and representative
2. Event dates are reasonably accurate
3. Log returns achieve sufficient stationarity for analysis
4. Observations are reasonably independent conditional on change points
5. Normal distributions are appropriate for likelihood functions

**Critical Limitations**:
- Cannot prove causal relationships from correlations
- Daily data granularity may miss important dynamics
- Single change point model may oversimplify complex patterns
- Event database limited to 15 major events

---

## 9. References

### 9.1 Methodological References

1. **Change Point Analysis**:
   - Forecastegy: Change Point Detection in Time Series Python
   - Kais et al.: "A Survey on Change Point Detection Methods" (2016)
   - Fraunhofer: Change Point Detection Blog

2. **Bayesian Methods**:
   - PyMC Documentation: Bayesian Changepoint Detection
   - McElreath: "Statistical Rethinking" (2020)
   - Gelman et al.: "Bayesian Data Analysis" (2013)

3. **Time Series Analysis**:
   - Hamilton: "Time Series Analysis" (1994)
   - Chatfield: "The Analysis of Time Series" (2016)
   - Hyndman: "Forecasting: Principles and Practice" (2018)

### 9.2 Domain References

1. **Oil Market Dynamics**:
   - OPEC Annual Statistical Bulletin
   - IEA World Energy Outlook
   - EIA Short-Term Energy Outlook

2. **Event Database Sources**:
   - Federal Reserve Economic Data (FRED)
   - World Bank Global Economic Monitor
   - IMF World Economic Outlook

---

## 10. Conclusion

This comprehensive analysis of Brent oil prices using Bayesian change point detection has identified a significant structural break in February 2005, characterized by a 252.9% increase in mean price levels. The absence of direct correlation with major events in our database suggests that this structural change was driven by broader market dynamics rather than any single geopolitical or economic event.

The analysis demonstrates the value of probabilistic approaches for time series analysis, providing full posterior distributions for all parameters and quantifying uncertainty in estimates. The methodology, while subject to important limitations regarding causal inference and model assumptions, offers valuable insights for investors, policymakers, and energy companies seeking to understand and navigate the complex dynamics of global oil markets.

Future research should explore multiple change point models, incorporate additional explanatory variables, and develop more sophisticated causal inference methods to address the limitations identified in this analysis. The continued development of such analytical approaches will be essential for improving our understanding of energy market dynamics and supporting more informed decision-making across the energy sector.

---

**Analysis Completed**: July 15, 2026  
**Total Analysis Time**: ~4 hours  
**Code Repository**: https://github.com/rihanaa-m/week-10.git  
**Dashboard**: Flask backend + React frontend (deployed locally)