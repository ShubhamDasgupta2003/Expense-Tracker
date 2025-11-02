from sklearn.metrics import f1_score, classification_report
import joblib

import pandas as pd
import numpy as np

# A function to generate a dummy dataset for testing
def create_dummy_test_data():
    # Simulate normal expenses across different categories
    data = {
        'cat_code': ['SHOP'],
        'amount': [800], # Normal FOOD amounts
        'label': [1] # '1' for normal
    }

    # Create the DataFrame
    df_test = pd.DataFrame(data)
    
    return df_test


def preprocess_test_data(df_test, feature_columns):
    # Calculate category-specific statistics
    # Note: These are not ideal for single data points, but match the training logic
    df_test['cat_mean'] = df_test.groupby('cat_code')['amount'].transform('mean')
    df_test['cat_std'] = df_test.groupby('cat_code')['amount'].transform('std').fillna(0)

    # Create new contextual features
    df_test['amount_diff_from_cat_mean'] = df_test['amount'] - df_test['cat_mean']
    df_test['amount_zscore'] = (df_test['amount'] - df_test['cat_mean']) / df_test['cat_std']
    df_test['amount_zscore'] = df_test['amount_zscore'].replace([np.inf, -np.inf], 0)
    df_test['amount_zscore'].fillna(0, inplace=True)

    # Apply one-hot encoding
    categorical_cols = ['cat_code']
    df_encoded = pd.get_dummies(df_test, columns=categorical_cols, drop_first=True)

    # Reindex and fill missing columns to align with training data
    # This ensures that even if 'GROC' wasn't in the training data,
    # the column structure is consistent.
    # The new 'cat_code_GROC' column will have to be handled.
    df_final = df_encoded.reindex(columns=feature_columns, fill_value=0)
    
    # If a new category appears (like GROC in your test data, if not in train)
    # the corresponding column will be added with 0s because of the fill_value=0
    # when you reindex with the training feature_columns.
    # We need to manually add the column if it's missing.
    # A better approach is to store the encoder itself.
    
    # For a robust solution, you should use the scikit-learn OneHotEncoder
    # and save it along with your model, but for now, this will work.
    
    # Check if the specific category column exists after reindexing
    cat_code_test_cat = f"cat_code_{df_test['cat_code'].iloc[0]}"
    if cat_code_test_cat in df_final.columns:
        df_final[cat_code_test_cat] = 1 # Set it to 1
    
    df_final.to_csv('test_dataframe.csv')
    return df_final


# Load the trained model and feature columns
try:
    model_data = joblib.load('isolation_forest_model.joblib')
    model = model_data['model']
    feature_columns = model_data['feature_columns']
except FileNotFoundError:
    print("Error: 'isolation_forest_model.joblib' not found. Please train the model first.")
    exit()

# Generate and preprocess dummy test data
df_test_raw = create_dummy_test_data()
X_test = preprocess_test_data(df_test_raw, feature_columns)
y_true = df_test_raw['label']

# Get predictions from the model
y_pred = model.predict(X_test)

print(X_test)
# Print results
print("Actual Labels (y_true):", list(y_true))
print("Predicted Labels (y_pred):", list(y_pred))

