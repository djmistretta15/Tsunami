"""
Tech Momentum Arbitrage Engine - Second-Order Arbitrage Module
Identifies suppliers to the suppliers - mispriced exposure to Wave 1 tech
"""

from datetime import datetime
from typing import List, Dict, Tuple
from src.core.schemas import SecondOrderPlay, Sector, MomentumScore
from src.core.config import Config


class SecondOrderArbitrageEngine:
    """
    Find second and third-order plays on technology momentum

    If AI Infra heats up → Cooling systems, power infrastructure
    If 6G momentum builds → RF components, fiber optics
    If Quantum scales → Dilution refrigerators, control systems
    """

    def __init__(self, config: Config = Config()):
        self.config = config

        # Dependency mapping: Primary tech → Supplier categories
        self.dependency_map = {
            Sector.AI_INFRA: [
                {
                    "category": "Datacenter Cooling",
                    "suppliers": [
                        {"name": "Vertiv (VRT)", "ticker": "VRT", "dependency": 0.87},
                        {"name": "nVent Electric (NVT)", "ticker": "NVT", "dependency": 0.72},
                    ],
                    "thesis": "AI datacenter buildout requires 3x cooling capacity for GPU clusters",
                },
                {
                    "category": "Power Infrastructure",
                    "suppliers": [
                        {"name": "Eaton (ETN)", "ticker": "ETN", "dependency": 0.78},
                        {"name": "Schneider Electric (SBGSY)", "ticker": "SBGSY", "dependency": 0.75},
                    ],
                    "thesis": "AI compute demands robust UPS and power distribution systems",
                },
                {
                    "category": "Networking Equipment",
                    "suppliers": [
                        {"name": "Arista Networks (ANET)", "ticker": "ANET", "dependency": 0.91},
                        {"name": "Juniper Networks (JNPR)", "ticker": "JNPR", "dependency": 0.68},
                    ],
                    "thesis": "GPU cluster interconnects require high-bandwidth networking",
                },
            ],
            Sector.SIX_G: [
                {
                    "category": "RF Components",
                    "suppliers": [
                        {"name": "Qorvo (QRVO)", "ticker": "QRVO", "dependency": 0.85},
                        {"name": "Skyworks Solutions (SWKS)", "ticker": "SWKS", "dependency": 0.82},
                    ],
                    "thesis": "6G and satellite mesh require advanced RF filtering and amplification",
                },
                {
                    "category": "Fiber Optics",
                    "suppliers": [
                        {"name": "Corning (GLW)", "ticker": "GLW", "dependency": 0.79},
                        {"name": "Lumentum (LITE)", "ticker": "LITE", "dependency": 0.71},
                    ],
                    "thesis": "Backhaul infrastructure for 6G requires massive fiber deployment",
                },
            ],
            Sector.QUANTUM: [
                {
                    "category": "Cryogenic Systems",
                    "suppliers": [
                        {"name": "BlueFors (Private)", "ticker": None, "dependency": 0.92},
                        {"name": "Oxford Instruments (OXIG.L)", "ticker": "OXIG.L", "dependency": 0.73},
                    ],
                    "thesis": "Quantum computers require dilution refrigerators at millikelvin temperatures",
                },
                {
                    "category": "Control Electronics",
                    "suppliers": [
                        {"name": "Keysight (KEYS)", "ticker": "KEYS", "dependency": 0.68},
                        {"name": "Zurich Instruments (Private)", "ticker": None, "dependency": 0.84},
                    ],
                    "thesis": "Quantum systems need precision control and measurement electronics",
                },
            ],
            Sector.GREEN_ENERGY: [
                {
                    "category": "Rare Earth Mining",
                    "suppliers": [
                        {"name": "MP Materials (MP)", "ticker": "MP", "dependency": 0.81},
                        {"name": "Lynas Rare Earths (LYSDY)", "ticker": "LYSDY", "dependency": 0.76},
                    ],
                    "thesis": "Wind turbines and EV motors require neodymium and dysprosium",
                },
                {
                    "category": "Grid Storage Components",
                    "suppliers": [
                        {"name": "Fluence Energy (FLNC)", "ticker": "FLNC", "dependency": 0.88},
                        {"name": "Enphase Energy (ENPH)", "ticker": "ENPH", "dependency": 0.79},
                    ],
                    "thesis": "Renewable intermittency drives massive battery storage deployment",
                },
            ],
            Sector.SEMICONDUCTORS: [
                {
                    "category": "Semiconductor Equipment",
                    "suppliers": [
                        {"name": "ASML (ASML)", "ticker": "ASML", "dependency": 0.95},
                        {"name": "Applied Materials (AMAT)", "ticker": "AMAT", "dependency": 0.91},
                        {"name": "Lam Research (LRCX)", "ticker": "LRCX", "dependency": 0.89},
                    ],
                    "thesis": "Chip fab buildout requires advanced lithography and deposition tools",
                },
                {
                    "category": "Materials & Chemicals",
                    "suppliers": [
                        {"name": "Entegris (ENTG)", "ticker": "ENTG", "dependency": 0.84},
                        {"name": "Cabot Microelectronics (CCMP)", "ticker": "CCMP", "dependency": 0.77},
                    ],
                    "thesis": "Advanced nodes require specialized chemicals and materials",
                },
            ],
            Sector.CYBERSECURITY: [
                {
                    "category": "Identity Infrastructure",
                    "suppliers": [
                        {"name": "Okta (OKTA)", "ticker": "OKTA", "dependency": 0.72},
                        {"name": "Ping Identity (PING)", "ticker": "PING", "dependency": 0.68},
                    ],
                    "thesis": "Zero-trust architectures built on identity as perimeter",
                },
            ],
            Sector.DATA_INFRA: [
                {
                    "category": "Cloud Storage",
                    "suppliers": [
                        {"name": "Pure Storage (PSTG)", "ticker": "PSTG", "dependency": 0.76},
                        {"name": "NetApp (NTAP)", "ticker": "NTAP", "dependency": 0.71},
                    ],
                    "thesis": "Data infrastructure growth drives storage infrastructure demand",
                },
            ],
        }

    def find_second_order_plays(
        self,
        momentum_scores: List[MomentumScore],
        price_correlations: Dict[str, float] = None,
    ) -> List[SecondOrderPlay]:
        """
        Identify second-order arbitrage opportunities

        Args:
            momentum_scores: Momentum scores for primary technologies
            price_correlations: Historical price correlations (ticker -> correlation)

        Returns:
            List of SecondOrderPlay objects
        """
        price_correlations = price_correlations or {}
        plays = []

        # Identify high-momentum primary technologies
        high_momentum = [s for s in momentum_scores if s.momentum_score > 70]

        for momentum_score in high_momentum:
            # Find sector dependencies
            sector = self._infer_sector(momentum_score.company_name)

            if sector in self.dependency_map:
                dependencies = self.dependency_map[sector]

                for dep_category in dependencies:
                    for supplier in dep_category["suppliers"]:
                        if not supplier["ticker"]:
                            continue  # Skip private companies

                        # Get price correlation (if available)
                        ticker = supplier["ticker"]
                        correlation = price_correlations.get(ticker, 0.50)  # Default 0.50

                        # Opportunity if HIGH dependency but LOW correlation
                        is_mispriced = (
                            supplier["dependency"] > self.config.thresholds.HIGH_DEPENDENCY
                            and correlation < self.config.thresholds.LOW_CORRELATION
                        )

                        if is_mispriced:
                            entry_timing = "Immediate"
                            risk_return = "High"
                        else:
                            entry_timing = "Monitor"
                            risk_return = "Medium"

                        play = SecondOrderPlay(
                            primary_technology=momentum_score.company_name,
                            primary_momentum_score=momentum_score.momentum_score,
                            supplier_company=supplier["name"],
                            supplier_ticker=ticker,
                            exposure_type=dep_category["category"],
                            dependency_score=supplier["dependency"],
                            price_correlation=correlation,
                            thesis=dep_category["thesis"],
                            entry_timing=entry_timing,
                            risk_adjusted_return=risk_return,
                            timestamp=datetime.now(),
                        )

                        plays.append(play)

        # Sort by opportunity quality (high dependency, low correlation)
        plays.sort(
            key=lambda p: p.dependency_score - p.price_correlation, reverse=True
        )

        return plays

    def _infer_sector(self, company_name: str) -> Sector:
        """Infer sector from company name (simplified)"""
        # In production, would look up from company database
        name_lower = company_name.lower()

        if any(
            kw in name_lower for kw in ["ai", "gpu", "inference", "training", "cerebras", "groq"]
        ):
            return Sector.AI_INFRA
        elif any(kw in name_lower for kw in ["satellite", "6g", "wireless", "ast"]):
            return Sector.SIX_G
        elif any(kw in name_lower for kw in ["quantum", "ionq", "rigetti"]):
            return Sector.QUANTUM
        elif any(kw in name_lower for kw in ["energy", "battery", "solar", "form"]):
            return Sector.GREEN_ENERGY
        elif any(kw in name_lower for kw in ["chip", "semiconductor", "tenstorrent"]):
            return Sector.SEMICONDUCTORS
        elif any(kw in name_lower for kw in ["security", "cyber", "wiz"]):
            return Sector.CYBERSECURITY
        elif any(kw in name_lower for kw in ["data", "databricks", "fivetran"]):
            return Sector.DATA_INFRA
        else:
            return Sector.AI_INFRA  # Default

    def get_top_plays(self, plays: List[SecondOrderPlay], n: int = 10) -> List[SecondOrderPlay]:
        """Get top N second-order plays"""
        return plays[:n]

    def filter_immediate_entry(self, plays: List[SecondOrderPlay]) -> List[SecondOrderPlay]:
        """Filter for immediate entry opportunities"""
        return [p for p in plays if p.entry_timing == "Immediate"]


# ======================== GENERATE MOCK CORRELATIONS ========================


def generate_mock_correlations() -> Dict[str, float]:
    """
    Generate realistic price correlations for demonstration
    In production, would calculate from historical price data
    """
    return {
        # AI Infrastructure suppliers (varied correlations)
        "VRT": 0.34,  # Vertiv - LOW correlation (opportunity!)
        "NVT": 0.42,  # nVent - LOW correlation
        "ETN": 0.51,  # Eaton - MEDIUM
        "SBGSY": 0.48,  # Schneider - MEDIUM
        "ANET": 0.78,  # Arista - HIGH (already priced in)
        "JNPR": 0.45,  # Juniper - MEDIUM
        # 6G suppliers
        "QRVO": 0.38,  # Qorvo - LOW correlation (opportunity!)
        "SWKS": 0.41,  # Skyworks - LOW
        "GLW": 0.52,  # Corning - MEDIUM
        "LITE": 0.47,  # Lumentum - MEDIUM
        # Quantum suppliers
        "OXIG.L": 0.29,  # Oxford Instruments - VERY LOW (opportunity!)
        "KEYS": 0.43,  # Keysight - LOW
        # Green Energy suppliers
        "MP": 0.58,  # MP Materials - MEDIUM
        "LYSDY": 0.52,  # Lynas - MEDIUM
        "FLNC": 0.71,  # Fluence - HIGH
        "ENPH": 0.69,  # Enphase - HIGH
        # Semiconductor equipment (high correlation, already priced)
        "ASML": 0.82,  # ASML - HIGH
        "AMAT": 0.79,  # Applied Materials - HIGH
        "LRCX": 0.81,  # Lam Research - HIGH
        "ENTG": 0.64,  # Entegris - MEDIUM-HIGH
        "CCMP": 0.59,  # Cabot Micro - MEDIUM
        # Cybersecurity
        "OKTA": 0.67,  # Okta - MEDIUM-HIGH
        "PING": 0.62,  # Ping - MEDIUM-HIGH
        # Data Infra
        "PSTG": 0.55,  # Pure Storage - MEDIUM
        "NTAP": 0.58,  # NetApp - MEDIUM
    }
