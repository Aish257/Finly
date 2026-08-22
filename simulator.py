import plotly.graph_objects as go
import plotly.express as px

SCENARIOS = {
    "Market Rises (Bull Run 🐂)": {
        "description": "Strong economic growth, corporate earnings surge, and investor optimism drive markets higher.",
        "returns": {"Stocks": 0.20, "Mutual Funds": 0.13, "Gold": 0.05, "Cash": 0.00},
        "explanation": "During a Bull Run, high-risk assets like individual stocks and equity mutual funds outperform significantly. Gold provides steady modest gains, while cash yields no capital growth."
    },
    "Market Falls (Bear Crash 🐻)": {
        "description": "Economic recession fears or unexpected global shocks lead to sharp sell-offs.",
        "returns": {"Stocks": -0.22, "Mutual Funds": -0.14, "Gold": 0.10, "Cash": 0.00},
        "explanation": "Equities decline significantly in a bear crash. However, holding Gold and Cash buffers your portfolio loss because investors flee to safe-haven assets during panic."
    },
    "High Volatility (Turbulent ⚡)": {
        "description": "Rapid market swings driven by inflation reports, interest rate changes, and geopolitical uncertainty.",
        "returns": {"Stocks": -0.10, "Mutual Funds": 0.06, "Gold": 0.15, "Cash": 0.00},
        "explanation": "Volatile markets reward diversified assets. While individual stock picking faces whipsaws, Gold and balanced Mutual Funds protect total portfolio capital."
    },
    "Stable Market (Sideways 🌊)": {
        "description": "The economy grows steadily at a predictable pace with minimal surprises.",
        "returns": {"Stocks": 0.07, "Mutual Funds": 0.08, "Gold": 0.04, "Cash": 0.015},
        "explanation": "In a sideways or stable market, returns are positive across all categories with low stress and low price fluctuations."
    }
}

def calculate_simulation(allocations, scenario_name, initial_capital=10000.0):
    """
    allocations: dict like {'Stocks': 40, 'Mutual Funds': 30, 'Gold': 20, 'Cash': 10} (percentages)
    """
    scenario = SCENARIOS[scenario_name]
    returns = scenario["returns"]
    
    results = {}
    total_final = 0.0
    
    for asset, percent in allocations.items():
        initial_val = (percent / 100.0) * initial_capital
        rate = returns.get(asset, 0.0)
        final_val = initial_val * (1.0 + rate)
        profit_loss = final_val - initial_val
        
        results[asset] = {
            "initial": initial_val,
            "final": final_val,
            "change": profit_loss,
            "rate_pct": rate * 100
        }
        total_final += final_val
        
    net_pl = total_final - initial_capital
    net_pl_pct = (net_pl / initial_capital) * 100.0
    
    return {
        "initial_capital": initial_capital,
        "total_final": total_final,
        "net_pl": net_pl,
        "net_pl_pct": net_pl_pct,
        "asset_results": results,
        "scenario_info": scenario
    }

def create_simulation_chart(sim_result):
    categories = list(sim_result["asset_results"].keys())
    initial_vals = [sim_result["asset_results"][c]["initial"] for c in categories]
    final_vals = [sim_result["asset_results"][c]["final"] for c in categories]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=initial_vals,
        name='Initial Allocation (₹)',
        marker_color='#FF7A00'
    ))
    fig.add_trace(go.Bar(
        x=categories,
        y=final_vals,
        name='Simulated Outcome (₹)',
        marker_color='#FF9800' if sim_result['net_pl'] >= 0 else '#EF4444'
    ))
    
    fig.update_layout(
        barmode='group',
        title=dict(text="Portfolio Before vs After Simulation", font=dict(color='#FFFFFF', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#A1A1AA'),
        legend=dict(font=dict(color='#FFFFFF')),
        xaxis=dict(gridcolor='#1F222C'),
        yaxis=dict(gridcolor='#1F222C', title="Amount (₹)")
    )
    return fig
