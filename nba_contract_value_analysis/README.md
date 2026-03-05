# NBA Contract Value Analysis

## 

### Project Overview

This project evaluates NBA player contract efficiency by analyzing on-court production relative to salary impact across multiple seasons (2022–2026).



The goal is to identify:

* Which players provide the highest return on investment (ROI)
* Which contracts are underpaid or overpaid relative to performance
* How contract value changes across different salary cap environments



The analysis was built entirely in PostgreSQL using layered CTE pipelines and window functions.

### 

### Tools

* PostgreSQL
* SQL (CTEs, joins, window functions)
* Python (data collection/cleaning)

### 

### Data

* Player statistics (NBAstuffer)
* Player salaries (ESPN)
* Seasons: 2022–2026



### Methodology



##### Impact Metric

Impact per Minute (IPM) = (Points + Rebounds + Assists) / Minutes Played

Players with low minutes (<15 MPG) or limited games (<20 GP) were excluded to reduce statistical noise.

##### 

##### ROI Model

Contracts were standardized using salary cap percentage:

Cap Hit % = Salary / League Salary Cap



Return on Investment:

Value Index = IPM / Salary Cap %



##### Percentile Model

Ranked players by:

* Performance percentile
* Salary percentile



Classified contracts as:

* Underpaid
* Overpaid
* Fair Value



### Notable Insights



• Rookie-scale and veteran minimum contracts frequently dominate top ROI tiers, as lower salary cap hits amplify production efficiency.



Example: Players on rookie contracts in the 2024–2025 season ranked disproportionately in the top 10 ROI scores despite moderate box-score production. Many of these players came from the eventual champions (OKC Thunder) and their opponent in the finals (IND Pacers). 



• High-salary veteran contracts often show lower value indices relative to cap impact, indicating diminishing marginal returns at the top of the salary distribution.



Example: In the 2022–2023 season, Joe Harris carried a large cap hit but produced a relatively low impact-per-minute score, placing him in the bottom value percentile.

