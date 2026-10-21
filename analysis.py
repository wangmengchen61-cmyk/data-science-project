# -*- coding: utf-8 -*-
"""
Automobile Sales Analysis (1980-2023)
=====================================
A complete end-to-end analysis of the US automobile sales dataset:
load -> clean -> explore -> visualize -> key findings.

Dataset source:
  IBM Developer Skills Network (open dataset used in the IBM Data
  Visualization with Python course). Published for public use.

Run:
    python analysis.py
Outputs:
    - console summary of key findings
    - 4 figures saved to ./visualizations
"""

import os

import matplotlib

matplotlib.use("Agg")  # headless rendering

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "automobile-sales.csv")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)

plt.rcParams.update({"figure.dpi": 130, "axes.titlesize": 11})


# ---------------------------------------------------------------------------
# 1. Load and prepare
# ---------------------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# ---------------------------------------------------------------------------
# 2. Exploratory overview
# ---------------------------------------------------------------------------
def overview(df: pd.DataFrame) -> None:
    print("=" * 70)
    print("DATASET OVERVIEW")
    print("=" * 70)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Period: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"Vehicle types: {sorted(df['Vehicle_Type'].unique())}")
    print(f"Cities: {sorted(df['City'].unique())}")
    print(f"Missing values per column:\n{df.isna().sum()}")
    print("\nDescriptive statistics:\n")
    print(df.describe(include="number").round(2).to_string())


# ---------------------------------------------------------------------------
# 3. Visualizations
# ---------------------------------------------------------------------------
def fig_yearly_trend(df: pd.DataFrame) -> str:
    """Average yearly sales, with recession years highlighted."""
    yearly = df.groupby("Year")["Automobile_Sales"].mean().reset_index()
    recession_years = df.loc[df["Recession"] == 1, "Year"].unique()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(yearly["Year"], yearly["Automobile_Sales"],
            marker="o", ms=3, lw=1.6, color="#1f77b4", label="Average sales")
    for y in recession_years:
        ax.axvspan(y - 0.5, y + 0.5, color="#d62728", alpha=0.12)
    ax.set_title("Average Automobile Sales per Year (1980-2023)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Automobile Sales (units)")
    ax.legend(["Average sales", "Recession year"], loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(VIZ_DIR, "yearly_sales_trend.png")
    fig.savefig(path)
    plt.close(fig)
    return path


def fig_recession_by_vehicle_type(df: pd.DataFrame) -> str:
    """Average sales by vehicle type during recession vs non-recession."""
    g = (df.groupby(["Vehicle_Type", "Recession"])["Automobile_Sales"]
           .mean().unstack().reset_index())
    g.columns = ["Vehicle_Type", "Non-Recession", "Recession"]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = range(len(g))
    w = 0.36
    ax.bar([i - w / 2 for i in x], g["Non-Recession"], width=w,
           label="Non-Recession", color="#2ca02c")
    ax.bar([i + w / 2 for i in x], g["Recession"], width=w,
           label="Recession", color="#d62728")
    ax.set_xticks(list(x))
    ax.set_xticklabels(g["Vehicle_Type"], rotation=12, ha="right")
    ax.set_ylabel("Average Automobile Sales (units)")
    ax.set_title("Average Sales by Vehicle Type: Recession vs Non-Recession")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    path = os.path.join(VIZ_DIR, "sales_by_vehicle_type.png")
    fig.savefig(path)
    plt.close(fig)
    return path


def fig_advertising_share(df: pd.DataFrame) -> str:
    """Advertising expenditure share by vehicle type during recessions."""
    rec = df[df["Recession"] == 1]
    exp = (rec.groupby("Vehicle_Type")["Advertising_Expenditure"]
              .sum().sort_values(ascending=False))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.pie(exp.values, labels=exp.index, autopct="%1.1f%%",
           startangle=140, textprops={"fontsize": 8})
    ax.set_title("Advertising Expenditure Share by Vehicle Type\n(Recession Periods)")
    fig.tight_layout()
    path = os.path.join(VIZ_DIR, "advertising_share_recession.png")
    fig.savefig(path)
    plt.close(fig)
    return path


def fig_unemployment_vs_sales(df: pd.DataFrame) -> str:
    """Average sales vs unemployment rate during recessions."""
    rec = df[df["Recession"] == 1]
    g = (rec.groupby("unemployment_rate")["Automobile_Sales"].mean().reset_index())

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(g["unemployment_rate"], g["Automobile_Sales"],
            marker="o", ms=4, color="#9467bd")
    ax.set_xlabel("Unemployment Rate (%)")
    ax.set_ylabel("Average Automobile Sales (units)")
    ax.set_title("Average Automobile Sales vs Unemployment Rate (Recession Periods)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(VIZ_DIR, "unemployment_vs_sales.png")
    fig.savefig(path)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# 4. Key findings
# ---------------------------------------------------------------------------
def key_findings(df: pd.DataFrame) -> None:
    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)

    # Finding 1: recession vs non-recession overall
    overall = (df.groupby("Recession")["Automobile_Sales"].mean())
    print(f"1. Average sales during recessions: {overall[1]:.1f} units vs "
          f"{overall[0]:.1f} units outside recessions "
          f"(drop of {((overall[1]/overall[0]-1)*100):.1f}%).")

    # Finding 2: worst recession year
    yearly = df.groupby("Year")["Automobile_Sales"].mean()
    print(f"2. The lowest average sales year was {yearly.idxmin()} "
          f"({yearly.min():.1f} units).")

    # Finding 3: best-performing vehicle type overall
    vt = df.groupby("Vehicle_Type")["Automobile_Sales"].mean().sort_values()
    print(f"3. Best-selling vehicle type on average: {vt.index[-1]} "
          f"({vt.iloc[-1]:.1f} units); lowest: {vt.index[0]} ({vt.iloc[0]:.1f} units).")

    # Finding 4: correlation with economic indicators (recession periods)
    rec = df[df["Recession"] == 1]
    corr = rec[["Automobile_Sales", "unemployment_rate",
                "Consumer_Confidence", "GDP"]].corr()["Automobile_Sales"].drop("Automobile_Sales")
    print("4. Correlation of sales with economic indicators (recession):")
    print(corr.round(3).to_string())

    # Limitation
    print("\n5. Limitation: the dataset reports aggregated average sales per "
          "city/type/month rather than individual transactions, so "
          "driver-level factors (income, preferences) cannot be analysed.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    df = load_data(DATA_PATH)
    overview(df)
    paths = [
        fig_yearly_trend(df),
        fig_recession_by_vehicle_type(df),
        fig_advertising_share(df),
        fig_unemployment_vs_sales(df),
    ]
    key_findings(df)
    print("\nVisualizations saved:")
    for p in paths:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
