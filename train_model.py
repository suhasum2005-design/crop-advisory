import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load big dataset
df = pd.read_csv("data/crop_data.csv")

# Encode soil type
soil_encoder = LabelEncoder()
df["soil_enc"] = soil_encoder.fit_transform(df["soil"])

# Features & target
X = df[["soil_enc", "ph"]]
y = df["crop"]

# Train improved model
model = DecisionTreeClassifier(
    max_depth=6,
    min_samples_split=3,
    random_state=42
)
model.fit(X, y)

# Save model
joblib.dump(model, "crop_model.pkl")
joblib.dump(soil_encoder, "soil_encoder.pkl")

print("✅ Bigger ML model trained successfully")
print("📊 Total training samples:", len(df))
