import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load data
df = pd.read_csv("../data/enhanced_data.csv")

# -----------------------------
# Target Variable
# -----------------------------
df['Will_Buy_Again'] = df['Recency'].apply(lambda x: 0 if x > 30 else 1)

# -----------------------------
# Feature Selection
# -----------------------------
features = ['Recency', 'Frequency', 'Monetary', 'Avg_Order_Value']
X = df[features]
y = df['Will_Buy_Again']

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Model Training
# -----------------------------
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\n✅ Model Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# -----------------------------
# Save Model
# -----------------------------
with open("purchase_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model saved as purchase_model.pkl")