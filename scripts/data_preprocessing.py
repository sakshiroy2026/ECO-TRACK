import pandas as pd

def load_data(path="data/company_esg_financial_dataset.csv"):
    """Load raw dataset"""
    return pd.read_csv(path)

def clean_data(df):
    """Clean dataset: handle missing values, types, duplicates"""
    # Drop duplicates
    df = df.drop_duplicates()

    # Fill missing numerical values with median
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Fill missing categorical with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

def save_clean_data(df, path="cleaned_data/cleaned_dataset.csv"):
    """Save cleaned dataset"""
    df.to_csv(path, index=False)

if __name__ == "__main__":
    raw_df = load_data()
    clean_df = clean_data(raw_df)
    save_clean_data(clean_df)
    print("✅ Cleaned data saved at cleaned_data/cleaned_dataset.csv")
