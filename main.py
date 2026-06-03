
# Customer Churn AI Project
# Data Analysis - Phase 1
# ==========================================

# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("Customer_Churn.csv")


# ==========================================
# Basic Dataset Information
# ==========================================

print("\n===== Dataset Information =====")

print(df.head())

print(df.info())

print(df.isnull().sum())


# ==========================================
# Dashboard Summary
# ==========================================

print("\n===== Customer Churn Dashboard =====")

# Total Customers
total_customers = len(df)

# Customers Who Left
churned_customers = len(
    df[df["Churn"] == "Yes"]
)

# Customers Who Stayed
retained_customers = len(
    df[df["Churn"] == "No"]
)

# Average Monthly Charges
average_monthly_charges = round(
    df["MonthlyCharges"].mean(),
    2
)

print("Total Customers:",
      total_customers)

print("Churned Customers:",
      churned_customers)

print("Retained Customers:",
      retained_customers)

print("Average Monthly Charges:",
      average_monthly_charges)


# ==========================================
# Analysis 1
# Customer Churn Distribution
# ==========================================

churn_distribution = (
    df["Churn"]
    .value_counts()
)

print("\n===== Churn Distribution =====")

print(churn_distribution)


# ==========================================
# Visualization 1
# Churn Distribution Pie Chart
# ==========================================

churn_distribution.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title(
    "Customer Churn Distribution"
)

plt.ylabel("")

plt.show()
# ==========================================
# Analysis 2
# Churn by Contract Type
# ==========================================

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"]
)

print("\n===== Churn By Contract Type =====")

print(contract_churn)


# ==========================================
# Visualization 2
# Churn by Contract Type
# ==========================================

contract_churn.plot(
    kind="bar"
)

plt.title(
    "Customer Churn by Contract Type"
)

plt.xlabel("Contract Type")

plt.ylabel("Customers")

plt.show()
# ==========================================
# Analysis 3
# Monthly Charges by Churn
# ==========================================

monthly_charges = (
    df.groupby("Churn")["MonthlyCharges"]
    .mean()
)

print("\n===== Average Monthly Charges =====")

print(monthly_charges)


# ==========================================
# Visualization 3
# Average Monthly Charges
# ==========================================

monthly_charges.plot(
    kind="bar"
)

plt.title(
    "Average Monthly Charges by Churn"
)

plt.xlabel("Churn")

plt.ylabel("Average Monthly Charges")

plt.show()
# ==========================================
# Analysis 4
# Customer Tenure by Churn
# ==========================================

tenure_analysis = (
    df.groupby("Churn")["tenure"]
    .mean()
)

print("\n===== Average Customer Tenure =====")

print(tenure_analysis)


# ==========================================
# Visualization 4
# Average Tenure by Churn
# ==========================================

tenure_analysis.plot(
    kind="bar"
)

plt.title(
    "Average Customer Tenure by Churn"
)

plt.xlabel("Churn")

plt.ylabel("Average Months")

plt.show()
# ==========================================
# Data Preparation For Machine Learning
# ==========================================

from sklearn.preprocessing import LabelEncoder

df_ml = df.copy()

encoder = LabelEncoder()

for column in df_ml.columns:

    if df_ml[column].dtype == "object":

        df_ml[column] = encoder.fit_transform(
            df_ml[column]
        )

print("\n===== Encoded Dataset =====")

print(df_ml.head())
# ==========================================
# Machine Learning Model
# ==========================================

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("\n===== Machine Learning Model =====")

df_ml = df.copy()

# Remove customer ID because it is not useful for prediction
df_ml = df_ml.drop("customerID", axis=1)

# Convert TotalCharges from text to number
df_ml["TotalCharges"] = pd.to_numeric(
    df_ml["TotalCharges"],
    errors="coerce"
)

# Fill missing values after conversion
df_ml["TotalCharges"] = df_ml["TotalCharges"].fillna(
    df_ml["TotalCharges"].median()
)

# Convert categorical columns to numbers
df_ml = pd.get_dummies(
    df_ml,
    drop_first=True
)

# Features and Target
X = df_ml.drop("Churn_Yes", axis=1)
joblib.dump(X.columns.tolist(), "model_columns.pkl")
y = df_ml["Churn_Yes"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train Model
model.fit(X_train, y_train)

# Make Predictions
predictions = model.predict(X_test)

# Evaluate Model
accuracy = accuracy_score(
    y_test,
    predictions
)

print("Model Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, predictions))
# ==========================================
# Confusion Matrix
# ==========================================

cm = confusion_matrix(
    y_test,
    predictions
)

print("\nConfusion Matrix:")

print(cm)
# Save Model
joblib.dump(
    model,
    "churn_model.pkl"
)

print("Model Saved Successfully")