from flask import Flask, request, jsonify
import pandas as pd
import joblib
 
from inventory_optimizer import InventoryOptimizer


# INITIALIZE APP


app = Flask(__name__)
 

# LOAD MODELS

 
try:
 
    demand_model = joblib.load(
        "demand_model.pkl"
    )
 
    waste_model = joblib.load(
        "waste_model.pkl"
    )
 
    meal_encoder = joblib.load(
        "meal_encoder.pkl"
    )
 
    food_encoder = joblib.load(
        "food_encoder.pkl"
    )
 
    optimizer = InventoryOptimizer()
 
    print("✅ Models Loaded Successfully")
 
except Exception as e:
 
    print(f"❌ Error Loading Models: {e}")
    raise e
 

# HOME ROUTE

 
@app.route("/")
def home():
 
    return jsonify({
 
        "Application":
            "Food Waste Prediction Platform",
 
        "Status":
            "Running",
 
        "Version":
            "1.0",
 
        "Endpoints": [
 
            "/health",
            "/predict"
 
        ]
 
    })
 
 

# HEALTH CHECK

 
@app.route("/health")
def health():
 
    return jsonify({
 
        "API Status":
            "Healthy",
 
        "Demand Model":
            "Loaded",
 
        "Waste Model":
            "Loaded",
 
        "Encoders":
            "Loaded"
 
    })
 
 

# PREDICTION API

 
@app.route(
    "/predict",
    methods=["POST"]
)
def predict():
 
    try:
 
        data = request.json
 
        
        # INPUT PARAMETERS
        
 
        meal_type = data["Meal_Type"]
 
        food_item = data["Food_Item"]
 
        quantity_prepared = float(
            data["Quantity_Prepared"]
        )
 
        temperature = float(
            data["Temperature"]
        )
 
        rainfall = float(
            data["Rainfall"]
        )
 
        holiday_flag = int(
            data["Holiday_Flag"]
        )
 
        event_flag = int(
            data["Event_Flag"]
        )
 
        previous_day_sales = float(
            data["Previous_Day_Sales"]
        )
 
        previous_day_waste = float(
            data["Previous_Day_Waste"]
        )
 
        day = int(
            data["Day"]
        )
 
        month = int(
            data["Month"]
        )
 
        weekday = int(
            data["Weekday"]
        )
 
        unit_cost = float(
            data["Unit_Cost"]
        )
 
        
        # ENCODING
        
 
        meal_encoded = (
 
            meal_encoder.transform(
                [meal_type]
            )[0]
 
        )
 
        food_encoded = (
 
            food_encoder.transform(
                [food_item]
            )[0]
 
        )
 
        weekend_flag = (
 
            1 if weekday >= 5
 
            else 0
 
        )
 
        
        # DEMAND MODEL FEATURES
        
 
        demand_input = pd.DataFrame({
 
            "Meal_Type":
                [meal_encoded],
 
            "Food_Item":
                [food_encoded],
 
            "Temperature":
                [temperature],
 
            "Rainfall":
                [rainfall],
 
            "Holiday_Flag":
                [holiday_flag],
 
            "Event_Flag":
                [event_flag],
 
            "Previous_Day_Sales":
                [previous_day_sales],
 
            "Previous_Day_Waste":
                [previous_day_waste],
 
            "Day":
                [day],
 
            "Month":
                [month],
 
            "Weekday":
                [weekday],
 
            "Weekend_Flag":
                [weekend_flag]
 
        })
 
        
        # WASTE MODEL FEATURES
        
 
        waste_input = pd.DataFrame({
 
            "Meal_Type":
                [meal_encoded],
 
            "Food_Item":
                [food_encoded],
 
            "Quantity_Prepared":
                [quantity_prepared],
 
            "Temperature":
                [temperature],
 
            "Rainfall":
                [rainfall],
 
            "Holiday_Flag":
                [holiday_flag],
 
            "Event_Flag":
                [event_flag],
 
            "Previous_Day_Sales":
                [previous_day_sales],
 
            "Previous_Day_Waste":
                [previous_day_waste],
 
            "Day":
                [day],
 
            "Month":
                [month],
 
            "Weekday":
                [weekday],
 
            "Weekend_Flag":
                [weekend_flag]
 
        })
 
        
        # MODEL PREDICTIONS
        
 
        predicted_demand = float(
 
            demand_model.predict(
                demand_input
            )[0]
 
        )
 
        predicted_waste = float(
 
            waste_model.predict(
                waste_input
            )[0]
 
        )
 
        
        # INVENTORY OPTIMIZATION
        
 
        report = optimizer.generate_report(
 
            predicted_demand=
            predicted_demand,
 
            predicted_waste=
            predicted_waste,
 
            unit_cost=
            unit_cost
 
        )
 
        
        # RESPONSE
        
 
        response = {
 
            "Predicted_Demand":
 
                round(
                    report["Predicted_Demand"],
                    2
                ),
 
            "Predicted_Waste":
 
                round(
                    report["Predicted_Waste"],
                    2
                ),
 
            "Recommended_Inventory":
 
                report[
                    "Recommended_Inventory"
                ],
 
            "Safety_Stock":
 
                report[
                    "Safety_Stock"
                ],
 
            "Waste_Percentage":
 
                report[
                    "Waste_Percentage"
                ],
 
            "Estimated_Cost_Loss":
 
                report[
                    "Estimated_Cost_Loss"
                ],
 
            "Waste_Adjustment":
 
                report[
                    "Waste_Adjustment"
                ],
 
            "Procurement_Needed":
 
                report[
                    "Procurement_Needed"
                ],
 
            "Preparation_Reduction_Percent":
 
                report[
                    "Preparation_Reduction_Percent"
                ],
 
            "Potential_Waste_Saving_Units":
 
                report[
                    "Potential_Waste_Saving_Units"
                ],
 
            "Potential_Cost_Saving":
 
                report[
                    "Potential_Cost_Saving"
                ],
 
            "Risk_Level":
 
                report[
                    "Risk_Level"
                ],
 
            "Recommendation":
 
                report[
                    "Recommendation"
                ]
 
        }
 
        return jsonify(response)
 
    except Exception as e:
 
        return jsonify({
 
            "Status": "Error",
 
            "Message": str(e)
 
        }), 500
 
 

# RUN APPLICATION

 
if __name__ == "__main__":
 
    app.run(
 
        host="0.0.0.0",
 
        port=5000,
 
        debug=True
 
    )