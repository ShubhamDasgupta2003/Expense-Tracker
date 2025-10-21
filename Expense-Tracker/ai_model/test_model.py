import pandas as pd
import joblib

def predict_anomalies_with_model(new_data):
    """
    Loads a pre-trained model and predicts anomalies on new data.
    """
    # 1. Load the model and feature columns
    model_data = joblib.load('isolation_forest_model.joblib')
    model = model_data['model']
    feature_columns = model_data['feature_columns']
    print("Model and feature columns loaded successfully.")

    # 2. Preprocess the new data using the same steps as training
    # We need to apply the same one-hot encoding on the 'cat_code' column.
    categorical_cols = ['cat_code']
    new_data_encoded = pd.get_dummies(new_data, columns=categorical_cols, drop_first=True)

    # 3. Align the columns with the training data
    # Ensure the new data has the same columns in the same order as the training data.
    new_data_final = new_data_encoded.reindex(columns=feature_columns, fill_value=0)

    scores = model.decision_function(new_data_final)
    print(scores)
    # 4. Make predictions
    predictions = model.predict(new_data_final)
    
    # 5. Add predictions to the original new data for display
    new_data['is_anomaly'] = predictions
    new_data['is_anomaly'] = new_data['is_anomaly'].apply(lambda x: 'Yes' if x == -1 else 'No')
    return new_data

if __name__ == '__main__':
    # Define some new dummy data for testing
    # This data includes a regular entry and a potential anomaly
    new_test_data = pd.DataFrame([
        ['GROC', 75.00, 0],    # Normal entry
        ['FOOD', 60.00, 1],     # Normal entry
        ['FOOD', 5000.00, 0],   # Anomalous amount
        ['TRVL', 250.00, 1],    # Normal entry
        ['TEA',450.00,0],
        # ['SALARY', 1000000.00, 0],   # Anomalous category not seen in training
    ], columns=['cat_code', 'amount', 'is_weekend'])
    
    # Predict and display the results
    results = predict_anomalies_with_model(new_test_data)
    
    print("\n--- New Data Predictions ---")
    print(results)
