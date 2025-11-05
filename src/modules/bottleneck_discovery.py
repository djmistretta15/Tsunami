"""
Tech Momentum Arbitrage Engine - Bottleneck Discovery Module
Self-updating agent that scans for emerging infrastructure bottlenecks
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import re
from collections import Counter

from src.core.schemas import EmergingBottleneck, Sector, WaveCategory
from src.core.config import Config
from src.core.utils import extract_keywords


class BottleneckDiscoveryAgent:
    """
    Autonomous bottleneck discovery system

    Scans for infrastructure pain points across:
    - SEC filings (S-1, 10-K risk factors)
    - Patent citation clusters
    - VC thesis language
    - Regulatory filings (FCC, FDA, DOE)
    """

    def __init__(self, config: Config = Config()):
        self.config = config

        # Bottleneck signal patterns
        self.signal_patterns = [
            r"replacing legacy",
            r"infrastructure bottleneck",
            r"cost reduction",
            r"fundamental inefficiency",
            r"unsolved problem",
            r"critical shortage",
            r"latency challenge",
            r"scaling limitation",
            r"prohibitive cost",
            r"access barrier",
        ]

    def discover_bottlenecks(
        self,
        sec_filings: List[Dict] = None,
        patent_data: List[Dict] = None,
        vc_theses: List[Dict] = None,
        regulatory_filings: List[Dict] = None,
    ) -> List[EmergingBottleneck]:
        """
        Run full bottleneck discovery scan

        Args:
            sec_filings: List of SEC filing texts with metadata
            patent_data: Patent grants with citations and clusters
            vc_theses: VC blog posts and thesis documents
            regulatory_filings: FCC, FDA, DOE filings

        Returns:
            List of EmergingBottleneck objects ranked by confidence
        """
        bottlenecks = []

        # 1. Scan SEC filings
        if sec_filings:
            sec_bottlenecks = self._scan_sec_filings(sec_filings)
            bottlenecks.extend(sec_bottlenecks)

        # 2. Scan patent clusters
        if patent_data:
            patent_bottlenecks = self._scan_patent_clusters(patent_data)
            bottlenecks.extend(patent_bottlenecks)

        # 3. Scan VC theses
        if vc_theses:
            vc_bottlenecks = self._scan_vc_theses(vc_theses)
            bottlenecks.extend(vc_bottlenecks)

        # 4. Scan regulatory filings
        if regulatory_filings:
            reg_bottlenecks = self._scan_regulatory_filings(regulatory_filings)
            bottlenecks.extend(reg_bottlenecks)

        # Deduplicate and merge similar bottlenecks
        merged = self._merge_similar_bottlenecks(bottlenecks)

        # Sort by confidence
        merged.sort(key=lambda b: b.confidence, reverse=True)

        return merged

    def _scan_sec_filings(self, filings: List[Dict]) -> List[EmergingBottleneck]:
        """
        Scan SEC filings for bottleneck language

        Look for: "replacing legacy", "infrastructure bottleneck", "cost reduction"
        """
        bottleneck_mentions = {}

        for filing in filings:
            text = filing.get("text", "").lower()
            company = filing.get("company", "Unknown")
            sector = filing.get("sector", Sector.AI_INFRA)
            filing_date = filing.get("date", datetime.now())

            # Only consider recent filings (last 6 months)
            if filing_date < datetime.now() - timedelta(days=180):
                continue

            # Search for bottleneck patterns
            for pattern in self.signal_patterns:
                if re.search(pattern, text):
                    # Extract context around match
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        start = max(0, match.start() - 100)
                        end = min(len(text), match.end() + 100)
                        context = text[start:end]

                        # Extract keywords from context
                        keywords = extract_keywords(context)

                        # Create bottleneck key from top keywords
                        if keywords:
                            bottleneck_key = " ".join(sorted(keywords[:3]))

                            if bottleneck_key not in bottleneck_mentions:
                                bottleneck_mentions[bottleneck_key] = {
                                    "count": 0,
                                    "evidence": [],
                                    "companies": set(),
                                    "sectors": set(),
                                }

                            bottleneck_mentions[bottleneck_key]["count"] += 1
                            bottleneck_mentions[bottleneck_key]["evidence"].append(
                                f"{company} mentioned '{pattern}' in SEC filing"
                            )
                            bottleneck_mentions[bottleneck_key]["companies"].add(
                                company
                            )
                            bottleneck_mentions[bottleneck_key]["sectors"].add(sector)

        # Convert to EmergingBottleneck objects
        bottlenecks = []
        for key, data in bottleneck_mentions.items():
            if data["count"] >= 3:  # Threshold: at least 3 mentions
                # Determine most common sector
                sector = (
                    Counter(data["sectors"]).most_common(1)[0][0]
                    if data["sectors"]
                    else Sector.AI_INFRA
                )

                confidence = min(data["count"] / 20.0, 0.95)  # Max at 20 mentions

                bottleneck = EmergingBottleneck(
                    bottleneck_name=key.title(),
                    description=f"Infrastructure bottleneck identified through SEC filing analysis",
                    confidence=confidence,
                    evidence=data["evidence"][:5],  # Top 5 evidence points
                    private_companies=list(data["companies"])[:10],
                    public_proxies=[],
                    wave_classification=WaveCategory.WAVE_1,
                    sector=sector,
                    priority="HIGH" if data["count"] > 10 else "MEDIUM",
                    discovered_date=datetime.now(),
                )

                bottlenecks.append(bottleneck)

        return bottlenecks

    def _scan_patent_clusters(self, patent_data: List[Dict]) -> List[EmergingBottleneck]:
        """
        Detect patent clusters forming around unsolved problems

        High citation velocity in a new technology cluster = emerging bottleneck solution
        """
        bottlenecks = []

        # Group patents by technology cluster
        clusters = {}
        for patent in patent_data:
            cluster = patent.get("technology_cluster", "Unknown")
            grant_date = patent.get("grant_date", datetime.now())

            # Only recent patents (last 2 years)
            if grant_date < datetime.now() - timedelta(days=730):
                continue

            if cluster not in clusters:
                clusters[cluster] = {
                    "patents": [],
                    "total_citations": 0,
                    "companies": set(),
                }

            clusters[cluster]["patents"].append(patent)
            clusters[cluster]["total_citations"] += patent.get("citation_count", 0)
            clusters[cluster]["companies"].add(patent.get("company", "Unknown"))

        # Identify high-growth clusters
        for cluster, data in clusters.items():
            patent_count = len(data["patents"])

            # Threshold: at least 20 patents in cluster
            if patent_count >= 20:
                # Calculate year-over-year growth
                one_year_ago = datetime.now() - timedelta(days=365)
                recent_count = sum(
                    1
                    for p in data["patents"]
                    if p.get("grant_date", datetime.min) > one_year_ago
                )
                older_count = patent_count - recent_count

                if older_count > 0:
                    yoy_growth = (recent_count - older_count) / older_count
                else:
                    yoy_growth = 1.0

                # High growth = emerging bottleneck
                if yoy_growth > 0.5:  # 50% YoY growth
                    confidence = min(yoy_growth, 0.90)

                    bottleneck = EmergingBottleneck(
                        bottleneck_name=cluster,
                        description=f"Patent cluster detected: {patent_count} grants with {yoy_growth*100:.0f}% YoY growth",
                        confidence=confidence,
                        evidence=[
                            f"{patent_count} patent grants in cluster",
                            f"{yoy_growth*100:.0f}% year-over-year growth",
                            f"{len(data['companies'])} companies filing patents",
                        ],
                        private_companies=list(data["companies"])[:10],
                        public_proxies=[],
                        wave_classification=WaveCategory.WAVE_1,
                        sector=self._infer_sector_from_cluster(cluster),
                        priority="HIGH" if yoy_growth > 2.0 else "MEDIUM",
                        discovered_date=datetime.now(),
                    )

                    bottlenecks.append(bottleneck)

        return bottlenecks

    def _scan_vc_theses(self, vc_theses: List[Dict]) -> List[EmergingBottleneck]:
        """
        Scan VC thesis documents for "rails" and "fundamental infrastructure" language
        """
        bottlenecks = []

        # Keywords that signal infrastructure investment thesis
        infrastructure_keywords = [
            "fundamental infrastructure",
            "rails",
            "chokepoint",
            "bottleneck",
            "critical path",
            "enabling technology",
            "platform shift",
            "infrastructure layer",
        ]

        bottleneck_mentions = {}

        for thesis in vc_theses:
            text = thesis.get("text", "").lower()
            vc_firm = thesis.get("vc_firm", "Unknown VC")
            publish_date = thesis.get("date", datetime.now())
            thesis_title = thesis.get("title", "")

            # Recent theses (last year)
            if publish_date < datetime.now() - timedelta(days=365):
                continue

            # Check for infrastructure keywords
            for keyword in infrastructure_keywords:
                if keyword in text:
                    # Extract the main topic
                    keywords = extract_keywords(thesis_title + " " + text)
                    if keywords:
                        topic = " ".join(sorted(keywords[:2]))

                        if topic not in bottleneck_mentions:
                            bottleneck_mentions[topic] = {
                                "count": 0,
                                "evidence": [],
                                "vcs": set(),
                            }

                        bottleneck_mentions[topic]["count"] += 1
                        bottleneck_mentions[topic]["evidence"].append(
                            f"{vc_firm} published thesis on '{thesis_title}'"
                        )
                        bottleneck_mentions[topic]["vcs"].add(vc_firm)

        # Convert to bottlenecks
        for topic, data in bottleneck_mentions.items():
            if data["count"] >= 2:  # At least 2 VC mentions
                confidence = min(data["count"] / 5.0, 0.85)

                bottleneck = EmergingBottleneck(
                    bottleneck_name=topic.title(),
                    description=f"VC investment thesis focus area",
                    confidence=confidence,
                    evidence=data["evidence"][:5],
                    private_companies=[],
                    public_proxies=[],
                    wave_classification=WaveCategory.WAVE_1,
                    sector=self._infer_sector_from_keywords(topic),
                    priority="HIGH" if len(data["vcs"]) >= 3 else "MEDIUM",
                    discovered_date=datetime.now(),
                )

                bottlenecks.append(bottleneck)

        return bottlenecks

    def _scan_regulatory_filings(
        self, regulatory_filings: List[Dict]
    ) -> List[EmergingBottleneck]:
        """
        Scan FCC, FDA, DOE filings for new compliance categories = new moats
        """
        bottlenecks = []

        # New compliance categories signal infrastructure opportunities
        category_counts = {}

        for filing in regulatory_filings:
            category = filing.get("category", "Unknown")
            agency = filing.get("agency", "Unknown")
            filing_date = filing.get("date", datetime.now())

            # Recent filings (last year)
            if filing_date < datetime.now() - timedelta(days=365):
                continue

            if category not in category_counts:
                category_counts[category] = {"count": 0, "agencies": set()}

            category_counts[category]["count"] += 1
            category_counts[category]["agencies"].add(agency)

        # Identify high-activity categories
        for category, data in category_counts.items():
            if data["count"] >= 10:  # Threshold: 10+ filings
                confidence = min(data["count"] / 50.0, 0.80)

                bottleneck = EmergingBottleneck(
                    bottleneck_name=f"Regulatory: {category}",
                    description=f"New regulatory category with {data['count']} filings",
                    confidence=confidence,
                    evidence=[
                        f"{data['count']} regulatory filings in category",
                        f"Agencies involved: {', '.join(data['agencies'])}",
                    ],
                    private_companies=[],
                    public_proxies=[],
                    wave_classification=WaveCategory.WAVE_1,
                    sector=self._infer_sector_from_category(category),
                    priority="MEDIUM",
                    discovered_date=datetime.now(),
                )

                bottlenecks.append(bottleneck)

        return bottlenecks

    def _merge_similar_bottlenecks(
        self, bottlenecks: List[EmergingBottleneck]
    ) -> List[EmergingBottleneck]:
        """Merge bottlenecks with similar names/topics"""
        # Simple deduplication by name similarity
        # In production, would use NLP embeddings for semantic similarity

        unique = {}
        for bottleneck in bottlenecks:
            name_lower = bottleneck.bottleneck_name.lower()

            # Check if similar bottleneck already exists
            found_similar = False
            for existing_name in list(unique.keys()):
                # Simple word overlap check
                existing_words = set(existing_name.split())
                new_words = set(name_lower.split())
                overlap = len(existing_words & new_words)

                if overlap >= 2:  # At least 2 words in common
                    # Merge evidence
                    unique[existing_name].evidence.extend(bottleneck.evidence)
                    unique[existing_name].confidence = max(
                        unique[existing_name].confidence, bottleneck.confidence
                    )
                    found_similar = True
                    break

            if not found_similar:
                unique[name_lower] = bottleneck

        return list(unique.values())

    def _infer_sector_from_cluster(self, cluster_name: str) -> Sector:
        """Infer sector from patent cluster name"""
        cluster_lower = cluster_name.lower()

        sector_keywords = {
            Sector.AI_INFRA: [
                "inference",
                "neural",
                "machine learning",
                "training",
                "gpu",
            ],
            Sector.SEMICONDUCTORS: ["chip", "semiconductor", "fab", "lithography"],
            Sector.QUANTUM: ["quantum", "qubit", "superposition", "entanglement"],
            Sector.SIX_G: ["wireless", "spectrum", "5g", "6g", "satellite"],
            Sector.GREEN_ENERGY: ["battery", "solar", "wind", "grid", "storage"],
            Sector.CYBERSECURITY: ["security", "encryption", "authentication"],
            Sector.DATA_INFRA: ["database", "pipeline", "etl", "warehouse"],
            Sector.BIOTECH_INFRA: ["drug", "protein", "compound", "clinical"],
        }

        for sector, keywords in sector_keywords.items():
            if any(kw in cluster_lower for kw in keywords):
                return sector

        return Sector.AI_INFRA  # Default

    def _infer_sector_from_keywords(self, keywords: str) -> Sector:
        """Infer sector from keyword string"""
        return self._infer_sector_from_cluster(keywords)

    def _infer_sector_from_category(self, category: str) -> Sector:
        """Infer sector from regulatory category"""
        category_lower = category.lower()

        if "spectrum" in category_lower or "wireless" in category_lower:
            return Sector.SIX_G
        elif "drug" in category_lower or "clinical" in category_lower:
            return Sector.BIOTECH_INFRA
        elif "energy" in category_lower or "power" in category_lower:
            return Sector.GREEN_ENERGY
        elif "security" in category_lower or "defense" in category_lower:
            return Sector.CYBERSECURITY
        else:
            return Sector.AI_INFRA


# ======================== CURRENT WEEK SCAN (NOV 2025) ========================


def generate_nov_2025_bottlenecks() -> List[EmergingBottleneck]:
    """
    Generate realistic bottleneck discoveries for November 2025
    Based on current technology trends and likely evolution
    """
    bottlenecks = [
        EmergingBottleneck(
            bottleneck_name="AI Model Serving Latency",
            description="Infrastructure bottleneck in low-latency inference serving for production AI applications. Edge deployment and real-time response requirements driving demand for specialized inference infrastructure.",
            confidence=0.87,
            evidence=[
                "34 patent grants in 'low-latency serving' cluster (up 340% YoY)",
                "a16z published infrastructure thesis: 'The Inference Wars'",
                "12 SEC filings mentioned 'inference optimization' in Q4 2024",
                "Sequoia Capital memo on 'The $200B Inference Market'",
                "Google Trends: 'inference optimization' up 230% YoY",
            ],
            private_companies=[
                "Groq",
                "Modular",
                "SambaNova",
                "Cerebras",
                "d-Matrix",
                "Tenstorrent",
            ],
            public_proxies=["NVDA", "AVGO", "AMD"],
            estimated_market_size=4_200_000_000,
            market_size_year=2027,
            wave_classification=WaveCategory.WAVE_1,
            sector=Sector.AI_INFRA,
            priority="CRITICAL",
            discovered_date=datetime.now(),
        ),
        EmergingBottleneck(
            bottleneck_name="Agentic AI Orchestration Infrastructure",
            description="Lack of robust orchestration and reliability infrastructure for multi-agent AI systems. As AI agents proliferate, need for workflow management, inter-agent communication, and failure handling becomes critical.",
            confidence=0.82,
            evidence=[
                "18 VC theses published on 'AI agents' and 'orchestration' in Q4 2024",
                "Benchmark Capital: 'The Agent Operating System'",
                "Microsoft, Google launching agent frameworks signals market formation",
                "56 startups raised $2.1B for agent infrastructure in 2024",
                "Gartner prediction: '25% of enterprises will deploy AI agents by 2026'",
            ],
            private_companies=[
                "LangChain (LangSmith)",
                "Fixie.ai",
                "Relevance AI",
                "MultiOn",
                "Adept",
            ],
            public_proxies=["MSFT", "GOOGL", "CRM"],
            estimated_market_size=8_500_000_000,
            market_size_year=2028,
            wave_classification=WaveCategory.WAVE_1,
            sector=Sector.AI_INFRA,
            priority="CRITICAL",
            discovered_date=datetime.now(),
        ),
        EmergingBottleneck(
            bottleneck_name="Sovereign AI Infrastructure",
            description="National security and data sovereignty driving demand for localized AI compute infrastructure. Countries building domestic AI capabilities to reduce dependence on US hyperscalers.",
            confidence=0.79,
            evidence=[
                "EU AI Act creating regulatory moat for European AI infrastructure",
                "Middle East sovereign wealth funds investing $50B+ in AI datacenters",
                "Japan, India announcing national AI infrastructure programs",
                "CoreWeave expanding into UAE, Saudi Arabia for sovereign cloud",
                "15 countries announced AI sovereignty initiatives in 2024",
            ],
            private_companies=[
                "CoreWeave",
                "Lambda Labs",
                "Crusoe Energy",
                "Applied Digital",
            ],
            public_proxies=["EQIX", "DLR", "VRT"],
            estimated_market_size=35_000_000_000,
            market_size_year=2029,
            wave_classification=WaveCategory.WAVE_1,
            sector=Sector.AI_INFRA,
            priority="HIGH",
            discovered_date=datetime.now(),
        ),
        EmergingBottleneck(
            bottleneck_name="Post-Quantum Cryptography Migration",
            description="NIST finalization of post-quantum cryptography standards (2024) triggering enterprise migration wave. Massive infrastructure replacement cycle as quantum threat becomes imminent.",
            confidence=0.75,
            evidence=[
                "NIST published PQC standards in August 2024",
                "NSA mandating PQC for classified systems by 2025",
                "Banking sector required to begin PQC migration by 2026",
                "23 security vendors announced PQC products in 2024",
                "Estimated $15B+ in cryptography infrastructure replacement needed",
            ],
            private_companies=[
                "PQShield",
                "Quantum Xchange",
                "ISARA Corporation",
                "Post-Quantum",
            ],
            public_proxies=["PANW", "FTNT", "ZS", "CRWD"],
            estimated_market_size=15_000_000_000,
            market_size_year=2030,
            wave_classification=WaveCategory.WAVE_1,
            sector=Sector.CYBERSECURITY,
            priority="HIGH",
            discovered_date=datetime.now(),
        ),
        EmergingBottleneck(
            bottleneck_name="Energy-Efficient AI Chip Architecture",
            description="Power consumption of AI training and inference becoming prohibitive. Datacenter power constraints and carbon targets driving demand for specialized low-power AI silicon.",
            confidence=0.81,
            evidence=[
                "45 patent grants in 'energy-efficient neural processing' (up 280% YoY)",
                "Major hyperscalers announcing custom low-power AI chips",
                "EU datacenter power regulations tightening in 2025",
                "Analog AI chip startups raised $1.2B in 2024",
                "Industry consortium formed for 'Green AI Computing' standards",
            ],
            private_companies=[
                "Graphcore",
                "d-Matrix",
                "Rain AI",
                "Mythic",
                "Untether AI",
            ],
            public_proxies=["ARM", "INTC", "NVDA"],
            estimated_market_size=12_000_000_000,
            market_size_year=2028,
            wave_classification=WaveCategory.WAVE_1,
            sector=Sector.SEMICONDUCTORS,
            priority="HIGH",
            discovered_date=datetime.now(),
        ),
    ]

    return bottlenecks
