import pandas as pd
import joblib
import numpy as np

def test_model_on_new_data(new_data_list):
    # ... (code to load model and features) ...
    try:
        model_data = joblib.load('random_forest_model_fixed.joblib') # Load the fixed model file
        model = model_data['model']
        feature_columns = model_data['feature_columns']
        train_stats = model_data['train_stats'] # Load the crucial training stats
        print("Model and training statistics loaded successfully.")

    except FileNotFoundError:
        print("Error: 'random_forest_model_fixed.joblib' not found. Please train the model first.")
        return

    # Convert new data list to a DataFrame
    new_df = pd.DataFrame(new_data_list)
    
    # --- Use a consistent apply_features function from training script ---
    def apply_features_test(data_df, stats_df):
        data_df = data_df.copy()
        data_df['cat_code'] = data_df['cat_code'].astype(str) # Ensure string type

        # Map training stats to new data
        data_df['cat_mean'] = data_df['cat_code'].map(stats_df['mean'])
        data_df['cat_std'] = data_df['cat_code'].map(stats_df['std']).fillna(0)
        
        # Handle cases where a category in test data was unseen in training data (will result in NaN mean/std)
        data_df['cat_mean'].fillna(data_df['amount'].mean(), inplace=True) # Fallback to overall mean if category unseen
        data_df['cat_std'].fillna(data_df['amount'].std() or 1, inplace=True) # Fallback std or 1

        data_df['amount_diff_from_cat_mean'] = data_df['amount'] - data_df['cat_mean']
        
        return data_df

    new_df_processed = apply_features_test(new_df, train_stats)

    # 3. Apply one-hot encoding
    categorical_cols = ['cat_code']
    new_df_encoded = pd.get_dummies(new_df_processed, columns=categorical_cols, drop_first=True)

    # Align columns with the model's expected features
    final_new_df = new_df_encoded.reindex(columns=feature_columns, fill_value=0)

    # 4. Make predictions
    predictions = model.predict(final_new_df)
    probabilities = model.predict_proba(final_new_df)

    # Add predictions back to the original new data for clarity
    new_df['prediction'] = predictions
    new_df['is_anomaly'] = new_df['prediction'].apply(lambda x: "Anomaly" if x == 1 else "Normal")
    new_df['normal_prob'] = probabilities[:, 0]
    new_df['anomaly_prob'] = probabilities[:, 1]

    print("\nPredictions on New Data:")
    print(new_df[['cat_code', 'amount', 'is_anomaly', 'anomaly_prob']])

# Example usage (will raise an error if expenses.csv is not present)
if __name__ == '__main__':
    # Make sure to run train_and_save_model_rf_fixed() first
    random_new_expenses = [
        {'cat_code': 'TRVL', 'amount': 641.0}, # The specific expense you are testing
        {'cat_code': 'TRVL', 'amount': 1000.0},
        {'cat_code': 'FOOD', 'amount': 650.0},
        {'cat_code': 'MOBRC', 'amount': 240.00},
        {'cat_code': 'TEA', 'amount': 13.00},
        {'cat_code': 'GROC', 'amount': 2800.00}
    ]
    
    test_model_on_new_data(random_new_expenses)
