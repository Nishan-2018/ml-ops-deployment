from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    print("Loading data...")
    iris = load_iris()
    X, y = iris.data, iris.target

    print("Training model...")
    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    clf.fit(X, y)

    print("Saving model...")
    joblib.dump(clf, "model.joblib")
    print("Model saved to model.joblib")

if __name__ == "__main__":
    train_model()
