"""
Tech Momentum Arbitrage Engine - Moat Scoring Module
Evaluates competitive durability across 5 dimensions
"""

from datetime import datetime
from typing import List, Dict

from src.core.schemas import Company, MoatScore, WaveCategory, Sector
from src.core.config import Config
from src.core.utils import weighted_score, normalize_score


class MoatScoringEngine:
    """
    Competitive moat analysis across 5 dimensions:
    1. Regulatory Moat (30%) - ITAR, FDA, utility licenses, spectrum
    2. Network Effects (25%) - API adoption, developer ecosystem
    3. Capital Intensity (20%) - CapEx creates entry barriers
    4. Data Moat (15%) - Proprietary datasets, training advantages
    5. Switching Costs (10%) - Integration depth, workflow lock-in
    """

    def __init__(self, config: Config = Config()):
        self.config = config

    def calculate_moat_score(self, company: Company, industry_data: Dict = None) -> MoatScore:
        """
        Calculate comprehensive moat score

        Args:
            company: Company object
            industry_data: Additional industry-specific data

        Returns:
            MoatScore object with 5-dimension analysis
        """
        industry_data = industry_data or {}

        # 1. Regulatory Moat (0-100)
        regulatory_moat = self._score_regulatory_moat(company, industry_data)

        # 2. Network Effects (0-100)
        network_effects = self._score_network_effects(company)

        # 3. Capital Intensity (0-100)
        capital_intensity = self._score_capital_intensity(company)

        # 4. Data Moat (0-100)
        data_moat = self._score_data_moat(company)

        # 5. Switching Costs (0-100)
        switching_costs = self._score_switching_costs(company)

        # Weighted composite
        components = {
            "regulatory_moat": regulatory_moat,
            "network_effects": network_effects,
            "capital_intensity": capital_intensity,
            "data_moat": data_moat,
            "switching_costs": switching_costs,
        }
        total_moat_score = weighted_score(components, self.config.scoring.MOAT_WEIGHTS)

        # Determine wave potential and durability
        wave_potential = self._classify_wave_potential(total_moat_score, company)
        durability_rating = self._classify_durability(total_moat_score)

        return MoatScore(
            company_id=company.company_id,
            company_name=company.name,
            regulatory_moat=regulatory_moat,
            network_effects=network_effects,
            capital_intensity=capital_intensity,
            data_moat=data_moat,
            switching_costs=switching_costs,
            total_moat_score=total_moat_score,
            wave_potential=wave_potential,
            durability_rating=durability_rating,
            timestamp=datetime.now(),
        )

    def _score_regulatory_moat(self, company: Company, industry_data: Dict) -> float:
        """
        Score regulatory barriers (licenses, approvals, compliance requirements)

        High moat sectors: Defense (ITAR), Healthcare (FDA), Telecom (FCC spectrum),
        Energy (utility contracts), Quantum (export controls)
        """
        score = 0.0

        # Sector-based regulatory intensity
        high_regulatory_sectors = {
            Sector.SIX_G: 85.0,  # Spectrum licenses
            Sector.QUANTUM: 80.0,  # Export controls, national security
            Sector.GREEN_ENERGY: 75.0,  # Utility contracts, grid integration
            Sector.BIOTECH_INFRA: 70.0,  # FDA pathways
            Sector.CYBERSECURITY: 60.0,  # FedRAMP, defense contracts
            Sector.SEMICONDUCTORS: 55.0,  # Export controls (China)
            Sector.AI_INFRA: 30.0,  # Emerging regulation
            Sector.DATA_INFRA: 25.0,  # Data privacy laws
        }

        score = high_regulatory_sectors.get(company.sector, 20.0)

        # Government/defense customer presence (adds regulatory moat)
        has_defense = industry_data.get("has_defense_contracts", False)
        has_gov = industry_data.get("has_government_customers", False)

        if has_defense:
            score += 15.0
        elif has_gov:
            score += 8.0

        # Regulatory approvals obtained
        approvals = industry_data.get("regulatory_approvals", [])
        if approvals:
            score += min(len(approvals) * 3, 15.0)

        return min(score, 100.0)

    def _score_network_effects(self, company: Company) -> float:
        """
        Score network effects strength (platform effects, developer ecosystems)

        Strong network effects: API platforms, developer tools, marketplaces
        """
        score = 20.0  # Baseline

        # Customer count as proxy for network density
        customer_score = normalize_score(company.fortune_500_customers, 0, 100, 35)
        score += customer_score

        # Sector propensity for network effects
        network_effect_sectors = {
            Sector.DATA_INFRA: 25.0,  # Data pipelines create lock-in
            Sector.AI_INFRA: 20.0,  # Model serving platforms
            Sector.BIOTECH_INFRA: 15.0,  # Compound libraries
            Sector.CYBERSECURITY: 15.0,  # Security ecosystems
            Sector.SEMICONDUCTORS: 10.0,  # Design tool ecosystems
            Sector.GREEN_ENERGY: 5.0,  # Limited network effects
            Sector.QUANTUM: 10.0,  # Emerging developer ecosystem
            Sector.SIX_G: 15.0,  # Network infrastructure
        }

        score += network_effect_sectors.get(company.sector, 10.0)

        # Funding stage proxy (later stage = more network built)
        if company.total_funding > 500_000_000:
            score += 20.0
        elif company.total_funding > 200_000_000:
            score += 15.0
        elif company.total_funding > 100_000_000:
            score += 10.0

        return min(score, 100.0)

    def _score_capital_intensity(self, company: Company) -> float:
        """
        Score capital intensity as entry barrier

        High CapEx creates moats: Semiconductors (fabs), Datacenter infrastructure,
        Quantum (dilution refrigerators), 6G (satellites), Green Energy (plants)
        """
        # Sector-based CapEx intensity
        capex_intensity = {
            Sector.SEMICONDUCTORS: 95.0,  # Multi-billion dollar fabs
            Sector.QUANTUM: 90.0,  # Expensive cryogenic systems
            Sector.SIX_G: 85.0,  # Satellite constellations
            Sector.GREEN_ENERGY: 80.0,  # Power plants, grid storage
            Sector.AI_INFRA: 75.0,  # GPU clusters, datacenters
            Sector.BIOTECH_INFRA: 50.0,  # Lab equipment, but less intense
            Sector.CYBERSECURITY: 25.0,  # Software-centric
            Sector.DATA_INFRA: 30.0,  # Mostly software
        }

        base_score = capex_intensity.get(company.sector, 30.0)

        # Funding magnitude as CapEx proxy
        funding_boost = normalize_score(company.total_funding, 0, 1_000_000_000, 15)

        return min(base_score + funding_boost, 100.0)

    def _score_data_moat(self, company: Company) -> float:
        """
        Score proprietary data advantages (datasets, feedback loops, training data)

        Strong data moats: AI training data, biotech compound libraries,
        customer usage data, proprietary sensor networks
        """
        score = 15.0  # Baseline

        # Sector propensity for data moats
        data_moat_sectors = {
            Sector.AI_INFRA: 30.0,  # Training data, inference patterns
            Sector.DATA_INFRA: 25.0,  # Data transformation patterns
            Sector.BIOTECH_INFRA: 25.0,  # Compound libraries, experimental data
            Sector.CYBERSECURITY: 20.0,  # Threat intelligence
            Sector.SIX_G: 15.0,  # Network usage patterns
            Sector.GREEN_ENERGY: 10.0,  # Grid data
            Sector.SEMICONDUCTORS: 20.0,  # Design IP, process data
            Sector.QUANTUM: 15.0,  # Calibration data
        }

        score += data_moat_sectors.get(company.sector, 10.0)

        # Customer count = more data generated
        customer_boost = normalize_score(company.fortune_500_customers, 0, 100, 25)
        score += customer_boost

        # Patent count as proxy for proprietary knowledge
        patent_boost = normalize_score(company.patent_count, 0, 100, 20)
        score += patent_boost

        return min(score, 100.0)

    def _score_switching_costs(self, company: Company) -> float:
        """
        Score customer switching costs (integration depth, workflow lock-in)

        High switching costs: Infrastructure deeply embedded in workflows,
        compliance/certification requirements, API integration depth
        """
        score = 20.0  # Baseline

        # Sector switching cost intensity
        switching_cost_sectors = {
            Sector.DATA_INFRA: 30.0,  # Pipeline migrations are painful
            Sector.CYBERSECURITY: 25.0,  # Security posture lock-in
            Sector.AI_INFRA: 20.0,  # Model retraining costs
            Sector.BIOTECH_INFRA: 25.0,  # Workflow integration
            Sector.SEMICONDUCTORS: 30.0,  # Design tool lock-in
            Sector.GREEN_ENERGY: 20.0,  # Long-term contracts
            Sector.QUANTUM: 15.0,  # Early, less lock-in yet
            Sector.SIX_G: 25.0,  # Infrastructure dependencies
        }

        score += switching_cost_sectors.get(company.sector, 15.0)

        # Enterprise customer count (enterprises have higher switching costs)
        customer_boost = normalize_score(company.fortune_500_customers, 0, 100, 30)
        score += customer_boost

        # Funding/maturity proxy (mature products have deeper integration)
        if company.total_funding > 300_000_000:
            score += 25.0
        elif company.total_funding > 150_000_000:
            score += 15.0
        elif company.total_funding > 75_000_000:
            score += 10.0

        return min(score, 100.0)

    def _classify_wave_potential(self, moat_score: float, company: Company) -> WaveCategory:
        """
        Classify wave potential based on moat strength

        Wave 4 candidates: Moat > 75 (potential rail owners)
        Wave 3: Moat 60-75 (embedding as middleware)
        Wave 2: Moat 40-60 (arbitrage phase)
        Wave 1: Moat < 40 (replacement phase)
        """
        if moat_score >= self.config.thresholds.WAVE_4_MOAT_THRESHOLD:
            return WaveCategory.WAVE_4

        elif moat_score >= self.config.thresholds.STRONG_MOAT:
            return WaveCategory.WAVE_3

        elif moat_score >= self.config.thresholds.MEDIUM_MOAT:
            return WaveCategory.WAVE_2

        else:
            # Default to company's current wave classification
            return company.wave_category

    def _classify_durability(self, moat_score: float) -> str:
        """Convert moat score to qualitative durability rating"""
        if moat_score >= 80:
            return "Very High"
        elif moat_score >= 60:
            return "High"
        elif moat_score >= 40:
            return "Medium"
        else:
            return "Low"

    def score_companies(
        self,
        companies: List[Company],
        industry_data_map: Dict[str, Dict] = None,
    ) -> List[MoatScore]:
        """Score multiple companies in batch"""
        industry_data_map = industry_data_map or {}

        scores = []
        for company in companies:
            industry_data = industry_data_map.get(company.company_id, {})
            score = self.calculate_moat_score(company, industry_data)
            scores.append(score)

        # Sort by total moat score descending
        scores.sort(key=lambda s: s.total_moat_score, reverse=True)

        return scores

    def filter_wave_4_candidates(self, scores: List[MoatScore]) -> List[MoatScore]:
        """Filter for Wave 4 candidates (potential rail owners)"""
        threshold = self.config.thresholds.WAVE_4_MOAT_THRESHOLD
        return [s for s in scores if s.total_moat_score >= threshold]
