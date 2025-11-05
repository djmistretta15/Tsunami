"""
Tech Momentum Arbitrage Engine - Timing & Catalyst Prediction Module
Predicts WHEN momentum converts to tradeable events
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math

from src.core.schemas import Company, Catalyst, ExecutiveHire
from src.core.config import Config
from src.core.utils import days_until, probability_decay, time_to_catalyst


class TimingPredictionEngine:
    """
    Predict timing of investable catalysts:
    - IPO filings and pricing windows
    - M&A exit events
    - Product launches
    - Regulatory approvals
    """

    def __init__(self, config: Config = Config()):
        self.config = config

    def predict_ipo_timing(
        self, company: Company, market_conditions: Dict = None
    ) -> Catalyst:
        """
        Predict IPO timing based on leading indicators

        Signals:
        1. CFO/CCO hire → 9-month leading indicator
        2. Series D+ funding → 18-month median to IPO
        3. Revenue scale ($100M+ ARR)
        4. Market window health
        """
        market_conditions = market_conditions or {"ipo_window": "open", "volatility": "low"}

        # Base probability from funding stage
        funding_stage_prob = self._funding_stage_probability(company)

        # CFO/CCO hire signal (strongest predictor)
        cfo_signal_prob = self._cfo_hire_signal(company)

        # Revenue scale readiness
        revenue_readiness = self._revenue_readiness(company)

        # Market window adjustment
        market_multiplier = self._market_window_multiplier(market_conditions)

        # Combined probability
        base_prob = (funding_stage_prob + cfo_signal_prob + revenue_readiness) / 3
        adjusted_prob = base_prob * market_multiplier

        # Estimate date
        estimated_date = self._estimate_ipo_date(company)

        # Calculate 6-month and 12-month probabilities
        days_to_event = days_until(estimated_date)

        if days_to_event < 180:  # Within 6 months
            prob_6mo = adjusted_prob
            prob_12mo = min(adjusted_prob + 0.15, 0.95)
        elif days_to_event < 365:  # 6-12 months
            prob_6mo = adjusted_prob * 0.5
            prob_12mo = adjusted_prob
        else:  # Beyond 12 months
            prob_6mo = adjusted_prob * 0.2
            prob_12mo = adjusted_prob * 0.6

        # Identify leading indicators
        leading_indicators = self._identify_ipo_indicators(company)

        # Risk factors
        risk_factors = self._identify_ipo_risks(company, market_conditions)

        return Catalyst(
            catalyst_type="IPO Filing Expected",
            estimated_date=estimated_date,
            confidence=adjusted_prob,
            probability_6mo=round(prob_6mo, 2),
            probability_12mo=round(prob_12mo, 2),
            leading_indicators=leading_indicators,
            risk_factors=risk_factors,
        )

    def predict_ma_timing(self, company: Company) -> Optional[Catalyst]:
        """
        Predict M&A exit timing

        Signals:
        - Acquisition multiples in sector
        - Strategic buyer presence
        - Competitive pressure
        - Funding runway
        """
        # Simple heuristic: companies with moderate funding, no IPO path
        if company.total_funding < 100_000_000:
            return None  # Too early

        if company.total_funding > 500_000_000:
            # More likely IPO path
            return None

        # Estimate acquisition probability
        ma_prob = 0.35  # Base probability for mid-stage companies

        # Sector with high M&A activity
        high_ma_sectors = ["Cybersecurity", "Data_Infra", "Biotech_Infra"]
        if company.sector.value in high_ma_sectors:
            ma_prob += 0.15

        # Estimate timing (12-24 months)
        estimated_date = datetime.now() + timedelta(days=540)  # 18 months

        return Catalyst(
            catalyst_type="M&A Exit Potential",
            estimated_date=estimated_date,
            confidence=ma_prob,
            probability_6mo=0.10,
            probability_12mo=0.25,
            leading_indicators=[
                "Strategic buyer interest in sector",
                "Competitive consolidation pressure",
            ],
            risk_factors=["Market multiples compression", "Antitrust scrutiny"],
        )

    def predict_product_launch(self, company: Company) -> List[Catalyst]:
        """
        Predict major product launch timing

        Patent grant → Product launch: 6-12 month lag
        """
        catalysts = []

        if not company.patent_grants:
            return catalysts

        # Recent patents → upcoming launches
        six_months_ago = datetime.now() - timedelta(days=180)
        recent_patents = [
            p for p in company.patent_grants if p.grant_date > six_months_ago
        ]

        if recent_patents:
            # Estimate launch 6 months from grant
            avg_grant_date = sum(
                (p.grant_date - datetime(1970, 1, 1)).days for p in recent_patents
            ) / len(recent_patents)
            avg_date = datetime(1970, 1, 1) + timedelta(days=avg_grant_date)

            estimated_launch = avg_date + timedelta(days=180)

            catalyst = Catalyst(
                catalyst_type="Product Launch Expected",
                estimated_date=estimated_launch,
                confidence=0.60,
                probability_6mo=0.70,
                probability_12mo=0.90,
                leading_indicators=[
                    f"{len(recent_patents)} recent patent grants",
                    "Technology development timeline",
                ],
                risk_factors=["Development delays", "Regulatory approvals"],
            )

            catalysts.append(catalyst)

        return catalysts

    def predict_regulatory_approval(
        self, company: Company, regulatory_context: Dict = None
    ) -> Optional[Catalyst]:
        """
        Predict regulatory approval timing (FDA, FCC, etc.)

        Sector-specific timelines
        """
        regulatory_context = regulatory_context or {}

        # Only relevant for certain sectors
        regulated_sectors = {
            "Biotech_Infra": {"agency": "FDA", "avg_timeline_days": 365},
            "6G": {"agency": "FCC", "avg_timeline_days": 180},
            "Green_Energy": {"agency": "DOE/FERC", "avg_timeline_days": 270},
        }

        if company.sector.value not in regulated_sectors:
            return None

        sector_data = regulated_sectors[company.sector.value]

        # Check if regulatory process is underway
        in_review = regulatory_context.get("in_regulatory_review", False)

        if not in_review:
            return None

        estimated_date = datetime.now() + timedelta(
            days=sector_data["avg_timeline_days"]
        )

        return Catalyst(
            catalyst_type=f"{sector_data['agency']} Approval Expected",
            estimated_date=estimated_date,
            confidence=0.65,
            probability_6mo=0.40,
            probability_12mo=0.75,
            leading_indicators=["Regulatory filing submitted", "Review process initiated"],
            risk_factors=["Regulatory delays", "Compliance issues"],
        )

    # ======================== HELPER FUNCTIONS ========================

    def _funding_stage_probability(self, company: Company) -> float:
        """IPO probability based on funding stage"""
        total_funding = company.total_funding

        if total_funding > 1_000_000_000:  # $1B+ (unicorn+)
            return 0.75
        elif total_funding > 500_000_000:  # $500M+
            return 0.60
        elif total_funding > 300_000_000:  # $300M+
            return 0.45
        elif total_funding > 150_000_000:  # $150M+ (Series C/D)
            return 0.25
        else:
            return 0.10

    def _cfo_hire_signal(self, company: Company) -> float:
        """CFO/CCO hire as IPO leading indicator (9-month lead time)"""
        if not company.executive_hires:
            return 0.15

        # Look for CFO or Chief Commercial Officer hires
        nine_months_ago = datetime.now() - timedelta(days=270)
        eighteen_months_ago = datetime.now() - timedelta(days=540)

        recent_cfo = any(
            hire.date > nine_months_ago
            and hire.date < datetime.now()
            and ("CFO" in hire.role.upper() or "CHIEF FINANCIAL" in hire.role.upper())
            for hire in company.executive_hires
        )

        if recent_cfo:
            return 0.85  # Strong signal

        # Check for earlier CFO hire (signal fading)
        earlier_cfo = any(
            hire.date > eighteen_months_ago
            and hire.date < nine_months_ago
            and ("CFO" in hire.role.upper() or "CHIEF FINANCIAL" in hire.role.upper())
            for hire in company.executive_hires
        )

        if earlier_cfo:
            return 0.60

        return 0.15

    def _revenue_readiness(self, company: Company) -> float:
        """IPO readiness based on revenue scale"""
        if not company.estimated_arr:
            # Infer from funding
            if company.total_funding > 500_000_000:
                return 0.60
            else:
                return 0.20

        arr = company.estimated_arr

        if arr > 500_000_000:  # $500M+ ARR
            return 0.90
        elif arr > 200_000_000:  # $200M+ ARR
            return 0.75
        elif arr > 100_000_000:  # $100M+ ARR (typical minimum)
            return 0.60
        elif arr > 50_000_000:  # $50M+ ARR
            return 0.35
        else:
            return 0.15

    def _market_window_multiplier(self, market_conditions: Dict) -> float:
        """Adjust probability based on IPO market window health"""
        window_status = market_conditions.get("ipo_window", "open")
        volatility = market_conditions.get("volatility", "medium")

        multipliers = {
            "open": {"low": 1.2, "medium": 1.0, "high": 0.7},
            "mixed": {"low": 1.0, "medium": 0.8, "high": 0.5},
            "closed": {"low": 0.6, "medium": 0.4, "high": 0.2},
        }

        return multipliers.get(window_status, {}).get(volatility, 1.0)

    def _estimate_ipo_date(self, company: Company) -> datetime:
        """Estimate IPO filing date"""
        # Default: 12 months from now
        base_estimate = datetime.now() + timedelta(days=365)

        # Adjust based on CFO hire
        if company.executive_hires:
            cfo_hires = [
                hire
                for hire in company.executive_hires
                if "CFO" in hire.role.upper() or "CHIEF FINANCIAL" in hire.role.upper()
            ]

            if cfo_hires:
                # Most recent CFO hire
                latest_cfo = max(cfo_hires, key=lambda h: h.date)

                # IPO typically 9 months after CFO hire
                cfo_based_estimate = latest_cfo.date + timedelta(days=270)

                # Use the nearer date
                if cfo_based_estimate > datetime.now():
                    return cfo_based_estimate

        # Adjust based on funding stage
        if company.total_funding > 1_000_000_000:
            # Unicorns typically IPO within 18 months if ready
            base_estimate = datetime.now() + timedelta(days=540)
        elif company.total_funding > 500_000_000:
            # Late-stage: 12-24 months
            base_estimate = datetime.now() + timedelta(days=450)
        elif company.total_funding > 300_000_000:
            # Series D: 18-36 months
            base_estimate = datetime.now() + timedelta(days=730)

        return base_estimate

    def _identify_ipo_indicators(self, company: Company) -> List[str]:
        """List leading indicators present for company"""
        indicators = []

        # CFO hire
        if company.executive_hires:
            recent_cfo = any(
                "CFO" in hire.role.upper() or "CHIEF FINANCIAL" in hire.role.upper()
                for hire in company.executive_hires
                if hire.date > datetime.now() - timedelta(days=365)
            )
            if recent_cfo:
                indicators.append("CFO hire within last 12 months")

        # Revenue scale
        if company.estimated_arr and company.estimated_arr > 100_000_000:
            indicators.append(f"${company.estimated_arr/1_000_000:.0f}M+ ARR scale")

        # Late-stage funding
        if company.total_funding > 300_000_000:
            indicators.append(
                f"${company.total_funding/1_000_000:.0f}M raised (late-stage)"
            )

        # Customer traction
        if company.fortune_500_customers > 50:
            indicators.append(f"{company.fortune_500_customers} Fortune 500 customers")

        # Sector momentum
        indicators.append(f"{company.sector.value} sector momentum")

        return indicators

    def _identify_ipo_risks(
        self, company: Company, market_conditions: Dict
    ) -> List[str]:
        """List risk factors for IPO timing"""
        risks = []

        # Market conditions
        if market_conditions.get("ipo_window") == "closed":
            risks.append("IPO market window closed")
        elif market_conditions.get("volatility") == "high":
            risks.append("High market volatility")

        # Interest rate sensitivity
        if market_conditions.get("interest_rates", "neutral") == "rising":
            risks.append("Rising interest rates (duration risk for unprofitable growth)")

        # Company-specific
        if not company.estimated_arr or company.estimated_arr < 100_000_000:
            risks.append("Revenue scale below typical IPO threshold")

        # Sector-specific
        capex_heavy_sectors = ["Semiconductors", "Quantum", "6G", "Green_Energy"]
        if company.sector.value in capex_heavy_sectors:
            risks.append("Capital-intensive business model (profitability scrutiny)")

        # Competitive
        if company.fortune_500_customers < 20:
            risks.append("Limited customer diversification")

        return risks

    def get_all_catalysts(
        self, company: Company, market_conditions: Dict = None
    ) -> List[Catalyst]:
        """Get all predicted catalysts for a company"""
        catalysts = []

        # IPO timing (most important)
        ipo_catalyst = self.predict_ipo_timing(company, market_conditions)
        if ipo_catalyst.confidence > 0.30:
            catalysts.append(ipo_catalyst)

        # M&A potential
        ma_catalyst = self.predict_ma_timing(company)
        if ma_catalyst:
            catalysts.append(ma_catalyst)

        # Product launches
        product_catalysts = self.predict_product_launch(company)
        catalysts.extend(product_catalysts)

        # Regulatory approvals
        reg_catalyst = self.predict_regulatory_approval(company)
        if reg_catalyst:
            catalysts.append(reg_catalyst)

        # Sort by estimated date
        catalysts.sort(key=lambda c: c.estimated_date)

        return catalysts

    def get_next_catalyst(
        self, company: Company, market_conditions: Dict = None
    ) -> Optional[Catalyst]:
        """Get the next imminent catalyst"""
        catalysts = self.get_all_catalysts(company, market_conditions)

        if not catalysts:
            return None

        # Return the earliest catalyst
        return catalysts[0]
