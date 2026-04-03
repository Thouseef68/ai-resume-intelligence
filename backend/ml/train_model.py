import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load data
df = pd.read_csv("final_dataset.csv")

df = df.dropna()
# Combine resume + job
df["resume"] = df["resume"].astype(str)
df["job"] = df["job"].astype(str)

df["text"] = df["resume"] + " " + df["job"]

# Features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

# Labels
y = df["label"]

# Train model
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss'
)

model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained and saved")