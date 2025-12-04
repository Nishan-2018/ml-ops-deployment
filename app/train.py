import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# 1. Load Data
print("Loading California Housing dataset...")
data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Select specific features for simplicity
# MedInc: Median Income
# HouseAge: Median House Age
# AveRooms: Average number of rooms
# Population: Population
selected_features = ['MedInc', 'HouseAge', 'AveRooms', 'Population']
X = X[selected_features]

# 2. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train Model
print("Training RandomForestRegressor...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Model MSE: {mse}")

# 5. Save Model
joblib.dump(model, 'model.joblib')
print("Model saved to model.joblib")
