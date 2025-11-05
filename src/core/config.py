"""
Tech Momentum Arbitrage Engine - Configuration
Central configuration for scoring weights, thresholds, and system parameters
"""

from typing import Dict


class ScoringWeights:
    """Weights for momentum scoring algorithms"""

    # Hype Score (Narrative Momentum) weights - sum to 1.0
    HYPE_WEIGHTS = {
        "media_velocity": 0.25,
        "social_signal": 0.20,
        "vc_buzz": 0.30,
        "conference_presence": 0.15,
        "search_trends": 0.10,
    }

    # Build Score (Execution Momentum) weights - sum to 1.0
    BUILD_WEIGHTS = {
        "revenue_indicators": 0.30,
        "customer_logos": 0.25,
        "patent_velocity": 0.15,
        "talent_density": 0.20,
        "product_milestones": 0.10,
    }

    # Composite momentum: Hype vs Build weighting
    MOMENTUM_COMPOSITE_WEIGHTS = {
        "hype": 0.40,
        "build": 0.60,
    }

    # Moat Score weights - sum to 1.0
    MOAT_WEIGHTS = {
        "regulatory_moat": 0.30,
        "network_effects": 0.25,
        "capital_intensity": 0.20,
        "data_moat": 0.15,
        "switching_costs": 0.10,
    }


class Thresholds:
    """Thresholds for signal classification"""

    # Momentum score thresholds
    HIGH_MOMENTUM = 75.0
    MEDIUM_MOMENTUM = 50.0
    LOW_MOMENTUM = 30.0

    # Divergence detection thresholds
    HIGH_SCORE_THRESHOLD = 65.0  # Above this = "high"
    LOW_SCORE_THRESHOLD = 45.0  # Below this = "low"

    # Moat score thresholds
    WAVE_4_MOAT_THRESHOLD = 75.0  # Companies with moat > 75 are Wave 4 candidates
    STRONG_MOAT = 60.0
    MEDIUM_MOAT = 40.0

    # Confidence thresholds
    HIGH_CONFIDENCE = 0.75
    MEDIUM_CONFIDENCE = 0.50

    # Correlation thresholds
    LOW_CORRELATION = 0.40  # Below this = mispriced opportunity
    HIGH_DEPENDENCY = 0.70  # Above this = strong second-order play


class TimingParameters:
    """Timing windows for catalyst prediction"""

    # Average days from event to event
    IPO_FILING_TO_PRICING = 150  # days (120-180 range)
    SERIES_D_TO_EXIT = 540  # days (18 months)
    PATENT_TO_PRODUCT = 270  # days (6-12 months)
    CFO_HIRE_TO_IPO = 270  # days (9 months)

    # Probability decay functions
    CONFIDENCE_DECAY_RATE = 0.95  # per month


class RiskParameters:
    """Risk management configuration"""

    # Position sizing limits
    MAX_POSITION_SIZE = 0.05  # 5% per play
    MIN_POSITION_SIZE = 0.01  # 1% minimum

    # Correlation limits
    MAX_PORTFOLIO_CORRELATION = 0.70

    # Stop losses
    PUBLIC_STOP_LOSS = 0.15  # 15% for public equities
    PRIVATE_STOP_LOSS = 0.30  # 30% for private positions

    # Liquidity requirements
    MIN_DAILY_VOLUME = 10_000_000  # $10M minimum for public plays


class DataSources:
    """Data source configuration (for future API integration)"""

    SOURCES = {
        "sec_edgar": {
            "enabled": True,
            "url": "https://www.sec.gov/cgi-bin/browse-edgar",
            "rate_limit": 10,  # requests per second
        },
        "crunchbase": {
            "enabled": True,
            "url": "https://api.crunchbase.com/v4",
            "rate_limit": 5,
        },
        "uspto": {
            "enabled": True,
            "url": "https://developer.uspto.gov",
            "rate_limit": 1,
        },
        "linkedin": {
            "enabled": False,  # Requires enterprise API
            "url": "https://api.linkedin.com/v2",
            "rate_limit": 100,
        },
    }


class SectorDefinitions:
    """Sector-specific parameters and bottleneck definitions"""

    SECTORS = {
        "AI_Infra": {
            "bottlenecks": ["GPU shortage", "inference latency", "training cost"],
            "chokepoint_type": "Compute rail",
            "moat_potential": "High",
            "capex_intensity": "Very High",
        },
        "Data_Infra": {
            "bottlenecks": [
                "fragmented pipelines",
                "transformation cost",
                "data governance",
            ],
            "chokepoint_type": "Data flow rail",
            "moat_potential": "Medium",
            "capex_intensity": "Low",
        },
        "Semiconductors": {
            "bottlenecks": ["Moore's Law limits", "power efficiency", "fab costs"],
            "chokepoint_type": "Hardware rail",
            "moat_potential": "Very High",
            "capex_intensity": "Extreme",
        },
        "Cybersecurity": {
            "bottlenecks": [
                "breach fatigue",
                "zero-trust adoption",
                "identity sprawl",
            ],
            "chokepoint_type": "Trust rail",
            "moat_potential": "High",
            "capex_intensity": "Low",
        },
        "Quantum": {
            "bottlenecks": [
                "error correction",
                "qubit stability",
                "scaling challenges",
            ],
            "chokepoint_type": "Future compute rail",
            "moat_potential": "Very High",
            "capex_intensity": "Extreme",
        },
        "6G": {
            "bottlenecks": [
                "bandwidth bottlenecks",
                "rural connectivity",
                "latency limits",
            ],
            "chokepoint_type": "Network rail",
            "moat_potential": "Very High",
            "capex_intensity": "Very High",
        },
        "Green_Energy": {
            "bottlenecks": [
                "grid stability",
                "renewable intermittency",
                "storage cost",
            ],
            "chokepoint_type": "Energy rail",
            "moat_potential": "High",
            "capex_intensity": "Very High",
        },
        "Biotech_Infra": {
            "bottlenecks": [
                "drug discovery cost",
                "clinical trial inefficiency",
                "data integration",
            ],
            "chokepoint_type": "Bio compute rail",
            "moat_potential": "Medium",
            "capex_intensity": "Medium",
        },
    }


class AlertTriggers:
    """Alert system trigger conditions"""

    TRIGGERS = {
        "momentum_breakthrough": {
            "condition": "momentum_score > 75",
            "description": "New high-conviction play identified",
        },
        "divergence_flip": {
            "condition": "divergence_flag changed",
            "description": "Hype/Build mismatch detected",
        },
        "catalyst_imminent": {
            "condition": "catalyst_date < 30 days",
            "description": "IPO filing or major event within 30 days",
        },
        "second_order_opportunity": {
            "condition": "dependency > 0.7 AND correlation < 0.4",
            "description": "Mispriced second-order exposure identified",
        },
        "moat_expansion": {
            "condition": "moat_score increased > 10 points",
            "description": "Competitive position strengthening",
        },
    }


class VisualizationConfig:
    """Configuration for dashboards and visualizations"""

    # Color schemes for heatmaps
    MOMENTUM_COLORS = {
        "high": "#00ff00",  # Green
        "medium": "#ffff00",  # Yellow
        "low": "#ff0000",  # Red
    }

    # Wave progression colors
    WAVE_COLORS = {
        "Wave1": "#1f77b4",  # Blue
        "Wave2": "#ff7f0e",  # Orange
        "Wave3": "#2ca02c",  # Green
        "Wave4": "#d62728",  # Red
    }


# Export configuration instance
class Config:
    """Master configuration object"""

    scoring = ScoringWeights()
    thresholds = Thresholds()
    timing = TimingParameters()
    risk = RiskParameters()
    data_sources = DataSources()
    sectors = SectorDefinitions()
    alerts = AlertTriggers()
    visualization = VisualizationConfig()
