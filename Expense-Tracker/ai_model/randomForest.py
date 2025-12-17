import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler # Needed for proper scaling
import joblib
import numpy as np

def train_and_save_model_rf_fixed():
    """
    Trains a Random Forest Classifier with corrected feature engineering to avoid data leakage.
    """
    try:
        df = pd.read_csv('expense.csv', usecols=['cat_code', 'amount', 'is_anomaly'], dtype={'cat_code': 'category', 'amount': float, 'is_anomaly': int})
        print("Loaded data from expenses.csv")
    except FileNotFoundError:
        print("Error: 'expenses.csv' not found. Make sure it exists and contains 'is_anomaly' column.")
        raise
    except ValueError as e:
        print(f"Data loading error: {e}")
        print("Please check data types, especially if 'amount' is all numeric and 'is_anomaly' is integer (0/1).")
        return
    
    # 1. Split data *first* before any feature engineering or statistics calculation
    X = df.drop('is_anomaly', axis=1)
    y = df['is_anomaly']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # 2. Perform feature engineering ONLY on the training set and apply to test set
    
    # Calculate category-specific statistics *only* from the training data
    train_stats = X_train.groupby('cat_code')['amount'].agg(['mean', 'std']).fillna(0)
    
    # Function to apply feature engineering
    def apply_features(data_df, stats_df):
        data_df = data_df.copy()
        
        # Convert cat_code to string type to avoid categorical constraints during mapping/filling
        data_df['cat_code'] = data_df['cat_code'].astype(str) 
        
        data_df['cat_mean'] = data_df['cat_code'].map(stats_df['mean'])
        data_df['cat_std'] = data_df['cat_code'].map(stats_df['std']).fillna(0)
        data_df['amount_diff_from_cat_mean'] = data_df['amount'] - data_df['cat_mean']
        
        return data_df


    X_train_processed = apply_features(X_train, train_stats)
    X_test_processed = apply_features(X_test, train_stats) # Apply same stats to test data

    # 3. Apply one-hot encoding
    categorical_cols = ['cat_code']
    X_train_encoded = pd.get_dummies(X_train_processed, columns=categorical_cols, drop_first=True)
    X_test_encoded = pd.get_dummies(X_test_processed, columns=categorical_cols, drop_first=True)

    # Align test columns with training columns (important for production use)
    X_test_encoded = X_test_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)
    
    feature_columns = X_train_encoded.columns.tolist()

    # 4. Train the Random Forest Classifier model
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train_encoded, y_train) # Fit with processed training data and labels

    # 5. Make predictions and evaluate
    y_pred = model.predict(X_test_encoded) # Predict using processed test data
    print("\nModel Evaluation on Test Data (Fixed):")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # 6. Save the model and feature columns
    model_data = {
        'model': model,
        'feature_columns': feature_columns,
        'train_stats': train_stats # Save the training stats for future use on new data
    }
    joblib.dump(model_data, 'random_forest_model_fixed.joblib')
    print("\nFixed Random Forest model saved to random_forest_model_fixed.joblib")

# Example usage
if __name__ == '__main__':
    try:
        train_and_save_model_rf_fixed()
    except FileNotFoundError:
        print("Model training failed. Please ensure 'expenses.csv' exists with the 'is_anomaly' column.")
