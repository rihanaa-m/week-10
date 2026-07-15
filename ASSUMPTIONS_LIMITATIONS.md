# Assumptions and Limitations for Brent Oil Price Change Point Analysis

## Core Assumptions

### Data Quality and Completeness
1. **Historical Data Accuracy**: We assume that the historical Brent oil price data from May 20, 1987, to September 30, 2022, is accurate and representative of actual market prices during that period.
2. **Event Date Precision**: We assume that the dates assigned to major geopolitical and economic events are reasonably accurate, though exact timing of market impact may vary.
3. **No Survivorship Bias**: The dataset is assumed to be complete without systematic exclusion of relevant time periods or events.

### Market Behavior Assumptions
1. **Market Efficiency**: The analysis assumes that oil markets generally incorporate available information into prices, though with potential lags and inefficiencies.
2. **Causal Relationship**: We assume that major events can influence oil prices, though the magnitude and timing of such effects may vary.
3. **Representative Events**: The compiled list of 15 key events is assumed to be representative of the major drivers of oil price changes over the analysis period.

### Statistical Assumptions
1. **Stationarity**: After appropriate transformations (e.g., log returns), we assume that the data exhibits sufficient stationarity for change point analysis.
2. **Independence**: We assume that, conditional on the change points, observations are reasonably independent for modeling purposes.
3. **Distributional Choice**: The use of normal distributions for likelihood functions assumes that the transformed price data is approximately normally distributed.

### Model Assumptions
1. **Single Change Point Model**: Initial models assume single change points, which may oversimplify complex market dynamics with multiple simultaneous influences.
2. **Markov Chain Convergence**: We assume that MCMC sampling will converge to the true posterior distribution given appropriate run lengths and diagnostics.
3. **Prior Appropriateness**: The choice of prior distributions is assumed to be reasonable and not overly influential on posterior results.

## Key Limitations

### Methodological Limitations

#### Correlation vs. Causation
**Critical Distinction**: This analysis can identify statistical correlations between events and price changes, but cannot definitively prove causal relationships. 

**Specific Limitations**:
- **Temporal Proximity**: Just because a price change follows an event doesn't prove the event caused the change
- **Confounding Variables**: Multiple factors often influence oil prices simultaneously; isolating individual event impacts is challenging
- **Reverse Causality**: Sometimes price movements may precipitate political or economic responses rather than vice versa
- **Omitted Variable Bias**: Unmeasured factors (e.g., inventory levels, production capacity, demand shifts) may be the true drivers

**Approach**: We will frame findings as "associations" and "correlations" rather than definitive causal claims, using language like "consistent with" rather than "caused by."

#### Temporal Resolution Limitations
- **Daily Data Granularity**: Daily price data may miss intraday volatility and precise timing of market reactions
- **Event Impact Lags**: The analysis may not capture delayed market responses to events that occur over weeks or months
- **Multiple Event Confounding**: When events occur in close proximity, isolating individual impacts becomes difficult

#### Model Limitations
- **Simplified Change Point Structure**: Real markets may experience gradual transitions rather than abrupt change points
- **Parameter Stationarity**: The assumption of constant parameters between change points may not hold in volatile markets
- **Single vs. Multiple Change Points**: The analysis may miss complex patterns with multiple simultaneous structural breaks

### Data Limitations

#### Event Dataset Limitations
- **Subjective Event Selection**: The choice of 15 key events involves subjective judgment about what constitutes "major" events
- **Event Timing Precision**: Exact dates of market impact may differ from official announcement dates
- **Event Magnitude Quantification**: The analysis doesn't quantify the "size" or importance of events beyond binary classification
- **Geographic Scope**: Events are focused on major global incidents, potentially missing regional influences

#### Price Data Limitations
- **Brent Crude Specificity**: Analysis is limited to Brent crude prices; other benchmarks (WTI, Dubai) may show different patterns
- **Exchange Rate Effects**: Price movements may reflect USD exchange rate changes rather than fundamental oil market dynamics
- **Quality Changes**: Changes in oil quality specifications over time may affect price comparisons

### Analytical Limitations

#### Statistical Power
- **Multiple Testing**: Testing multiple change points increases the risk of false positives
- **Sample Size Constraints**: While the dataset spans 35 years, the number of major events is relatively small
- **Volatility Clustering**: Standard change point models may not adequately capture volatility clustering patterns

#### Generalizability
- **Historical Specificity**: Patterns identified may not generalize to future market conditions
- **Structural Market Changes**: Fundamental changes in oil markets (e.g., shale revolution, renewable energy transition) may limit historical comparability
- **Regime Changes**: Market dynamics may have fundamentally different characteristics in different time periods

## Mitigation Strategies

### Methodological Mitigations
1. **Multiple Model Specifications**: Test different change point model structures to assess robustness
2. **Cross-Validation**: Use temporal cross-validation to assess predictive performance
3. **Sensitivity Analysis**: Test sensitivity to prior choices and model assumptions
4. **Confidence Intervals**: Report uncertainty quantification for all parameter estimates

### Interpretation Mitigations
1. **Conservative Language**: Use cautious language when describing event-price relationships
2. **Multiple Lines of Evidence**: Consider economic theory and domain knowledge alongside statistical findings
3. **Contextual Factors**: Always present findings in the context of broader market conditions
4. **Alternative Explanations**: Acknowledge and discuss alternative explanations for observed patterns

### Data Mitigations
1. **Multiple Data Sources**: Cross-reference findings with additional data sources when available
2. **Event Classification**: Use multiple event classification schemes to test robustness
3. **Time Window Analysis**: Examine impacts over different time windows to assess persistence

## Ethical and Professional Considerations

### Responsible Communication
1. **Uncertainty Transparency**: Clearly communicate uncertainty and limitations in all reporting
2. **Avoid Overstatement**: Resist the temptation to make stronger claims than the data supports
3. **Methodological Transparency**: Document all methodological choices and their justifications
4. **Reproducibility**: Ensure analysis is fully reproducible with complete code and data documentation

### Stakeholder Considerations
1. **Investment Implications**: Avoid making specific investment recommendations based solely on this analysis
2. **Policy Relevance**: Frame findings appropriately for policy audiences without oversimplification
3. **Professional Responsibility**: Acknowledge the limitations of the analysis when communicating results

## Conclusion

This analysis aims to provide valuable insights into the relationship between major events and Brent oil prices while maintaining scientific rigor and professional responsibility. By explicitly acknowledging assumptions and limitations, we aim to provide a transparent foundation for interpreting results and making informed decisions based on the findings.

The fundamental distinction between correlation and causation remains the most critical limitation, and all findings should be interpreted with this distinction in mind. The analysis is designed to identify patterns and generate hypotheses rather than provide definitive causal explanations.