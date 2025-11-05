"""
Tech Momentum Arbitrage Engine - Trade Signal Generator
Generates actionable trade signals with multi-tier exposure recommendations
"""

from datetime import datetime
from typing import List, Dict, Optional
from src.core.schemas import (
    Company,
    TradeSignal,
    MomentumScore,
    MoatScore,
    Catalyst,
    TradeRecommendation,
    DivergenceFlag,
)
from src.core.config import Config
from src.core.utils import calculate_position_size, time_to_catalyst


class TradeSignalGenerator:
    """
    Generate trade signals with:
    - Public market proxies (Tier 1)
    - Pre-IPO/private access (Tier 2)
    - Synthetic exposure (Tier 3)
    """

    def __init__(self, config: Config = Config()):
        self.config = config

    def generate_signal(
        self,
        rank: int,
        company: Company,
        momentum_score: MomentumScore,
        moat_score: MoatScore,
        next_catalyst: Optional[Catalyst],
    ) -> TradeSignal:
        """
        Generate comprehensive trade signal for a company

        Args:
            rank: Signal ranking
            company: Company object
            momentum_score: Momentum score
            moat_score: Moat score
            next_catalyst: Next predicted catalyst

        Returns:
            TradeSignal object
        """

        # Determine recommendation
        recommendation = self._generate_recommendation(momentum_score, moat_score)

        # Calculate conviction
        conviction = self._calculate_conviction(momentum_score, moat_score, next_catalyst)

        # Identify exposure routes
        public_proxy = self._identify_public_proxy(company)
        pre_ipo_access = self._identify_pre_ipo_access(company)
        synthetic_exposure = self._generate_synthetic_exposure(company)

        # Position sizing
        risk_level = self._assess_risk_level(company, moat_score)
        position_size = calculate_position_size(conviction, risk_level)

        # Entry timing
        entry_timing = self._determine_entry_timing(momentum_score, next_catalyst)

        # Risk factors
        risk_factors = self._identify_risk_factors(company, momentum_score, moat_score)

        # Expected return (qualitative)
        expected_return = self._estimate_expected_return(
            momentum_score, moat_score, next_catalyst
        )

        # Time horizon
        time_horizon = self._determine_time_horizon(next_catalyst)

        return TradeSignal(
            rank=rank,
            company=company.name,
            company_id=company.company_id,
            sector=company.sector,
            # Momentum metrics
            momentum_score=momentum_score.momentum_score,
            momentum_change_7d=momentum_score.momentum_change_7d,
            hype_score=momentum_score.hype_score,
            build_score=momentum_score.build_score,
            moat_score=moat_score.total_moat_score,
            # Exposure routes
            public_proxy=public_proxy,
            pre_ipo_access=pre_ipo_access,
            synthetic_exposure=synthetic_exposure,
            # Trade mechanics
            recommendation=recommendation,
            conviction=conviction,
            position_size=position_size,
            entry_timing=entry_timing,
            # Catalyst
            next_catalyst=next_catalyst.catalyst_type if next_catalyst else None,
            catalyst_date=next_catalyst.estimated_date if next_catalyst else None,
            # Risk assessment
            risk_factors=risk_factors,
            expected_return=expected_return,
            time_horizon=time_horizon,
            generated_date=datetime.now(),
        )

    def generate_signals(
        self,
        companies: List[Company],
        momentum_scores: List[MomentumScore],
        moat_scores: List[MoatScore],
        catalysts: Dict[str, Catalyst],
    ) -> List[TradeSignal]:
        """
        Generate signals for multiple companies

        Args:
            companies: List of companies
            momentum_scores: List of momentum scores (must be same order)
            moat_scores: List of moat scores (must be same order)
            catalysts: Dict mapping company_id to next catalyst

        Returns:
            List of TradeSignal objects, ranked by conviction
        """
        signals = []

        for i, company in enumerate(companies):
            momentum_score = momentum_scores[i]
            moat_score = moat_scores[i]
            next_catalyst = catalysts.get(company.company_id)

            signal = self.generate_signal(
                rank=i + 1,
                company=company,
                momentum_score=momentum_score,
                moat_score=moat_score,
                next_catalyst=next_catalyst,
            )

            signals.append(signal)

        # Re-rank by conviction
        signals.sort(key=lambda s: s.conviction, reverse=True)

        # Update ranks
        for i, signal in enumerate(signals):
            signal.rank = i + 1

        return signals

    def _generate_recommendation(
        self, momentum_score: MomentumScore, moat_score: MoatScore
    ) -> TradeRecommendation:
        """Generate buy/sell recommendation"""

        # CONFIRMED_MOMENTUM + High Moat = STRONG BUY
        if (
            momentum_score.divergence_flag == DivergenceFlag.CONFIRMED_MOMENTUM
            and moat_score.total_moat_score > 70
        ):
            return TradeRecommendation.STRONG_BUY

        # MISPRICED_OPPORTUNITY (low hype, high build) = BUY
        elif momentum_score.divergence_flag == DivergenceFlag.MISPRICED_OPPORTUNITY:
            return TradeRecommendation.BUY

        # High momentum, good moat = BUY
        elif (
            momentum_score.momentum_score > 75
            and moat_score.total_moat_score > 55
        ):
            return TradeRecommendation.BUY

        # BUBBLE_RISK (high hype, low build) = FADE or SHORT
        elif momentum_score.divergence_flag == DivergenceFlag.BUBBLE_RISK:
            return TradeRecommendation.FADE

        # Medium momentum = HOLD
        elif momentum_score.momentum_score > 50:
            return TradeRecommendation.HOLD

        # Low momentum = SELL
        else:
            return TradeRecommendation.SELL

    def _calculate_conviction(
        self,
        momentum_score: MomentumScore,
        moat_score: MoatScore,
        next_catalyst: Optional[Catalyst],
    ) -> float:
        """Calculate conviction level (0-1)"""

        # Base conviction from momentum
        momentum_conviction = momentum_score.momentum_score / 100

        # Moat adjustment (±0.15)
        moat_adjustment = (moat_score.total_moat_score - 50) / 500  # -0.10 to +0.10

        # Catalyst proximity boost
        catalyst_boost = 0.0
        if next_catalyst and next_catalyst.probability_6mo > 0.50:
            catalyst_boost = 0.10

        # Divergence flag adjustment
        divergence_adjustments = {
            DivergenceFlag.CONFIRMED_MOMENTUM: 0.10,
            DivergenceFlag.MISPRICED_OPPORTUNITY: 0.15,
            DivergenceFlag.BUBBLE_RISK: -0.25,
            DivergenceFlag.NO_SIGNAL: -0.10,
        }

        divergence_adj = divergence_adjustments.get(momentum_score.divergence_flag, 0)

        # Combined conviction
        conviction = (
            momentum_conviction + moat_adjustment + catalyst_boost + divergence_adj
        )

        return max(0.0, min(1.0, conviction))

    def _identify_public_proxy(self, company: Company) -> Optional[str]:
        """Identify public market proxy exposure"""
        if company.public_proxies:
            # Return the highest correlation proxy
            best_proxy = max(company.public_proxies, key=lambda p: p.correlation_score)
            return f"{best_proxy.ticker} ({best_proxy.exposure_type}, correlation {best_proxy.correlation_score:.2f})"

        # Fallback: sector ETFs
        sector_etfs = {
            "AI_Infra": "SKYY (Cloud Computing ETF) or WCLD",
            "Semiconductors": "SMH (Semiconductor ETF) or SOXX",
            "Cybersecurity": "HACK (Cybersecurity ETF) or CIBR",
            "Data_Infra": "SKYY (Cloud Computing ETF)",
            "Green_Energy": "ICLN (Clean Energy ETF) or TAN (Solar)",
            "6G": "ARKF (Fintech/Telecom) or IYZ (Telecom)",
            "Quantum": "QTUM (Quantum Computing ETF)",
            "Biotech_Infra": "XBI (Biotech ETF) or IBB",
        }

        return sector_etfs.get(company.sector.value, "QQQ (Nasdaq-100)")

    def _identify_pre_ipo_access(self, company: Company) -> Optional[str]:
        """Identify pre-IPO access routes"""

        # Companies with high IPO probability
        if company.ipo_probability_12mo > 0.50:
            # Check if likely available on secondary markets
            if company.total_funding > 300_000_000:
                # Large late-stage companies often have secondary liquidity
                return f"Secondary market access (Forge/EquityZen), estimated valuation ${company.last_valuation/1_000_000:.0f}M"

        # Otherwise, no easy pre-IPO access
        return None

    def _generate_synthetic_exposure(self, company: Company) -> Optional[str]:
        """Generate synthetic exposure strategy"""

        # Basket strategies for sectors
        if company.sector.value == "AI_Infra":
            return "Custom basket: 40% NVDA, 30% AVGO, 20% ANET, 10% VRT (cooling exposure)"
        elif company.sector.value == "Semiconductors":
            return "Custom basket: 30% ASML, 25% AMAT, 25% LRCX, 20% ENTG"
        elif company.sector.value == "6G":
            return "Custom basket: 35% QRVO, 35% SWKS, 30% GLW"
        elif company.sector.value == "Cybersecurity":
            return "HACK ETF or custom basket: 25% PANW, 25% CRWD, 25% ZS, 25% FTNT"
        elif company.sector.value == "Green_Energy":
            return "Custom basket: 40% FLNC, 30% ENPH, 30% MP (rare earths)"
        else:
            return "QQQ call spreads (tech proxy)"

    def _determine_entry_timing(
        self, momentum_score: MomentumScore, next_catalyst: Optional[Catalyst]
    ) -> str:
        """Determine optimal entry timing"""

        # High momentum + near-term catalyst = Immediate
        if momentum_score.momentum_score > 75 and next_catalyst:
            if next_catalyst.probability_6mo > 0.50:
                return "Immediate (catalyst within 6 months)"

        # Mispriced opportunity = Immediate
        if momentum_score.divergence_flag == DivergenceFlag.MISPRICED_OPPORTUNITY:
            return "Immediate (mispriced execution momentum)"

        # High momentum = Immediate
        if momentum_score.momentum_score > 75:
            return "Immediate"

        # Medium momentum = Staged entry
        if momentum_score.momentum_score > 55:
            return "Staged entry (build position over 30-60 days)"

        # Lower momentum = Wait for catalyst
        if next_catalyst:
            return f"Wait for catalyst (monitor until {next_catalyst.estimated_date.strftime('%Y-%m')})"

        return "Monitor (no immediate entry)"

    def _assess_risk_level(self, company: Company, moat_score: MoatScore) -> str:
        """Assess risk level"""

        # High moat = Lower risk
        if moat_score.total_moat_score > 70:
            return "Low"

        # Medium moat + late stage = Medium risk
        if moat_score.total_moat_score > 50 and company.total_funding > 300_000_000:
            return "Medium"

        # CapEx heavy sectors = Higher risk
        capex_sectors = ["Semiconductors", "Quantum", "6G", "Green_Energy"]
        if company.sector.value in capex_sectors:
            return "High"

        # Early stage = High risk
        if company.total_funding < 150_000_000:
            return "High"

        return "Medium"

    def _identify_risk_factors(
        self,
        company: Company,
        momentum_score: MomentumScore,
        moat_score: MoatScore,
    ) -> List[str]:
        """Identify key risk factors"""
        risks = []

        # Bubble risk
        if momentum_score.divergence_flag == DivergenceFlag.BUBBLE_RISK:
            risks.append("Bubble risk: High hype relative to execution")

        # Low moat
        if moat_score.total_moat_score < 40:
            risks.append("Weak competitive moat (susceptible to competition)")

        # Customer concentration
        if company.fortune_500_customers < 10:
            risks.append("Limited customer diversification")

        # Funding risk
        if company.total_funding < 200_000_000:
            risks.append("Requires additional funding rounds (dilution risk)")

        # CapEx intensity
        capex_sectors = ["Semiconductors", "Quantum", "6G", "Green_Energy"]
        if company.sector.value in capex_sectors:
            risks.append("Capital-intensive model (high burn rate)")

        # Market timing
        if company.ipo_probability_12mo > 0.60:
            risks.append("IPO window dependency (market conditions)")

        # Sector-specific
        if company.sector.value == "Quantum":
            risks.append("Technology commercialization timeline uncertain")
        elif company.sector.value == "Biotech_Infra":
            risks.append("Regulatory approval timelines")

        return risks

    def _estimate_expected_return(
        self,
        momentum_score: MomentumScore,
        moat_score: MoatScore,
        next_catalyst: Optional[Catalyst],
    ) -> str:
        """Estimate expected return (qualitative)"""

        # Very high conviction = High return potential
        if (
            momentum_score.momentum_score > 85
            and moat_score.total_moat_score > 70
            and next_catalyst
            and next_catalyst.probability_6mo > 0.60
        ):
            return "50-100% (12-18 months)"

        # High momentum + catalyst = Good return
        if momentum_score.momentum_score > 75 and next_catalyst:
            return "30-60% (12 months)"

        # Mispriced opportunity = Asymmetric
        if momentum_score.divergence_flag == DivergenceFlag.MISPRICED_OPPORTUNITY:
            return "40-80% (18-24 months, mispricing corrects)"

        # Moderate momentum = Moderate return
        if momentum_score.momentum_score > 60:
            return "20-40% (12-18 months)"

        # Lower conviction = Lower return
        return "10-25% (18-24 months)"

    def _determine_time_horizon(self, next_catalyst: Optional[Catalyst]) -> str:
        """Determine investment time horizon"""

        if not next_catalyst:
            return "18-36 months (long-term hold)"

        days = (next_catalyst.estimated_date - datetime.now()).days

        if days < 180:
            return "3-6 months (near-term catalyst)"
        elif days < 365:
            return "6-12 months (medium-term)"
        elif days < 730:
            return "12-24 months (long-term)"
        else:
            return "24+ months (very long-term)"

    def filter_high_conviction(
        self, signals: List[TradeSignal], threshold: float = 0.70
    ) -> List[TradeSignal]:
        """Filter for high-conviction signals"""
        return [s for s in signals if s.conviction >= threshold]

    def filter_by_recommendation(
        self, signals: List[TradeSignal], recommendation: TradeRecommendation
    ) -> List[TradeSignal]:
        """Filter by recommendation type"""
        return [s for s in signals if s.recommendation == recommendation]
