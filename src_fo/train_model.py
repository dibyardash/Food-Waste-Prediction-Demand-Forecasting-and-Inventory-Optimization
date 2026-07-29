import pandas as pd
import joblib
 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
 
from xgboost import XGBRegressor
 
from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)
 
df = pd.read_csv(
    "Food Waste Cleaned.csv"
)
 
df["Date"] = pd.to_datetime(
    df["Date"]
)
 
df["Day"] = df["Date"].dt.day
df["Month"] = df["Date"].dt.month
df["Weekday"] = df["Date"].dt.weekday
 
df["Weekend_Flag"] = (
    df["Weekday"] >= 5
).astype(int)
 
meal_encoder = LabelEncoder()
food_encoder = LabelEncoder()
 
df["Meal_Type"] = meal_encoder.fit_transform(
    df["Meal_Type"]
)
 
df["Food_Item"] = food_encoder.fit_transform(
    df["Food_Item"]
)
 

# DEMAND MODEL

 
demand_features = [
 
    "Meal_Type",
    "Food_Item",
    "Temperature",
    "Rainfall",
    "Holiday_Flag",
    "Event_Flag",
    "Previous_Day_Sales",
    "Previous_Day_Waste",
    "Day",
    "Month",
    "Weekday",
    "Weekend_Flag"
 
]
 
X_demand = df[demand_features]
 
y_demand = df["Quantity_Sold"]
 
X_train, X_test, y_train, y_test = train_test_split(
 
    X_demand,
    y_demand,
 
    test_size=0.2,
 
    random_state=42
)
 
demand_model = XGBRegressor(
 
    n_estimators=300,
 
    learning_rate=0.05,
 
    max_depth=6,
 
    random_state=42
)
 
demand_model.fit(
    X_train,
    y_train
)
 
pred = demand_model.predict(
    X_test
)
 
print(
    "Demand MAE:",
    mean_absolute_error(
        y_test,
        pred
    )
)
 
print(
    "Demand R2:",
    r2_score(
        y_test,
        pred
    )
)
 
joblib.dump(
    demand_model,
    "demand_model.pkl"
)
 

# WASTE MODEL

 
waste_features = [
 
    "Meal_Type",
    "Food_Item",
    "Quantity_Prepared",
    "Temperature",
    "Rainfall",
    "Holiday_Flag",
    "Event_Flag",
    "Previous_Day_Sales",
    "Previous_Day_Waste",
    "Day",
    "Month",
    "Weekday",
    "Weekend_Flag"
 
]
 
X_waste = df[waste_features]
 
y_waste = df["Quantity_Wasted"]
 
X_train, X_test, y_train, y_test = train_test_split(
 
    X_waste,
    y_waste,
 
    test_size=0.2,
 
    random_state=42
 
)
 
waste_model = RandomForestRegressor(
 
    n_estimators=300,
 
    max_depth=12,
 
    random_state=42
 
)
 
waste_model.fit(
    X_train,
    y_train
)
 
pred = waste_model.predict(
    X_test
)
 
print(
    "Waste MAE:",
    mean_absolute_error(
        y_test,
        pred
    )
)
 
print(
    "Waste R2:",
    r2_score(
        y_test,
        pred
    )
)
 
joblib.dump(
    waste_model,
    "waste_model.pkl"
)
 
joblib.dump(
    meal_encoder,
    "meal_encoder.pkl"
)
 
joblib.dump(
    food_encoder,
    "food_encoder.pkl"
)
 
print(
    "✅ Models Saved Successfully"
)