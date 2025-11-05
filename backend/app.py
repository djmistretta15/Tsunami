"""
Tech Momentum Arbitrage Engine - API Backend
Flask REST API to serve engine data to frontend
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine import TechMomentumArbitrageEngine
from datetime import datetime

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

# Initialize engine
engine = TechMomentumArbitrageEngine()

# Load data
companies = engine.load_companies_from_json("/home/user/Tsunami/data/companies.json")
market_conditions = {
    "ipo_window": "open",
    "volatility": "medium",
    "interest_rates": "neutral",
}

# Generate report (cache it)
report = engine.generate_weekly_report(companies, market_conditions)


@app.route('/api/summary')
def get_summary():
    """Get executive summary"""
    return jsonify({
        "report_date": report.report_date.isoformat(),
        "signals_generated": report.signals_generated,
        "high_conviction_count": report.high_conviction_count,
        "average_momentum_score": report.average_momentum_score,
        "ipo_window_health": report.ipo_window_health,
        "macro_conditions": report.macro_conditions,
    })


@app.route('/api/signals')
def get_signals():
    """Get top 10 trade signals"""
    signals = []
    for s in report.top_10_momentum_plays:
        signals.append({
            "rank": s.rank,
            "company": s.company,
            "company_id": s.company_id,
            "sector": s.sector.value,
            "momentum_score": s.momentum_score,
            "momentum_change_7d": s.momentum_change_7d,
            "hype_score": s.hype_score,
            "build_score": s.build_score,
            "moat_score": s.moat_score,
            "recommendation": s.recommendation.value,
            "conviction": s.conviction,
            "position_size": s.position_size,
            "public_proxy": s.public_proxy,
            "pre_ipo_access": s.pre_ipo_access,
            "entry_timing": s.entry_timing,
            "next_catalyst": s.next_catalyst,
            "catalyst_date": s.catalyst_date.isoformat() if s.catalyst_date else None,
            "expected_return": s.expected_return,
            "time_horizon": s.time_horizon,
            "risk_factors": s.risk_factors,
        })
    return jsonify(signals)


@app.route('/api/bottlenecks')
def get_bottlenecks():
    """Get emerging bottlenecks"""
    bottlenecks = []
    for b in report.emerging_bottlenecks:
        bottlenecks.append({
            "bottleneck_name": b.bottleneck_name,
            "description": b.description,
            "confidence": b.confidence,
            "evidence": b.evidence,
            "private_companies": b.private_companies,
            "public_proxies": b.public_proxies,
            "sector": b.sector.value,
            "priority": b.priority,
            "estimated_market_size": b.estimated_market_size,
        })
    return jsonify(bottlenecks)


@app.route('/api/companies')
def get_companies():
    """Get all companies"""
    companies_data = []
    for c in companies:
        companies_data.append({
            "company_id": c.company_id,
            "name": c.name,
            "sector": c.sector.value,
            "wave_category": c.wave_category.value,
            "bottleneck_solved": c.bottleneck_solved,
            "total_funding": c.total_funding,
            "last_valuation": c.last_valuation,
            "fortune_500_customers": c.fortune_500_customers,
            "estimated_arr": c.estimated_arr,
            "ipo_probability_12mo": c.ipo_probability_12mo,
            "employee_count": c.employee_count,
            "website": c.website,
        })
    return jsonify(companies_data)


@app.route('/api/heatmap')
def get_heatmap():
    """Get momentum heatmap data"""
    # Group by sector
    from collections import defaultdict
    sectors = defaultdict(list)

    # Get momentum scores for all companies
    momentum_engine = engine.momentum_engine
    all_momentum = momentum_engine.score_companies(companies)

    for i, company in enumerate(companies):
        momentum = all_momentum[i]
        sectors[company.sector.value].append({
            "company": company.name,
            "momentum_score": momentum.momentum_score,
            "hype_score": momentum.hype_score,
            "build_score": momentum.build_score,
            "divergence_flag": momentum.divergence_flag.value,
        })

    return jsonify(dict(sectors))


@app.route('/api/backtest')
def get_backtest():
    """Get backtest results"""
    from src.modules.backtesting import BacktestEngine
    backtest_engine = BacktestEngine()
    result = backtest_engine.run_backtest()

    return jsonify({
        "start_date": result.start_date.isoformat(),
        "end_date": result.end_date.isoformat(),
        "total_return": result.total_return,
        "sharpe_ratio": result.sharpe_ratio,
        "max_drawdown": result.max_drawdown,
        "alpha_vs_qqq": result.alpha_vs_qqq,
        "win_rate": result.win_rate,
        "best_signals": result.best_signals,
        "worst_signals": result.worst_signals,
    })


# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
