"""
Tech Momentum Arbitrage Engine - Main Orchestration System
Coordinates all modules to generate weekly intelligence reports
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple
from pathlib import Path

from src.core.schemas import Company, WeeklyAlphaReport, BacktestResult
from src.core.config import Config
from src.modules.momentum_scoring import MomentumScoringEngine
from src.modules.moat_scoring import MoatScoringEngine
from src.modules.bottleneck_discovery import BottleneckDiscoveryAgent, generate_nov_2025_bottlenecks
from src.modules.timing_prediction import TimingPredictionEngine
from src.modules.second_order_arbitrage import SecondOrderArbitrageEngine, generate_mock_correlations
from src.modules.trade_signals import TradeSignalGenerator


class TechMomentumArbitrageEngine:
    """
    Main orchestration system for Tech Momentum Arbitrage Engine

    Coordinates:
    - Data ingestion and normalization
    - Momentum scoring (Hype + Build)
    - Moat analysis
    - Bottleneck discovery
    - Timing prediction
    - Second-order arbitrage
    - Trade signal generation
    """

    def __init__(self, config: Config = Config()):
        self.config = config

        # Initialize all engines
        self.momentum_engine = MomentumScoringEngine(config)
        self.moat_engine = MoatScoringEngine(config)
        self.bottleneck_agent = BottleneckDiscoveryAgent(config)
        self.timing_engine = TimingPredictionEngine(config)
        self.second_order_engine = SecondOrderArbitrageEngine(config)
        self.signal_generator = TradeSignalGenerator(config)

        # Data
        self.companies: List[Company] = []

    def load_companies_from_json(self, filepath: str) -> List[Company]:
        """Load companies from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        companies = []
        for c in data:
            # Reconstruct Company object
            from src.core.schemas import (
                Sector, WaveCategory, FundingRound,
                PatentGrant, ExecutiveHire, PublicProxy
            )
            from datetime import datetime

            company = Company(
                company_id=c['company_id'],
                name=c['name'],
                sector=Sector(c['sector']),
                wave_category=WaveCategory(c['wave_category']),
                bottleneck_solved=c['bottleneck_solved'],
                funding_rounds=[
                    FundingRound(
                        date=datetime.fromisoformat(r['date']),
                        amount=r['amount'],
                        lead_investor=r['lead_investor'],
                        valuation=r['valuation'],
                        round_type=r['round_type'],
                    ) for r in c['funding_rounds']
                ],
                total_funding=c['total_funding'],
                last_valuation=c['last_valuation'],
                patent_grants=[
                    PatentGrant(
                        grant_date=datetime.fromisoformat(p['grant_date']),
                        patent_id=p['patent_id'],
                        title=p['title'],
                        citation_count=p['citation_count'],
                        technology_cluster=p['technology_cluster'],
                    ) for p in c['patent_grants']
                ],
                patent_count=c['patent_count'],
                executive_hires=[
                    ExecutiveHire(
                        date=datetime.fromisoformat(e['date']),
                        role=e['role'],
                        name=e['name'],
                        previous_company=e['previous_company'],
                        is_ipo_signal=e['is_ipo_signal'],
                    ) for e in c['executive_hires']
                ],
                employee_count=c['employee_count'],
                engineer_pct=c['engineer_pct'],
                faang_talent_pct=c['faang_talent_pct'],
                public_proxies=[
                    PublicProxy(
                        ticker=p['ticker'],
                        exposure_type=p['exposure_type'],
                        correlation_score=p['correlation_score'],
                        revenue_exposure_pct=p.get('revenue_exposure_pct'),
                    ) for p in c['public_proxies']
                ],
                fortune_500_customers=c['fortune_500_customers'],
                estimated_arr=c['estimated_arr'],
                ipo_probability_6mo=c['ipo_probability_6mo'],
                ipo_probability_12mo=c['ipo_probability_12mo'],
                expected_ipo_date=datetime.fromisoformat(c['expected_ipo_date']) if c['expected_ipo_date'] else None,
                founded_date=datetime.fromisoformat(c['founded_date']),
                headquarters=c['headquarters'],
                website=c['website'],
            )
            companies.append(company)

        print(f"✅ Loaded {len(companies)} companies")
        return companies

    def generate_weekly_report(
        self,
        companies: List[Company],
        market_conditions: Dict = None,
    ) -> WeeklyAlphaReport:
        """
        Generate comprehensive weekly alpha report

        Args:
            companies: List of companies to analyze
            market_conditions: Current market conditions

        Returns:
            WeeklyAlphaReport with top signals and insights
        """
        market_conditions = market_conditions or {
            "ipo_window": "open",
            "volatility": "medium",
            "interest_rates": "neutral",
        }

        print("\n" + "="*80)
        print("TECH MOMENTUM ARBITRAGE ENGINE - WEEKLY ALPHA REPORT")
        print(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
        print("="*80 + "\n")

        # Step 1: Score momentum for all companies
        print("📊 Step 1: Calculating momentum scores...")
        momentum_scores = self.momentum_engine.score_companies(companies)
        print(f"   ✓ Scored {len(momentum_scores)} companies")

        # Step 2: Score moats
        print("🏰 Step 2: Analyzing competitive moats...")
        moat_scores = self.moat_engine.score_companies(companies)
        print(f"   ✓ Analyzed {len(moat_scores)} moats")

        # Step 3: Predict catalysts
        print("⏰ Step 3: Predicting timing catalysts...")
        catalysts = {}
        for company in companies:
            catalyst = self.timing_engine.get_next_catalyst(company, market_conditions)
            if catalyst:
                catalysts[company.company_id] = catalyst
        print(f"   ✓ Predicted {len(catalysts)} catalysts")

        # Step 4: Generate trade signals
        print("📈 Step 4: Generating trade signals...")
        signals = self.signal_generator.generate_signals(
            companies, momentum_scores, moat_scores, catalysts
        )
        print(f"   ✓ Generated {len(signals)} signals")

        # Step 5: Get top 10 signals
        top_10 = signals[:10]
        high_conviction = [s for s in signals if s.conviction >= 0.70]
        print(f"   ✓ Top 10 signals identified ({len(high_conviction)} high-conviction)")

        # Step 6: Discover bottlenecks
        print("🔍 Step 5: Discovering emerging bottlenecks...")
        emerging_bottlenecks = generate_nov_2025_bottlenecks()
        print(f"   ✓ Identified {len(emerging_bottlenecks)} bottlenecks")

        # Step 7: Find second-order plays
        print("🎯 Step 6: Finding second-order arbitrage plays...")
        correlations = generate_mock_correlations()
        second_order_plays = self.second_order_engine.find_second_order_plays(
            momentum_scores, correlations
        )
        top_second_order = second_order_plays[:10]
        print(f"   ✓ Found {len(second_order_plays)} plays ({len(top_second_order)} top picks)")

        # Calculate metrics
        avg_momentum = sum(s.momentum_score for s in momentum_scores) / len(momentum_scores)

        # Create report
        report = WeeklyAlphaReport(
            report_date=datetime.now(),
            top_10_momentum_plays=top_10,
            emerging_bottlenecks=emerging_bottlenecks,
            second_order_plays=top_second_order,
            portfolio_rebalance_actions=[],
            ipo_window_health=market_conditions["ipo_window"],
            macro_conditions=market_conditions,
            signals_generated=len(signals),
            high_conviction_count=len(high_conviction),
            average_momentum_score=avg_momentum,
        )

        print("\n✅ Weekly report generation complete!\n")
        return report

    def export_report_json(self, report: WeeklyAlphaReport, filepath: str):
        """Export report to JSON"""
        report_dict = {
            "report_date": report.report_date.isoformat(),
            "ipo_window_health": report.ipo_window_health,
            "macro_conditions": report.macro_conditions,
            "signals_generated": report.signals_generated,
            "high_conviction_count": report.high_conviction_count,
            "average_momentum_score": report.average_momentum_score,
            "top_10_momentum_plays": [
                {
                    "rank": s.rank,
                    "company": s.company,
                    "sector": s.sector.value,
                    "momentum_score": s.momentum_score,
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
                    "expected_return": s.expected_return,
                    "time_horizon": s.time_horizon,
                    "risk_factors": s.risk_factors,
                } for s in report.top_10_momentum_plays
            ],
            "emerging_bottlenecks": [
                {
                    "bottleneck_name": b.bottleneck_name,
                    "description": b.description,
                    "confidence": b.confidence,
                    "evidence": b.evidence,
                    "private_companies": b.private_companies,
                    "public_proxies": b.public_proxies,
                    "sector": b.sector.value,
                    "priority": b.priority,
                } for b in report.emerging_bottlenecks
            ],
            "second_order_plays": [
                {
                    "primary_technology": p.primary_technology,
                    "primary_momentum_score": p.primary_momentum_score,
                    "supplier_company": p.supplier_company,
                    "supplier_ticker": p.supplier_ticker,
                    "exposure_type": p.exposure_type,
                    "dependency_score": p.dependency_score,
                    "price_correlation": p.price_correlation,
                    "thesis": p.thesis,
                    "entry_timing": p.entry_timing,
                    "risk_adjusted_return": p.risk_adjusted_return,
                } for p in report.second_order_plays
            ],
        }

        with open(filepath, 'w') as f:
            json.dump(report_dict, f, indent=2)

        print(f"✅ Exported report to {filepath}")

    def export_report_markdown(self, report: WeeklyAlphaReport, filepath: str):
        """Export report as formatted markdown"""
        md = []

        md.append("# TECH MOMENTUM ARBITRAGE ENGINE")
        md.append(f"## Weekly Alpha Report - {report.report_date.strftime('%B %d, %Y')}")
        md.append("")
        md.append("---")
        md.append("")

        # Executive Summary
        md.append("## 📊 Executive Summary")
        md.append("")
        md.append(f"- **Signals Generated**: {report.signals_generated}")
        md.append(f"- **High Conviction Plays**: {report.high_conviction_count}")
        md.append(f"- **Average Momentum Score**: {report.average_momentum_score:.1f}/100")
        md.append(f"- **IPO Window**: {report.ipo_window_health.upper()}")
        md.append(f"- **Market Volatility**: {report.macro_conditions.get('volatility', 'N/A').upper()}")
        md.append("")
        md.append("---")
        md.append("")

        # Top 10 Plays
        md.append("## 🎯 TOP 10 MOMENTUM PLAYS")
        md.append("")

        for signal in report.top_10_momentum_plays:
            md.append(f"### {signal.rank}. {signal.company}")
            md.append(f"**Sector**: {signal.sector.value} | **Recommendation**: {signal.recommendation.value}")
            md.append("")
            md.append(f"**Momentum Metrics:**")
            md.append(f"- Overall Momentum: **{signal.momentum_score:.1f}/100**")
            md.append(f"- Hype Score (Narrative): {signal.hype_score:.1f}/100")
            md.append(f"- Build Score (Execution): {signal.build_score:.1f}/100")
            md.append(f"- Moat Score: {signal.moat_score:.1f}/100")
            md.append(f"- Conviction: **{signal.conviction:.0%}**")
            md.append("")
            md.append(f"**Investment Thesis:**")
            md.append(f"- Position Size: {signal.position_size}")
            md.append(f"- Entry Timing: {signal.entry_timing}")
            md.append(f"- Expected Return: {signal.expected_return}")
            md.append(f"- Time Horizon: {signal.time_horizon}")
            md.append("")
            md.append(f"**Exposure Routes:**")
            if signal.public_proxy:
                md.append(f"- Public Proxy: {signal.public_proxy}")
            if signal.pre_ipo_access:
                md.append(f"- Pre-IPO: {signal.pre_ipo_access}")
            md.append("")
            if signal.next_catalyst:
                md.append(f"**Next Catalyst:** {signal.next_catalyst}")
            md.append("")
            md.append(f"**Risk Factors:**")
            for risk in signal.risk_factors:
                md.append(f"- {risk}")
            md.append("")
            md.append("---")
            md.append("")

        # Emerging Bottlenecks
        md.append("## 🔍 EMERGING BOTTLENECKS (Wave 1 Opportunities)")
        md.append("")

        for bottleneck in report.emerging_bottlenecks:
            md.append(f"### {bottleneck.bottleneck_name}")
            md.append(f"**Sector**: {bottleneck.sector.value} | **Priority**: {bottleneck.priority} | **Confidence**: {bottleneck.confidence:.0%}")
            md.append("")
            md.append(f"**Description:** {bottleneck.description}")
            md.append("")
            md.append(f"**Evidence:**")
            for evidence in bottleneck.evidence:
                md.append(f"- {evidence}")
            md.append("")
            if bottleneck.private_companies:
                md.append(f"**Private Companies Solving This:** {', '.join(bottleneck.private_companies[:5])}")
            if bottleneck.public_proxies:
                md.append(f"**Public Proxies:** {', '.join(bottleneck.public_proxies)}")
            md.append("")
            md.append("---")
            md.append("")

        # Second-Order Plays
        md.append("## 🎯 SECOND-ORDER ARBITRAGE PLAYS")
        md.append("")
        md.append("*Suppliers to the suppliers - mispriced exposure to Wave 1 momentum*")
        md.append("")

        for play in report.second_order_plays[:5]:  # Top 5
            md.append(f"### {play.supplier_company}")
            md.append(f"**Ticker**: {play.supplier_ticker} | **Exposure**: {play.exposure_type}")
            md.append("")
            md.append(f"**Primary Technology:** {play.primary_technology} (Momentum: {play.primary_momentum_score:.1f}/100)")
            md.append(f"**Dependency Score:** {play.dependency_score:.0%}")
            md.append(f"**Price Correlation:** {play.price_correlation:.2f} (LOW = opportunity!)")
            md.append("")
            md.append(f"**Thesis:** {play.thesis}")
            md.append("")
            md.append(f"**Entry Timing:** {play.entry_timing} | **Risk-Adjusted Return:** {play.risk_adjusted_return}")
            md.append("")
            md.append("---")
            md.append("")

        # Save
        with open(filepath, 'w') as f:
            f.write('\n'.join(md))

        print(f"✅ Exported markdown report to {filepath}")


# ======================== MAIN EXECUTION ========================

def main():
    """Run the full engine"""

    # Initialize engine
    engine = TechMomentumArbitrageEngine()

    # Load companies
    companies = engine.load_companies_from_json("/home/user/Tsunami/data/companies.json")

    # Generate weekly report
    market_conditions = {
        "ipo_window": "open",
        "volatility": "medium",
        "interest_rates": "neutral",
    }

    report = engine.generate_weekly_report(companies, market_conditions)

    # Export reports
    output_dir = Path("/home/user/Tsunami/outputs/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d")

    engine.export_report_json(
        report,
        str(output_dir / f"weekly_alpha_report_{timestamp}.json")
    )

    engine.export_report_markdown(
        report,
        str(output_dir / f"weekly_alpha_report_{timestamp}.md")
    )

    print("\n" + "="*80)
    print("🎉 ENGINE RUN COMPLETE!")
    print("="*80)
    print(f"\nGenerated {report.signals_generated} signals")
    print(f"High-conviction plays: {report.high_conviction_count}")
    print(f"Emerging bottlenecks discovered: {len(report.emerging_bottlenecks)}")
    print(f"Second-order plays identified: {len(report.second_order_plays)}")
    print("\nReports saved to: outputs/reports/")


if __name__ == "__main__":
    main()
