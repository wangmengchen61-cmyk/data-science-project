# Automobile Sales Data Analysis (1980–2023)

An end-to-end data science project that explores how US automobile sales
behave during economic recessions, using an open dataset of monthly
automobile sales across four states and five vehicle types.

## Research Question

How do automobile sales respond to economic recessions, and which vehicle
segments are affected the most?

## Dataset

- **Source:** IBM Developer Skills Network — *Automobile Sales* open dataset
  (the same dataset used in the official IBM *Data Visualization with Python*
  course materials).
- **Content:** monthly automobile sales statistics for 1980–2023 across
  California, Georgia, Illinois and New York, including vehicle type, average
  price, advertising expenditure, consumer confidence, GDP, growth rate and
  unemployment rate, plus a binary flag marking recession periods.
- **Usage permissions:** published by IBM as an open educational dataset;
  free to use for learning, teaching and research purposes. It contains no
  personal or restricted data.

## Methods & Tools

- **Language / libraries:** Python with `pandas` (data wrangling),
  `matplotlib` (static visualizations), `plotly` + `dash` (interactive
  dashboard).
- **Approach:** data loading and cleaning → exploratory analysis →
  recession vs non-recession comparisons → correlation analysis of economic
  indicators → static charts and an interactive dashboard.

## Key Findings

1. Average monthly sales drop by about **62.5%** during recession years
   (1,382 units vs 3,680 units outside recessions).
2. The lowest average sales year in the dataset is **1981** (549 units),
   reflecting the early-1980s recession.
3. **Small Family Cars** are the best-selling segment overall (≈3,494 units
   on average), while Executive Cars sell the least (≈2,741 units).
4. During recessions, sales correlate negatively with the unemployment rate
   (r ≈ −0.18), suggesting higher unemployment is associated with weaker
   automobile demand.

## Limitation

The dataset contains **aggregated monthly statistics per city and vehicle
type** rather than individual transactions. As a result, buyer-level factors
such as household income, financing conditions or personal preferences cannot
be analysed, and the findings describe market-level patterns only.

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/data-science-project.git
cd data-science-project

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4a. Run the static analysis (prints findings, saves charts)
python analysis.py

# 4b. Or run the interactive dashboard
python dashboard.py
# then open http://127.0.0.1:8050
```

## Repository Structure

```
data-science-project/
├── analysis.py            # end-to-end analysis script (load → explore → visualize)
├── dashboard.py           # interactive Dash dashboard
├── requirements.txt       # Python dependencies
├── data/
│   └── automobile-sales.csv   # open dataset (IBM)
├── notebooks/             # (optional) Jupyter notebooks
└── visualizations/
    ├── yearly_sales_trend.png          # Fig 1: yearly trend with recession years
    ├── sales_by_vehicle_type.png       # Fig 2: recession vs non-recession by type
    ├── advertising_share_recession.png # Fig 3: ad spend share during recessions
    └── unemployment_vs_sales.png       # Fig 4: unemployment rate vs sales
```

## License / Notes

This repository contains **no passwords, API keys, personal data or
restricted datasets**. The dataset is public and educational; the analysis
code is released for learning purposes.
