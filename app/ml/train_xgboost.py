import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_xgboost():
    print("📡 Loading Super-Dataset...")
    df = pd.read_parquet('app/ml/data/final_training_set.parquet')

    # 1. THE TIME-SERIES SPLIT (The "Honesty" Check)
    # Convert to datetime if it's not already
    df['tourney_date'] = pd.to_datetime(df['tourney_date'])
    
    # Train on everything before 2025
    train_df = df[df['tourney_date'] < '2025-01-01']
    # Test on everything 2025 and 2026
    test_df = df[df['tourney_date'] >= '2025-01-01']

    features = [c for c in df.columns if c not in [
        'p1_id', 'p2_id', 'p1_id_idx', 'p2_id_idx', 'surface', 
        'surface_idx', 'target', 'tourney_date' # REMOVE DATE FROM FEATURES
    ]]
    
    X_train, y_train = train_df[features], train_df['target']
    X_test, y_test = test_df[features], test_df['target']

    print(f"📈 Training on {len(X_train)} matches (Pre-2025)")
    print(f"🔮 Testing on {len(X_test)} matches (2025-2026)")

    # 3. Initialize XGBoost
    model = xgb.XGBClassifier(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='binary:logistic',
        early_stopping_rounds=50,
        random_state=42
    )

    # 4. Fit with Early Stopping
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=100
    )

    # 5. Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    print("\n--- Final Performance ---")
    print(f"✅ Accuracy: {acc:.2%}")
    print(classification_report(y_test, preds))

    # 6. Save the Final Model
    joblib.dump(model, 'app/ml/models/final_xgboost_model.pkl')
    # Save the list of feature names so the API knows the exact order later
    joblib.dump(features, 'app/ml/models/feature_names.pkl')
    print("🏁 Final Model saved to app/ml/models/final_xgboost_model.pkl")

    # Get feature importance
    importance = model.feature_importances_
    feature_names = X_train.columns
    feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importance}).sort_values(by='importance', ascending=False)

    print("\n--- Top 10 Most Important Features ---")
    print(feature_importance_df.head(10))

if __name__ == "__main__":
    train_xgboost()
