\# Demand Forecasting for Retail



Forecasting daily sales 16 days ahead for 54 stores and 33 product

families, and translating forecast error into inventory cost.



!\[Dashboard](images/dashboard.png)



\## Key results



| Model | WAPE | RMSLE |

|-------|------|-------|

| Seasonal naive (baseline) | \[x.xx] | \[x.xx] |

| LightGBM | \[x.xx] | \[x.xx] |



With the same restocking rules, the model reduced the simulated

stockout + overstock cost by \[X]% compared with the baseline.



\## Approach



1\. \*\*EDA\*\*: weekly seasonality, promotions, holidays, missing dates.

2\. \*\*Validation\*\*: time-based holdout (last 16 days), never random splits.

3\. \*\*Baselines\*\*: naive, seasonal naive, 28-day moving average.

4\. \*\*Model\*\*: LightGBM on log1p(sales) with lags >= 16 days, rolling

&#x20;  means, calendar, promotions, oil price and national holidays.

5\. \*\*Business translation\*\*: inventory simulation (stockout vs overstock).



\## Decisions worth noting



\- `transactions.csv` was \*\*not\*\* used: it is not known at prediction

&#x20; time and would leak future information.

\- All lag features are >= 16 days, the forecast horizon.

\- Inventory costs are hypothetical; the point is the method.



\## What I would do next



\- Add regional and local holidays (only national ones are used today)

\- Quantile forecasts to set safety stock from prediction intervals

\- Serve the model behind an API (FastAPI + Docker)



\## How to run



1\. Download the data from Kaggle (Store Sales - Time Series

&#x20;  Forecasting) into `data/raw/`.

2\. `pip install -r requirements.txt`

3\. `python src/train.py`

4\. `streamlit run app/app.py`



\## Author



Nycollas - Mechatronics Engineering, Poli-USP

\[LinkedIn](https://www.linkedin.com/in/nycollas-guimaraes)

