import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from sklearn.model_selection import GridSearchCV

def train_and_save_model():
    """
    Trains an Isolation Forest model using selected features and saves it.

    Raises:
        FileNotFoundError: If 'expenses.csv' is not found.
    """
    try:
        df = pd.read_csv('expense.csv', usecols=['cat_code', 'amount', 'is_weekend'], dtype={'cat_code': 'category', 'amount': float, 'is_weekend': int})
        print("Loaded data from expenses.csv")
    except FileNotFoundError:
        print("Error: 'expenses.csv' not found.")
        raise
    except ValueError as e:
            # Capture and provide more context for the ValueError
            print(f"Data loading error: {e}")
            print("Please check if the data in 'amount' column is all numeric.")
            return
    
    # During the training process, calculate the mean amount for each category
    df_mean_amount = df.groupby('cat_code')['amount'].transform('mean')
    df['amount_diff_from_cat_mean'] = df['amount'] - df_mean_amount

    # 1. Define the specific columns for each data type
    categorical_cols = ['cat_code']
    numerical_cols = ['amount','is_weekend','amount_diff_from_cat_mean'] # Columns to keep as-is

    # 2. Apply one-hot encoding to only the specified categorical columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # 3. Select all the columns that will be used for training
    # This includes the numerical columns from the original DataFrame,
    # and all the newly created one-hot encoded columns.
    feature_columns = numerical_cols + [col for col in df_encoded.columns if col not in categorical_cols]
    df_final = df_encoded[feature_columns]

    # 4. Train the Isolation Forest model
    # model = IsolationForest(random_state=42)
    # model.fit(df_final)

# Define a parameter grid to search
    param_grid = {
        'n_estimators': [100, 200, 300],
        'contamination': [0.005, 0.01, 0.05, 'auto'], # Test different contamination levels
        'max_samples': [128, 256, 512, 'auto']
    }
    
    # Initialize the model and GridSearchCV
    if_model = IsolationForest(random_state=42)
    grid_search = GridSearchCV(if_model, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)

    # Train the model with the best parameters
    grid_search.fit(df_final)
    best_model = grid_search.best_estimator_

    # 5. Save the model and feature columns
    model_data = {
        'model': best_model,
        'feature_columns': feature_columns
    }
    joblib.dump(model_data, 'isolation_forest_model.joblib')
    print("Isolation Forest model and feature columns saved to isolation_forest_model.joblib")

# Example usage (will raise an error if expenses.csv is not present)
if __name__ == '__main__':
    try:
        train_and_save_model()
    except FileNotFoundError:
        print("Model training failed. Please ensure 'expenses.csv' exists.")
