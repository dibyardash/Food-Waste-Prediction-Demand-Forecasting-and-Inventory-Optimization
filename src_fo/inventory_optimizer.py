class InventoryOptimizer:
 
    def generate_report(
        self,
        predicted_demand,
        predicted_waste,
        unit_cost
    ):
 
        
        # SAFETY STOCK
        
 
        safety_stock = predicted_demand * 0.10
 
        
        # WASTE PERCENTAGE
        
 
        waste_percentage = (predicted_waste / max(predicted_demand, 1)) * 100

        # Dynamic reduction percentage
        
        preparation_reduction = min(round(waste_percentage), 20)
 
        
        # INVENTORY ADJUSTMENT
        
 
        waste_adjustment = predicted_waste
 
        recommended_inventory = (predicted_demand + safety_stock - waste_adjustment)
 
        recommended_inventory = max(recommended_inventory, predicted_demand)
 
        
        # COST LOSS
        
 
        estimated_cost_loss = (predicted_waste * unit_cost)
 
        
        # PROCUREMENT NEED
        
 
        procurement_needed = (recommended_inventory - predicted_demand)
 
        
        # RISK CLASSIFICATION
        
 
        if waste_percentage >= 20:
 
            risk = "HIGH"
 
            recommendation = f"""
⚠️ HIGH WASTE RISK
 
Expected Waste:
{predicted_waste:.0f} units
 
Recommended Actions:
 
• Reduce preparation by 15%
 
• Prepare approximately {recommended_inventory:.0f} units
 
• Avoid overstocking
 
• Monitor high-waste menu items closely
 
• Review purchasing quantities
"""
 
        elif waste_percentage >= 10:
 
            risk = "MEDIUM"
 
            recommendation = f"""
⚠️ MODERATE WASTE RISK
 
Expected Waste:
{predicted_waste:.0f} units
 
Recommended Actions:
 
• Reduce preparation by 8%
 
• Prepare approximately {recommended_inventory:.0f} units
 
• Monitor inventory carefully
 
• Track demand fluctuations
"""
 
        else:
 
            risk = "LOW"
 
            recommendation = f"""
✅ LOW WASTE RISK
 
Expected Waste:
{predicted_waste:.0f} units
 
Recommended Actions:
 
• Maintain current preparation levels
 
• Prepare approximately {recommended_inventory:.0f} units
 
• Continue existing inventory strategy
"""
 
        
        # WASTE SAVING POTENTIAL
        
 
        waste_saving_units = predicted_waste
 
        waste_saving_cost = (waste_saving_units * unit_cost)
 
        
        # RETURN REPORT
        
 
        return {
 
            "Predicted_Demand":
 
                round(predicted_demand),
 
            "Predicted_Waste":
 
                round(predicted_waste),
 
            "Recommended_Inventory":
 
                round(recommended_inventory),
 
            "Safety_Stock":
 
                round(safety_stock),
 
            "Waste_Percentage":
 
                round(waste_percentage, 2),
 
            "Estimated_Cost_Loss":
 
                round(estimated_cost_loss, 2),
 
            "Waste_Adjustment":
 
                round(waste_adjustment),
 
            "Procurement_Needed":
 
                round(procurement_needed),
 
            "Preparation_Reduction_Percent":
 
                preparation_reduction,
 
            "Potential_Waste_Saving_Units":
 
                round(waste_saving_units),
 
            "Potential_Cost_Saving":
 
                round(
                    waste_saving_cost,
                    2
                ),
 
            "Risk_Level":
 
                risk,
 
            "Recommendation":
 
                recommendation
 
        }