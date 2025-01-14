# Code for "Unveiling Global Patterns of Cultural Influence in the Digital Age"

This repository contains the code for the study **"Unveiling Global Patterns of Cultural Influence in the Digital Age."** The study investigates global patterns of cultural diffusion and influence using data from Wikidata and Wikipedia.

## Data Collection

- **Wikidata Information:** Collected using the [Wikidata REST API](https://www.wikidata.org/wiki/Wikidata:REST_API).  
- **Wikipedia Edit Data:** Retrieved using the [MediaWiki API](https://www.mediawiki.org/wiki/API:Edit).

## Code Overview

The repository includes the following scripts, corresponding to the study's research questions (RQ):

1. **`0_datacrawling.py`:** Preparation code for data collection.  
2. **`1_calculate_jaccard.py`:** Calculates the Jaccard Index for RQ1, which focuses on cultural content overlap.  
3. **`2_negativebinomial.py`:** Constructs a Negative Binomial Regression model for RQ2, analyzing factors influencing cultural diffusion.  
4. **`3_pointprocess.py`:** Builds a point process model (Hawkes Process) for RQ3 to capture the dynamics of cultural diffusion.

## Notes

- Running these scripts alone is not sufficient for full reproducibility of the results but provides key resources and information to support further exploration.
- Additional documentation and updates will be provided over time to enhance reproducibility and usability.

Feel free to contribute or raise issues if you have questions about the repository.
