import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_data

sns.set_theme(style="whitegrid")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports", "figures")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_eda():
    df = load_data()
    
    # Target Definition: G3 < 10 is At Risk (1), else Not At Risk (0)
    df["Academic_Risk"] = (df["G3"] < 10).astype(int)
    risk_counts = df["Academic_Risk"].value_counts()
    
    print("\n--- Academic Risk Distribution ---")
    print(f"Not At Risk (0): {risk_counts[0]} ({risk_counts[0] / len(df) * 100:.2f}%)")
    print(f"At Risk (1):     {risk_counts[1]} ({risk_counts[1] / len(df) * 100:.2f}%)")

    # Plot 1: Target Class Imbalance
    plt.figure(figsize=(7, 4.5))
    ax = sns.countplot(x="Academic_Risk", data=df, palette=["#2a9d8f", "#e76f51"])
    plt.title("Academic Risk Class Distribution (n=649)", fontsize=13, weight="bold")
    plt.xticks([0, 1], ["Not At Risk (0)", "At Risk (1)"])
    plt.xlabel("Target Status")
    plt.ylabel("Number of Students")
    for p in ax.patches:
        height = int(p.get_height())
        ax.annotate(f"{height} ({height / len(df) * 100:.1f}%)",
                    (p.get_x() + p.get_width() / 2.0, height),
                    ha="center", va="bottom", fontsize=10, xytext=(0, 4), textcoords="offset points")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, "class_distribution.png"), dpi=300)
    plt.close()

    # Plot 2: Distribution of Final Grade (G3)
    plt.figure(figsize=(8, 4.5))
    sns.histplot(df["G3"], bins=20, kde=True, color="#1d3557")
    plt.axvline(10, color="#e63946", linestyle="--", linewidth=2, label="Pass Threshold (G3=10)")
    plt.axvline(df["G3"].mean(), color="#f4a261", linestyle="-", linewidth=2, label=f'Mean = {df["G3"].mean():.2f}')
    plt.title("Distribution of Final Grade (G3)", fontsize=13, weight="bold")
    plt.xlabel("G3 (Final Grade)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, "g3_distribution.png"), dpi=300)
    plt.close()

    # Plot 3: Absences Boxplot & Outliers
    plt.figure(figsize=(8, 3))
    sns.boxplot(x=df["absences"], color="#a8dadc", flierprops=dict(marker="o", markersize=6, markerfacecolor="#e63946"))
    plt.title("Box Plot of Absences (Right-skewed with Upper Outliers)", fontsize=12, weight="bold")
    plt.xlabel("Absences")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, "absences_boxplot.png"), dpi=300)
    plt.close()

    # Plot 4: Numerical Feature Correlation Matrix
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    plt.figure(figsize=(10, 8))
    corr = df[num_cols].corr()
    sns.heatmap(corr, cmap="viridis", annot=False, fmt=".2f", cbar=True)
    plt.title("Correlation Matrix of Numerical Variables", fontsize=13, weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, "correlation_matrix.png"), dpi=300)
    plt.close()

    print(f"[SUCCESS] All EDA figures generated in: {REPORTS_DIR}")

if __name__ == "__main__":
    run_eda()
