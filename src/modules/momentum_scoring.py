"""
Tech Momentum Arbitrage Engine - Momentum Scoring Module
Implements dual-track momentum scoring: Narrative (Hype) + Execution (Build)
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math

from src.core.schemas import (
    Company,
    MomentumScore,
    DivergenceFlag,
    FundingRound,
    PatentGrant,
    ExecutiveHire,
)
from src.core.config import Config
from src.core.utils import (
    weighted_score,
    moving_average,
    exponential_moving_average,
    normalize_score,
    sigmoid,
)


class MomentumScoringEngine:
    """
    Dual-track momentum scoring system
    Track A: Narrative Momentum (Hype Score)
    Track B: Execution Momentum (Build Score)
    """

    def __init__(self, config: Config = Config()):
        self.config = config

    def calculate_momentum_score(
        self,
        company: Company,
        media_mentions: List[Dict] = None,
        social_metrics: Dict = None,
        vc_mentions: List[str] = None,
        search_data: Dict = None,
    ) -> MomentumScore:
        """
        Calculate comprehensive momentum score for a company

        Args:
            company: Company object with core data
            media_mentions: List of media mentions with timestamps
            social_metrics: Social media metrics (followers, engagement)
            vc_mentions: List of VC thesis mentions
            search_data: Google Trends data

        Returns:
            MomentumScore object with dual-track scoring
        """

        # Track A: Narrative Momentum (Hype Score)
        hype_components = self._calculate_hype_score(
            company, media_mentions, social_metrics, vc_mentions, search_data
        )

        # Track B: Execution Momentum (Build Score)
        build_components = self._calculate_build_score(company)

        # Composite momentum score
        hype_score = weighted_score(
            hype_components, self.config.scoring.HYPE_WEIGHTS
        )
        build_score = weighted_score(
            build_components, self.config.scoring.BUILD_WEIGHTS
        )

        momentum_score = weighted_score(
            {"hype": hype_score, "build": build_score},
            self.config.scoring.MOMENTUM_COMPOSITE_WEIGHTS,
        )

        # Detect divergence
        divergence_flag = self._detect_divergence(hype_score, build_score)

        return MomentumScore(
            company_id=company.company_id,
            company_name=company.name,
            # Hype components
            media_velocity=hype_components["media_velocity"],
            social_signal=hype_components["social_signal"],
            vc_buzz=hype_components["vc_buzz"],
            conference_presence=hype_components["conference_presence"],
            search_trends=hype_components["search_trends"],
            hype_score=hype_score,
            # Build components
            revenue_indicators=build_components["revenue_indicators"],
            customer_logos=build_components["customer_logos"],
            patent_velocity=build_components["patent_velocity"],
            talent_density=build_components["talent_density"],
            product_milestones=build_components["product_milestones"],
            build_score=build_score,
            # Composite
            momentum_score=momentum_score,
            momentum_change_7d=0.0,  # Would be calculated from time series
            momentum_change_30d=0.0,
            divergence_flag=divergence_flag,
            timestamp=datetime.now(),
        )

    def _calculate_hype_score(
        self,
        company: Company,
        media_mentions: Optional[List[Dict]],
        social_metrics: Optional[Dict],
        vc_mentions: Optional[List[str]],
        search_data: Optional[Dict],
    ) -> Dict[str, float]:
        """
        Calculate Track A: Narrative Momentum (Hype)

        Components:
        1. Media Velocity - Mention frequency in tech press (30-day MA)
        2. Social Signal - LinkedIn/Twitter growth and engagement
        3. VC Buzz - Appearance in VC thesis docs
        4. Conference Presence - Speaking slots at major events
        5. Search Trends - Google Trends momentum
        """

        # 1. Media Velocity (0-100)
        media_velocity = self._score_media_velocity(media_mentions)

        # 2. Social Signal (0-100)
        social_signal = self._score_social_signal(social_metrics)

        # 3. VC Buzz (0-100)
        vc_buzz = self._score_vc_buzz(vc_mentions, company.funding_rounds)

        # 4. Conference Presence (0-100)
        conference_presence = self._score_conference_presence(company)

        # 5. Search Trends (0-100)
        search_trends = self._score_search_trends(search_data)

        return {
            "media_velocity": media_velocity,
            "social_signal": social_signal,
            "vc_buzz": vc_buzz,
            "conference_presence": conference_presence,
            "search_trends": search_trends,
        }

    def _calculate_build_score(self, company: Company) -> Dict[str, float]:
        """
        Calculate Track B: Execution Momentum (Build)

        Components:
        1. Revenue Indicators - Estimated ARR growth
        2. Customer Logos - Fortune 500 adoption rate
        3. Patent Velocity - USPTO grants per quarter
        4. Talent Density - Engineer headcount + FAANG talent %
        5. Product Milestones - GA launches, API adoption
        """

        # 1. Revenue Indicators (0-100)
        revenue_indicators = self._score_revenue_indicators(company)

        # 2. Customer Logos (0-100)
        customer_logos = self._score_customer_logos(company)

        # 3. Patent Velocity (0-100)
        patent_velocity = self._score_patent_velocity(company.patent_grants)

        # 4. Talent Density (0-100)
        talent_density = self._score_talent_density(company)

        # 5. Product Milestones (0-100)
        product_milestones = self._score_product_milestones(company)

        return {
            "revenue_indicators": revenue_indicators,
            "customer_logos": customer_logos,
            "patent_velocity": patent_velocity,
            "talent_density": talent_density,
            "product_milestones": product_milestones,
        }

    # ======================== HYPE SCORING FUNCTIONS ========================

    def _score_media_velocity(self, media_mentions: Optional[List[Dict]]) -> float:
        """Score based on media mention frequency (30-day MA)"""
        if not media_mentions:
            return 20.0  # Baseline for unknown

        # Count mentions in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_mentions = [
            m for m in media_mentions if m.get("date", datetime.min) > thirty_days_ago
        ]

        mention_count = len(recent_mentions)

        # Normalize: 0 mentions = 0, 50+ mentions = 100
        return normalize_score(mention_count, 0, 50, 100)

    def _score_social_signal(self, social_metrics: Optional[Dict]) -> float:
        """Score based on social media growth and engagement"""
        if not social_metrics:
            return 25.0  # Baseline

        # LinkedIn follower growth rate (monthly)
        linkedin_growth = social_metrics.get("linkedin_growth_rate", 0)
        # Twitter/X engagement rate
        twitter_engagement = social_metrics.get("twitter_engagement", 0)

        # Combined score
        linkedin_score = normalize_score(linkedin_growth, 0, 20, 50)  # 0-20% growth
        twitter_score = normalize_score(
            twitter_engagement, 0, 10, 50
        )  # 0-10% engagement

        return linkedin_score + twitter_score

    def _score_vc_buzz(
        self, vc_mentions: Optional[List[str]], funding_rounds: List[FundingRound]
    ) -> float:
        """Score based on VC thesis mentions and investor quality"""
        score = 0.0

        # Mentions in VC thesis documents
        if vc_mentions:
            mention_count = len(vc_mentions)
            score += normalize_score(mention_count, 0, 10, 40)

        # Tier-1 VC backing (a16z, Sequoia, etc.)
        tier_1_vcs = {
            "Andreessen Horowitz",
            "Sequoia Capital",
            "Benchmark",
            "Lightspeed",
            "Accel",
            "Greylock",
            "Kleiner Perkins",
            "Index Ventures",
        }

        has_tier_1 = any(
            any(vc in round.lead_investor for vc in tier_1_vcs)
            for round in funding_rounds
        )

        if has_tier_1:
            score += 30.0

        # Recent funding activity (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        recent_funding = any(round.date > six_months_ago for round in funding_rounds)

        if recent_funding:
            score += 30.0

        return min(score, 100.0)

    def _score_conference_presence(self, company: Company) -> float:
        """Score based on conference appearances (proxy via sector and stage)"""
        # In real implementation, would track actual conference speaking slots
        # For now, use funding stage as proxy

        total_funding = company.total_funding

        # Late-stage companies get more conference slots
        if total_funding > 500_000_000:  # $500M+
            return 80.0
        elif total_funding > 200_000_000:  # $200M+
            return 60.0
        elif total_funding > 100_000_000:  # $100M+
            return 40.0
        elif total_funding > 50_000_000:  # $50M+
            return 25.0
        else:
            return 10.0

    def _score_search_trends(self, search_data: Optional[Dict]) -> float:
        """Score based on Google Trends data"""
        if not search_data:
            return 20.0

        # Interest over time (0-100 scale from Google Trends)
        current_interest = search_data.get("current_interest", 0)
        previous_interest = search_data.get("previous_interest", 0)

        # Growth in interest
        if previous_interest > 0:
            growth = (current_interest - previous_interest) / previous_interest
            return normalize_score(growth, -0.5, 0.5, 100)  # -50% to +50% growth
        else:
            return normalize_score(current_interest, 0, 100, 100)

    # ======================== BUILD SCORING FUNCTIONS ========================

    def _score_revenue_indicators(self, company: Company) -> float:
        """Score based on revenue growth indicators"""
        if not company.estimated_arr:
            # Use funding as proxy if no ARR data
            if company.total_funding > 500_000_000:
                return 70.0  # Likely $100M+ ARR
            elif company.total_funding > 200_000_000:
                return 50.0
            else:
                return 30.0

        arr = company.estimated_arr

        # Score based on ARR magnitude and implied growth
        if arr > 500_000_000:  # $500M+
            return 95.0
        elif arr > 200_000_000:  # $200M+
            return 85.0
        elif arr > 100_000_000:  # $100M+
            return 75.0
        elif arr > 50_000_000:  # $50M+
            return 60.0
        elif arr > 20_000_000:  # $20M+
            return 45.0
        else:
            return 25.0

    def _score_customer_logos(self, company: Company) -> float:
        """Score based on Fortune 500 customer count"""
        f500_count = company.fortune_500_customers

        # Normalize: 0 customers = 0, 100+ customers = 100
        return normalize_score(f500_count, 0, 100, 100)

    def _score_patent_velocity(self, patent_grants: List[PatentGrant]) -> float:
        """Score based on patent grants per quarter (citation-weighted)"""
        if not patent_grants:
            return 15.0  # Baseline for no patents

        # Count grants in last year
        one_year_ago = datetime.now() - timedelta(days=365)
        recent_grants = [p for p in patent_grants if p.grant_date > one_year_ago]

        # Weight by citations
        weighted_count = sum(
            1 + (patent.citation_count * 0.1) for patent in recent_grants
        )

        # Quarterly rate
        quarterly_rate = weighted_count / 4

        # Normalize: 0 = 0, 10+ per quarter = 100
        return normalize_score(quarterly_rate, 0, 10, 100)

    def _score_talent_density(self, company: Company) -> float:
        """Score based on engineer headcount growth and FAANG talent %"""
        score = 0.0

        # Headcount magnitude
        if company.employee_count > 5000:
            score += 30.0
        elif company.employee_count > 2000:
            score += 25.0
        elif company.employee_count > 1000:
            score += 20.0
        elif company.employee_count > 500:
            score += 15.0
        elif company.employee_count > 200:
            score += 10.0

        # Engineer percentage (high talent density)
        engineer_score = normalize_score(company.engineer_pct, 0, 70, 35)  # 0-70%
        score += engineer_score

        # FAANG talent percentage (quality signal)
        faang_score = normalize_score(company.faang_talent_pct, 0, 30, 35)  # 0-30%
        score += faang_score

        return min(score, 100.0)

    def _score_product_milestones(self, company: Company) -> float:
        """Score based on product launches and adoption (proxy via customers)"""
        # In real implementation, would track actual GA launches, API adoption metrics
        # For now, use customer count as proxy for product-market fit

        base_score = 20.0

        # Customer adoption proxy
        if company.fortune_500_customers > 50:
            base_score += 40.0
        elif company.fortune_500_customers > 20:
            base_score += 30.0
        elif company.fortune_500_customers > 10:
            base_score += 20.0

        # Funding stage proxy (later stage = more product milestones)
        if company.total_funding > 500_000_000:
            base_score += 40.0
        elif company.total_funding > 200_000_000:
            base_score += 30.0
        elif company.total_funding > 100_000_000:
            base_score += 20.0

        return min(base_score, 100.0)

    # ======================== DIVERGENCE DETECTION ========================

    def _detect_divergence(self, hype_score: float, build_score: float) -> DivergenceFlag:
        """
        Detect divergence between narrative and execution momentum

        Quadrants:
        - High Hype + High Build = CONFIRMED_MOMENTUM (both > 65)
        - Low Hype + High Build = MISPRICED_OPPORTUNITY (hype < 45, build > 65)
        - High Hype + Low Build = BUBBLE_RISK (hype > 65, build < 45)
        - Low Hype + Low Build = NO_SIGNAL (both < 45)
        """
        high_threshold = self.config.thresholds.HIGH_SCORE_THRESHOLD
        low_threshold = self.config.thresholds.LOW_SCORE_THRESHOLD

        if hype_score >= high_threshold and build_score >= high_threshold:
            return DivergenceFlag.CONFIRMED_MOMENTUM

        elif hype_score < low_threshold and build_score >= high_threshold:
            return DivergenceFlag.MISPRICED_OPPORTUNITY

        elif hype_score >= high_threshold and build_score < low_threshold:
            return DivergenceFlag.BUBBLE_RISK

        else:
            return DivergenceFlag.NO_SIGNAL

    # ======================== BATCH SCORING ========================

    def score_companies(
        self,
        companies: List[Company],
        external_data: Optional[Dict[str, Dict]] = None,
    ) -> List[MomentumScore]:
        """
        Score multiple companies in batch

        Args:
            companies: List of Company objects
            external_data: Dict mapping company_id to external data (media, social, etc.)

        Returns:
            List of MomentumScore objects
        """
        scores = []

        for company in companies:
            # Get external data if available
            ext_data = external_data.get(company.company_id, {}) if external_data else {}

            score = self.calculate_momentum_score(
                company=company,
                media_mentions=ext_data.get("media_mentions"),
                social_metrics=ext_data.get("social_metrics"),
                vc_mentions=ext_data.get("vc_mentions"),
                search_data=ext_data.get("search_data"),
            )

            scores.append(score)

        # Sort by momentum score descending
        scores.sort(key=lambda s: s.momentum_score, reverse=True)

        return scores

    def filter_high_conviction(
        self, scores: List[MomentumScore], threshold: float = 75.0
    ) -> List[MomentumScore]:
        """Filter for high-conviction plays above threshold"""
        return [s for s in scores if s.momentum_score >= threshold]

    def filter_by_divergence(
        self, scores: List[MomentumScore], flag: DivergenceFlag
    ) -> List[MomentumScore]:
        """Filter by specific divergence pattern"""
        return [s for s in scores if s.divergence_flag == flag]


# ======================== STANDALONE FUNCTIONS ========================


def calculate_quick_momentum(
    total_funding: float,
    fortune_500_customers: int,
    patent_count: int,
    employee_count: int,
) -> float:
    """
    Quick momentum estimate from basic metrics
    Useful for initial screening before full scoring
    """
    funding_score = normalize_score(total_funding, 0, 500_000_000, 30)
    customer_score = normalize_score(fortune_500_customers, 0, 100, 30)
    patent_score = normalize_score(patent_count, 0, 50, 20)
    employee_score = normalize_score(employee_count, 0, 2000, 20)

    return funding_score + customer_score + patent_score + employee_score
