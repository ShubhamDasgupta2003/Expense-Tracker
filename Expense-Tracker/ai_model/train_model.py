import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import LocalOutlierFactor


def train_and_save_model():
    """
    Trains an Isolation Forest model using selected features and saves it.

    Raises:
        FileNotFoundError: If 'expenses.csv' is not found.
    """
    try:
        df = pd.read_csv('expense.csv', usecols=['cat_code', 'amount'], dtype={'cat_code': 'category', 'amount': float})
        print("Loaded data from expenses.csv")
    except FileNotFoundError:
        print("Error: 'expenses.csv' not found.")
        raise
    except ValueError as e:
            # Capture and provide more context for the ValueError
            print(f"Data loading error: {e}")
            print("Please check if the data in 'amount' column is all numeric.")
            return
    
    # Calculate category-specific statistics
    df['cat_mean'] = df.groupby('cat_code')['amount'].transform('mean')
    df['cat_std'] = df.groupby('cat_code')['amount'].transform('std').fillna(0)

# Create new contextual features
    df['amount_diff_from_cat_mean'] = df['amount'] - df['cat_mean']
    df['amount_zscore'] = (df['amount'] - df['cat_mean']) / df['cat_std']
    df['amount_zscore'] = df['amount_zscore'].replace([float('inf'), float('-inf')], 0)
    df['amount_zscore'].fillna(0, inplace=True)


    # 1. Define the specific columns for each data type
    categorical_cols = ['cat_code']
    numerical_cols = ['amount','amount_diff_from_cat_mean','amount_zscore'] # Columns to keep as-is

    # 2. Apply one-hot encoding to only the specified categorical columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # 3. Select all the columns that will be used for training
    # This includes the numerical columns from the original DataFrame,
    # and all the newly created one-hot encoded columns.
    feature_columns = numerical_cols + [col for col in df_encoded.columns if col not in categorical_cols]
    df_final = df_encoded[feature_columns]

    # 4. Train the Isolation Forest model
    #model = IsolationForest(n_estimators=300,random_state=42)
    model = LocalOutlierFactor(n_neighbors=20, contamination='auto', novelty=True)
    model.fit(df_final)

    # 5. Save the model and feature columns
    model_data = {
        'model': model,
        'feature_columns': feature_columns
    }

    joblib.dump(model_data, 'isolation_forest_model.joblib')
    print("Isolation Forest model and feature columns saved to isolation_forest_model.joblib")
    df_final.to_csv('final_dataframe.csv')

# Example usage (will raise an error if expenses.csv is not present)
if __name__ == '__main__':
    try:
        train_and_save_model()
    except FileNotFoundError:
        print("Model training failed. Please ensure 'expenses.csv' exists.")



