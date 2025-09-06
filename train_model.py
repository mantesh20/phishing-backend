import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1) Load dataset
csv_file = "dataset.csv"
print(f"📂 Loading dataset from: {csv_file}")
df = pd.read_csv(csv_file)

print("✅ Dataset loaded!")
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)
print("First 5 rows:")
print(df.head())

# 2) Use 'Result' as target column explicitly
target_col = "Result"
if target_col not in df.columns:
    print(f"❌ ERROR: Dataset must have a '{target_col}' column as target.")
    exit()

y = df[target_col]

# 3) Map target values: -1 -> 1 (phishing), 1 -> 0 (safe)
unique_vals = set(y.unique())
if unique_vals == {-1, 1}:
    print("Mapping target: -1 -> 1 (phishing), 1 -> 0 (safe)")
    y = (y == -1).astype(int)
else:
    print(f"❌ Unexpected target values: {unique_vals}. Expected -1 and 1.")
    exit()

# 4) Prepare features: drop target and index columns, keep numeric only
X = df.drop(columns=[target_col])
for col in ["index", "Index", "Unnamed: 0"]:
    if col in X.columns:
        X = X.drop(columns=[col])

X_num = X.select_dtypes(include=[np.number])
if X_num.shape[1] == 0:
    print("❌ No numeric features found.")
    exit()

X_num = X_num.fillna(0)
print("✅ Using features:", X_num.columns.tolist())

# 5) Train/test split and model training
X_train, X_test, y_train, y_test = train_test_split(X_num, y, test_size=0.2, random_state=42)
print("Training Logistic Regression...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Training complete — accuracy: {acc:.3f}")

# 6) Save model and feature names
joblib.dump(model, "phishing_model.pkl")
joblib.dump(list(X_num.columns), "feature_names.pkl")
print("💾 Saved: phishing_model.pkl, feature_names.pkl")

print("\n📝 Example JSON to send to /predict:")
print({name: 0 for name in X_num.columns})


