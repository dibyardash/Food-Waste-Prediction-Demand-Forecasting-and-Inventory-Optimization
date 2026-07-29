import streamlit as st
import pandas as pd
import joblib

from streamlit_option_menu import option_menu 
from inventory_optimizer import InventoryOptimizer
 

# PAGE CONFIG

 
st.set_page_config(
    page_title="FoodOptima Platform",
    page_icon="🍽️",
    layout="wide"
)
 

# CUSTOM CSS

 
st.markdown("""
<style>
 
.main{
    background-color:#f4f6f9;
}
 
/* Banner */
 
.banner{
    background:linear-gradient(
        90deg,
        #11998e,
        #38ef7d
    );
 
    padding:35px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
}
 
/* Page Transition Animation */
 
.main .block-container{
 
    animation: slideIn 0.45s ease-in-out;
}
 
@keyframes slideIn{
 
    from{
        opacity:0;
        transform:translateX(40px);
    }
 
    to{
        opacity:1;
        transform:translateX(0px);
    }
}
 
/* Cards */
 
div[data-testid="metric-container"]{
 
    background:white;
 
    border-radius:15px;
 
    padding:15px;
 
    box-shadow:
    0px 4px 12px rgba(0,0,0,0.10);
}
 
/* Buttons */
 
button{
 
    transition:all 0.3s ease;
}
 
button:hover{
 
    transform:translateY(-3px);
}
 
/* Tabs */
 
.stTabs [data-baseweb="tab-list"]{
 
    gap:10px;
}
 
.stTabs [data-baseweb="tab"]{
 
    border-radius:10px;
}
 
</style>
""", unsafe_allow_html=True)
 

# HEADER

 
st.markdown("""
<div class="banner">
 
<h1>🍽️ FoodOptima Platform</h1>
 
<p>
AI Driven Demand Forecasting,
Waste Prediction and Inventory Optimization
</p>
 
</div>
""", unsafe_allow_html=True)
 

# LOAD MODELS

 
@st.cache_resource
def load_models():
 
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
 
    return (
        demand_model,
        waste_model,
        meal_encoder,
        food_encoder
    )
 
(
    demand_model,
    waste_model,
    meal_encoder,
    food_encoder
) = load_models()
 
optimizer = InventoryOptimizer()
 

# NAVIGATION

 
selected = option_menu(
 
    menu_title=None,
 
    options=[
        "Home",
        "Predictor",
        "Analytics",
        "About"
    ],
 
    icons=[
        "house-fill",
        "graph-up-arrow",
        "bar-chart-fill",
        "info-circle-fill"
    ],
 
    default_index=0,
 
    orientation="horizontal",
 
    styles={
 
        "container": {
 
            "padding": "5px",
 
            "background-color": "#ffffff",
 
            "border-radius": "15px",
 
            "box-shadow":
            "0px 2px 12px rgba(0,0,0,0.08)"
        },
 
        "icon": {
 
            "color": "#11998e",
 
            "font-size": "18px"
        },
 
        "nav-link": {
 
            "font-size": "16px",
 
            "font-weight": "600",
 
            "text-align": "center",
 
            "margin": "0px",
 
            "--hover-color": "#e8fff5",
 
            "border-radius": "10px"
        },
 
        "nav-link-selected": {
 
            "background":
            "linear-gradient(90deg,#11998e,#38ef7d)",
 
            "color": "white",
 
            "border-radius": "10px"
        }
    }
)
 

# HOME

 
if selected == "Home":
 
    st.title(
        "Smart Food Waste Management System"
    )
 
    st.write("""
This platform helps restaurants,
canteens and cafeterias to:
 
✅ Forecast Food Demand
 
✅ Predict Food Waste
 
✅ Optimize Inventory
 
✅ Reduce Operational Cost
 
✅ Improve Sustainability
 
✅ Make AI Driven Decisions
""")
 
    c1,c2,c3,c4 = st.columns(4)
 
    c1.metric(
        "Models",
        "2"
    )
 
    c2.metric(
        "Waste Reduction",
        "30%"
    )
 
    c3.metric(
        "Safety Stock",
        "10%"
    )
 
    c4.metric(
        "Optimization",
        "AI Powered"
    )
 

# PREDICTION PAGE

 
elif selected == "Predictor":
 
    st.title("Prediction Center")
 
    prediction_tab, inventory_tab, recommendation_tab = st.tabs(
 
        [
            "🎯 Prediction",
            "📦 Inventory Report",
            "🤖 Recommendation"
        ]
 
    )
 
    with prediction_tab:
 
        col1,col2 = st.columns(2)
 
        with col1:
 
            meal_type = st.selectbox(
                "Meal Type",
                list(
                    meal_encoder.classes_
                )
            )
 
            food_item = st.selectbox(
                "Food Item",
                list(
                    food_encoder.classes_
                )
            )
 
            quantity_prepared = st.number_input(
                "Quantity Prepared",
                min_value=50,
                max_value=10000,
                value=500
            )
 
            previous_day_sales = st.number_input(
                "Previous Day Sales",
                min_value=0,
                value=350
            )
 
        with col2:
 
            temperature = st.number_input(
                "Temperature (°C)",
                0.0,
                50.0,
                28.0
            )
 
            rainfall = st.number_input(
                "Rainfall (mm)",
                0.0,
                300.0,
                15.0
            )
 
            previous_day_waste = st.number_input(
                "Previous Day Waste",
                min_value=0,
                value=40
            )
 
            unit_cost = st.number_input(
                "Unit Cost (₹)",
                min_value=1,
                value=20
            )
 
        st.markdown("---")
 
        c1,c2 = st.columns(2)
 
        holiday_flag = c1.selectbox(
            "Holiday Flag",
            [0,1]
        )
 
        event_flag = c2.selectbox(
            "Event Flag",
            [0,1]
        )
 
        selected_date = st.date_input(
            "Select Date"
        )
 
        predict_button = st.button(
            "🚀 Generate Prediction"
        )
 
    if predict_button:
 
        day = selected_date.day
        month = selected_date.month
        weekday = selected_date.weekday()
 
        weekend_flag = (
            1 if weekday >= 5 else 0
        )
 
        meal_encoded = meal_encoder.transform(
            [meal_type]
        )[0]
 
        food_encoded = food_encoder.transform(
            [food_item]
        )[0]
 
        demand_input = pd.DataFrame({
 
            "Meal_Type":[meal_encoded],
            "Food_Item":[food_encoded],
            "Temperature":[temperature],
            "Rainfall":[rainfall],
            "Holiday_Flag":[holiday_flag],
            "Event_Flag":[event_flag],
            "Previous_Day_Sales":[previous_day_sales],
            "Previous_Day_Waste":[previous_day_waste],
            "Day":[day],
            "Month":[month],
            "Weekday":[weekday],
            "Weekend_Flag":[weekend_flag]
 
        })
 
        waste_input = pd.DataFrame({
 
            "Meal_Type":[meal_encoded],
            "Food_Item":[food_encoded],
            "Quantity_Prepared":[quantity_prepared],
            "Temperature":[temperature],
            "Rainfall":[rainfall],
            "Holiday_Flag":[holiday_flag],
            "Event_Flag":[event_flag],
            "Previous_Day_Sales":[previous_day_sales],
            "Previous_Day_Waste":[previous_day_waste],
            "Day":[day],
            "Month":[month],
            "Weekday":[weekday],
            "Weekend_Flag":[weekend_flag]
 
        })
 
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
 
        report = optimizer.generate_report(
 
            predicted_demand,
            predicted_waste,
            unit_cost
 
        )
 
        
        # SUMMARY
        
 
        with prediction_tab:
 
            st.success(
                "Prediction Generated Successfully"
            )
 
            m1,m2,m3,m4,m5,m6 = st.columns(6)
 
            m1.metric(
                "Demand",
                f"{report['Predicted_Demand']:.0f}"
            )
 
            m2.metric(
                "Waste",
                f"{report['Predicted_Waste']:.0f}"
            )
 
            m3.metric(
                "Inventory",
                report["Recommended_Inventory"]
            )
 
            m4.metric(
                "Safety Stock",
                report["Safety_Stock"]
            )
 
            m5.metric(
                "Reduce Prep",
                f"{report['Preparation_Reduction_Percent']}%"
            )
 
            m6.metric(
                "Risk",
                report["Risk_Level"]
            )
 
        
        # INVENTORY REPORT
        
 
        with inventory_tab:
 
            st.subheader(
                "📦 Smart Inventory Optimization Report"
            )
 
            r1c1,r1c2,r1c3 = st.columns(3)
 
            r1c1.metric(
                "Recommended Inventory",
                report["Recommended_Inventory"]
            )
 
            r1c2.metric(
                "Procurement Needed",
                report["Procurement_Needed"]
            )
 
            r1c3.metric(
                "Waste Adjustment",
                report["Waste_Adjustment"]
            )
 
            r2c1,r2c2,r2c3 = st.columns(3)
 
            r2c1.metric(
                "Waste %",
                f"{report['Waste_Percentage']:.2f}%"
            )
 
            r2c2.metric(
                "Waste Saving",
                report["Potential_Waste_Saving_Units"]
            )
 
            r2c3.metric(
                "Cost Saving",
                f"₹{report['Potential_Cost_Saving']:.2f}"
            )
 
            st.markdown("---")
 
            st.success(f"""
✅ Predicted Demand: {report['Predicted_Demand']:.0f}
 
✅ Predicted Waste: {report['Predicted_Waste']:.0f}
 
✅ Recommended Inventory: {report['Recommended_Inventory']}
 
✅ Reduce Preparation By: {report['Preparation_Reduction_Percent']}%
 
✅ Cost Saving Potential: ₹{report['Potential_Cost_Saving']:.2f}
""")
 
        
        # RECOMMENDATION
        
 
        with recommendation_tab:
 
            st.subheader(
                "🤖 AI Recommendation"
            )
 
            if report["Risk_Level"] == "HIGH":
 
                st.error(
                    report["Recommendation"]
                )
 
            elif report["Risk_Level"] == "MEDIUM":
 
                st.warning(
                    report["Recommendation"]
                )
 
            else:
 
                st.success(
                    report["Recommendation"]
                )
 
            st.markdown("---")
 
            st.subheader(
                "📋 Today's Action Plan"
            )
 
            st.write(f"""
**Prepare:** {report['Recommended_Inventory']} units
 
**Expected Demand:** {report['Predicted_Demand']:.0f} units
 
**Expected Waste:** {report['Predicted_Waste']:.0f} units
 
**Reduction Required:** {report['Preparation_Reduction_Percent']}%
 
**Potential Waste Saving:** {report['Potential_Waste_Saving_Units']} units
 
**Potential Cost Saving:** ₹{report['Potential_Cost_Saving']:.2f}
""")
 

# ANALYTICS

 
elif selected == "Analytics":
 
    st.title("Analytics Dashboard")
 
    c1,c2,c3,c4 = st.columns(4)
 
    c1.metric(
        "Forecast Accuracy",
        "92%"
    )
 
    c2.metric(
        "Waste Reduction Goal",
        "30%"
    )
 
    c3.metric(
        "Potential Saving",
        "₹25,000+"
    )
 
    c4.metric(
        "Inventory Efficiency",
        "High"
    )
 
    st.info("""
🍛 Lunch generally has the highest demand.
 
🍚 Rice and Biryani often contribute the highest waste.
 
🌧 High rainfall may reduce demand.
 
📈 Historical sales improve prediction accuracy.
 
♻ Better inventory planning reduces food waste.
 
💰 Lower waste improves profitability.
""")
 

# ABOUT

 
elif selected == "About":
 
    st.title("About Project")
 
    st.markdown("""
## FoodOptima Platform
 
### Models
 
- XGBoost Demand Prediction
- Random Forest Waste Prediction
- Smart Inventory Optimizer
 
### Features
 
- Demand Forecasting
- Waste Prediction
- Inventory Recommendation
- Safety Stock Calculation
- Waste Reduction Strategy
- Cost Saving Estimation
 
### Technologies
 
- Python
- Pandas
- Scikit-Learn
- XGBoost
- Random Forest
- Streamlit
- Flask API
- Joblib
 
### Benefits
 
- Reduce Food Waste
- Improve Planning
- Save Cost
- Increase Sustainability
- AI-Powered Decision Making
""")