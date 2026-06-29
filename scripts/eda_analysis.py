import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_clean_data(path="cleaned_data/cleaned_dataset.csv"):
    return pd.read_csv(path)

def run_eda(df):
    print("🔎 Dataset Info:")
    print(df.info())
    print("\n📊 Summary Statistics:")
    print(df.describe())

    # Example 1: ESG Score over Years
    plt.figure(figsize=(10,6))
    sns.lineplot(data=df, x="Year", y="ESG_Overall", hue="Industry", ci=None)
    plt.title("Industry ESG Scores Over Time")
    plt.show()

    # Example 2: Water Usage by Company (instead of missing Resource_Utilization)
    plt.figure(figsize=(12,6))
    sns.barplot(data=df, x="CompanyName", y="WaterUsage")
    plt.title("Water Usage by Company")
    plt.xticks(rotation=90)
    plt.show()


if __name__ == "__main__":
    df = load_clean_data()
    run_eda(df)
