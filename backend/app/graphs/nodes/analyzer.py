"""
Analytics and KPI calculation nodes
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from backend.app.graphs.state import WorkflowState, AnalyticsState
from backend.app.core.logging import get_logger
from backend.app.graphs.hooks import apply_pre_hooks, apply_post_hooks

logger = get_logger(__name__)


async def analyze_sales_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Analyze sales data and calculate metrics
    Node with caching enabled
    """
    logger.info("Starting sales analysis", user_id=state["user_id"])
    
    try:
        # Extract parameters
        product_codes = state.get("product_codes", [])
        client_ids = state.get("client_ids", [])
        period = state.get("period", {})
        
        # TODO: Implement actual database queries
        # This is a mock implementation
        
        # Calculate mock metrics
        total_revenue = 150000000  # 150M KRW
        total_quantity = 1500
        num_clients = len(client_ids) if client_ids else 25
        
        # Mock sales by client
        sales_by_client = []
        if client_ids:
            for client_id in client_ids[:5]:  # Top 5 clients
                sales_by_client.append({
                    "client_id": client_id,
                    "client_name": f"Client {client_id}",
                    "revenue": total_revenue / 5,
                    "quantity": total_quantity / 5,
                    "growth_rate": 0.15
                })
        
        # Mock sales by product
        sales_by_product = []
        for product_code in product_codes[:3]:  # Top 3 products
            sales_by_product.append({
                "product_code": product_code,
                "product_name": f"Product {product_code}",
                "revenue": total_revenue / 3,
                "quantity": total_quantity / 3,
                "market_share": 0.25
            })
        
        # Create analysis result
        analysis = {
            "kpi_summary": {
                "total_revenue": total_revenue,
                "total_quantity": total_quantity,
                "num_clients": num_clients,
                "avg_deal_size": total_revenue / num_clients if num_clients > 0 else 0,
                "period": period
            },
            "sales_by_client": sales_by_client,
            "sales_by_product": sales_by_product,
            "trends": {
                "revenue_trend": "increasing",
                "growth_areas": ["hospital", "clinic"],
                "declining_areas": ["pharmacy"]
            }
        }
        
        # Apply post-hooks
        analysis = await apply_post_hooks("analyze_sales", analysis, state)
        
        logger.info("Sales analysis completed", metrics=analysis["kpi_summary"])
        
        return {
            "analysis": analysis,
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": f"Sales analysis completed. Total revenue: {total_revenue:,} KRW"
            }]
        }
        
    except Exception as e:
        logger.error(f"Error in sales analysis: {str(e)}", exc_info=True)
        return {
            "errors": state.get("errors", []) + [{
                "node": "analyze_sales",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }]
        }


async def calculate_kpi_node(state: AnalyticsState) -> Dict[str, Any]:
    """
    Calculate detailed KPIs including YoY, YTD, achievement rates
    """
    logger.info("Calculating KPIs")
    
    try:
        # Extract current period data
        period = state.get("period", {})
        current_year = int(period.get("end", "202412")[:4])
        current_month = int(period.get("end", "202412")[4:6])
        
        # TODO: Implement actual KPI calculations with database
        # Mock calculations
        
        # Year-over-Year (YoY) growth
        current_revenue = 150000000
        previous_year_revenue = 130000000
        yoy_growth = ((current_revenue - previous_year_revenue) / previous_year_revenue) * 100
        
        # Year-to-Date (YTD) achievement
        ytd_revenue = current_revenue * (current_month / 12)
        ytd_target = 200000000 * (current_month / 12)
        ytd_achievement = (ytd_revenue / ytd_target) * 100 if ytd_target > 0 else 0
        
        # Monthly target achievement
        monthly_target = 20000000
        monthly_revenue = current_revenue / current_month
        target_achievement_rate = (monthly_revenue / monthly_target) * 100
        
        # Detailed KPI results
        kpi_details = {
            "yoy_growth": round(yoy_growth, 2),
            "ytd_achievement": round(ytd_achievement, 2),
            "target_achievement_rate": round(target_achievement_rate, 2),
            "metrics": {
                "current_revenue": current_revenue,
                "ytd_revenue": ytd_revenue,
                "ytd_target": ytd_target,
                "monthly_avg": monthly_revenue,
                "quarterly_performance": {
                    "Q1": current_revenue * 0.2,
                    "Q2": current_revenue * 0.25,
                    "Q3": current_revenue * 0.3,
                    "Q4": current_revenue * 0.25
                }
            },
            "insights": {
                "performance_status": "on_track" if target_achievement_rate >= 90 else "below_target",
                "growth_status": "positive" if yoy_growth > 0 else "negative",
                "recommendations": []
            }
        }
        
        # Add recommendations based on performance
        if target_achievement_rate < 80:
            kpi_details["insights"]["recommendations"].append(
                "Consider intensifying sales efforts in high-potential clients"
            )
        if yoy_growth < 10:
            kpi_details["insights"]["recommendations"].append(
                "Focus on new product launches and market expansion"
            )
        
        logger.info(
            "KPI calculation completed",
            yoy=yoy_growth,
            ytd=ytd_achievement,
            target_rate=target_achievement_rate
        )
        
        return {
            **state,
            "yoy_growth": yoy_growth,
            "ytd_achievement": ytd_achievement,
            "target_achievement_rate": target_achievement_rate,
            "kpi_summary": {
                **state.get("kpi_summary", {}),
                **kpi_details
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating KPIs: {str(e)}", exc_info=True)
        return state