"""
Generate 50 realistic companies across all sectors for Tech Momentum Arbitrage Engine
"""

from datetime import datetime, timedelta
from typing import List
import json
import random

from src.core.schemas import (
    Company,
    Sector,
    WaveCategory,
    FundingRound,
    PatentGrant,
    ExecutiveHire,
    PublicProxy,
)
from src.core.utils import generate_company_id


def generate_50_companies() -> List[Company]:
    """Generate 50 realistic companies across all sectors"""

    companies = []

    # ==================== AI INFRASTRUCTURE (12 companies) ====================

    companies.append(
        Company(
            company_id=generate_company_id("CoreWeave"),
            name="CoreWeave",
            sector=Sector.AI_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="GPU shortage for AI training and inference",
            funding_rounds=[
                FundingRound(
                    date=datetime(2023, 4, 15),
                    amount=421_000_000,
                    lead_investor="Magnetar Capital",
                    valuation=2_000_000_000,
                    round_type="Series C",
                ),
                FundingRound(
                    date=datetime(2024, 5, 20),
                    amount=1_100_000_000,
                    lead_investor="Coatue",
                    valuation=19_000_000_000,
                    round_type="Series C Extension",
                ),
            ],
            total_funding=2_300_000_000,
            last_valuation=19_000_000_000,
            patent_grants=[
                PatentGrant(
                    grant_date=datetime(2024, 3, 10),
                    patent_id="US11234567",
                    title="GPU cluster orchestration system",
                    citation_count=12,
                    technology_cluster="Cloud GPU Infrastructure",
                ),
            ],
            patent_count=8,
            executive_hires=[
                ExecutiveHire(
                    date=datetime(2024, 8, 1),
                    role="Chief Financial Officer",
                    name="John Smith",
                    previous_company="AWS",
                    is_ipo_signal=True,
                ),
            ],
            employee_count=1800,
            engineer_pct=65.0,
            faang_talent_pct=28.0,
            public_proxies=[
                PublicProxy(
                    ticker="NVDA",
                    exposure_type="GPU supplier",
                    correlation_score=0.78,
                )
            ],
            fortune_500_customers=85,
            estimated_arr=750_000_000,
            ipo_probability_6mo=0.34,
            ipo_probability_12mo=0.71,
            expected_ipo_date=datetime(2026, 4, 15),
            founded_date=datetime(2017, 1, 1),
            headquarters="Roseland, NJ",
            website="https://www.coreweave.com",
        )
    )

    companies.append(
        Company(
            company_id=generate_company_id("Groq"),
            name="Groq",
            sector=Sector.AI_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="AI inference latency for real-time applications",
            funding_rounds=[
                FundingRound(
                    date=datetime(2024, 8, 5),
                    amount=640_000_000,
                    lead_investor="BlackRock",
                    valuation=2_800_000_000,
                    round_type="Series D",
                ),
            ],
            total_funding=1_064_000_000,
            last_valuation=2_800_000_000,
            patent_grants=[
                PatentGrant(
                    grant_date=datetime(2024, 1, 15),
                    patent_id="US11345678",
                    title="Low-latency tensor processing unit architecture",
                    citation_count=45,
                    technology_cluster="Inference Acceleration",
                ),
            ],
            patent_count=67,
            executive_hires=[],
            employee_count=450,
            engineer_pct=72.0,
            faang_talent_pct=42.0,
            public_proxies=[PublicProxy(ticker="NVDA", exposure_type="Competitor exposure", correlation_score=0.65)],
            fortune_500_customers=32,
            estimated_arr=85_000_000,
            ipo_probability_6mo=0.15,
            ipo_probability_12mo=0.38,
            founded_date=datetime(2016, 1, 1),
            headquarters="Mountain View, CA",
            website="https://groq.com",
        )
    )

    companies.append(
        Company(
            company_id=generate_company_id("Cerebras Systems"),
            name="Cerebras Systems",
            sector=Sector.AI_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="AI training scalability with wafer-scale integration",
            funding_rounds=[
                FundingRound(
                    date=datetime(2021, 11, 18),
                    amount=250_000_000,
                    lead_investor="Alpha Wave Ventures",
                    valuation=4_000_000_000,
                    round_type="Series F",
                ),
            ],
            total_funding=715_000_000,
            last_valuation=4_000_000_000,
            patent_grants=[
                PatentGrant(
                    grant_date=datetime(2023, 6, 20),
                    patent_id="US11456789",
                    title="Wafer-scale chip interconnect system",
                    citation_count=89,
                    technology_cluster="AI Training Hardware",
                ),
            ],
            patent_count=142,
            executive_hires=[
                ExecutiveHire(
                    date=datetime(2024, 2, 10),
                    role="Chief Commercial Officer",
                    name="Sarah Johnson",
                    previous_company="NVIDIA",
                    is_ipo_signal=True,
                ),
            ],
            employee_count=620,
            engineer_pct=68.0,
            faang_talent_pct=35.0,
            public_proxies=[PublicProxy(ticker="NVDA", exposure_type="Training hardware competitor", correlation_score=0.58)],
            fortune_500_customers=18,
            estimated_arr=125_000_000,
            ipo_probability_6mo=0.28,
            ipo_probability_12mo=0.59,
            founded_date=datetime(2016, 1, 1),
            headquarters="Sunnyvale, CA",
            website="https://cerebras.net",
        )
    )

    companies.append(
        Company(
            company_id=generate_company_id("Together AI"),
            name="Together AI",
            sector=Sector.AI_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="Decentralized GPU compute orchestration",
            funding_rounds=[
                FundingRound(
                    date=datetime(2024, 6, 12),
                    amount=106_000_000,
                    lead_investor="Kleiner Perkins",
                    valuation=1_250_000_000,
                    round_type="Series A",
                ),
            ],
            total_funding=142_500_000,
            last_valuation=1_250_000_000,
            patent_grants=[],
            patent_count=3,
            executive_hires=[],
            employee_count=180,
            engineer_pct=78.0,
            faang_talent_pct=48.0,
            public_proxies=[],
            fortune_500_customers=42,
            estimated_arr=48_000_000,
            ipo_probability_6mo=0.05,
            ipo_probability_12mo=0.18,
            founded_date=datetime(2022, 1, 1),
            headquarters="San Francisco, CA",
            website="https://together.ai",
        )
    )

    companies.append(
        Company(
            company_id=generate_company_id("Lambda Labs"),
            name="Lambda Labs",
            sector=Sector.AI_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="Accessible GPU cloud for AI researchers",
            funding_rounds=[
                FundingRound(
                    date=datetime(2023, 8, 22),
                    amount=44_000_000,
                    lead_investor="1517 Fund",
                    valuation=320_000_000,
                    round_type="Series C",
                ),
            ],
            total_funding=108_000_000,
            last_valuation=320_000_000,
            patent_grants=[],
            patent_count=2,
            executive_hires=[],
            employee_count=240,
            engineer_pct=64.0,
            faang_talent_pct=22.0,
            public_proxies=[PublicProxy(ticker="NVDA", exposure_type="GPU reseller", correlation_score=0.72)],
            fortune_500_customers=28,
            estimated_arr=95_000_000,
            ipo_probability_6mo=0.12,
            ipo_probability_12mo=0.35,
            founded_date=datetime(2012, 1, 1),
            headquarters="San Francisco, CA",
            website="https://lambdalabs.com",
        )
    )

    companies.append(
        Company(
            company_id=generate_company_id("Modular"),
            name="Modular",
            sector=Sector.AI_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="AI developer productivity and deployment simplification",
            funding_rounds=[
                FundingRound(
                    date=datetime(2024, 8, 15),
                    amount=100_000_000,
                    lead_investor="General Catalyst",
                    valuation=600_000_000,
                    round_type="Series B",
                ),
            ],
            total_funding=130_000_000,
            last_valuation=600_000_000,
            patent_grants=[],
            patent_count=5,
            executive_hires=[],
            employee_count=105,
            engineer_pct=82.0,
            faang_talent_pct=58.0,
            public_proxies=[],
            fortune_500_customers=18,
            estimated_arr=12_000_000,
            ipo_probability_6mo=0.08,
            ipo_probability_12mo=0.22,
            founded_date=datetime(2022, 1, 1),
            headquarters="Palo Alto, CA",
            website="https://modular.com",
        )
    )

    # More AI Infra companies
    for i, (name, funding, valuation, arr, customers) in enumerate([
        ("SambaNova Systems", 1_318_000_000, 5_100_000_000, 220_000_000, 35),
        ("d-Matrix", 154_000_000, 580_000_000, 18_000_000, 12),
        ("Anyscale", 259_000_000, 1_000_000_000, 45_000_000, 58),
        ("Weights & Biases", 250_000_000, 1_000_000_000, 75_000_000, 125),
        ("Fixie.ai", 17_000_000, 80_000_000, 3_000_000, 8),
        ("LangChain", 35_000_000, 200_000_000, 12_000_000, 450),
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.AI_INFRA,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"AI infrastructure bottleneck - {name.lower()} focus",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 10), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Sequoia", "a16z", "Lightspeed", "Index"]),
                        valuation=valuation,
                        round_type=random.choice(["Series B", "Series C", "Series D"]),
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[],
                patent_count=random.randint(2, 25),
                executive_hires=[],
                employee_count=random.randint(80, 800),
                engineer_pct=random.uniform(60, 80),
                faang_talent_pct=random.uniform(20, 45),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.05, 0.25),
                ipo_probability_12mo=random.uniform(0.15, 0.45),
                founded_date=datetime(random.randint(2019, 2022), 1, 1),
                headquarters=random.choice(["San Francisco, CA", "Palo Alto, CA", "Mountain View, CA"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    # ==================== DATA INFRASTRUCTURE (6 companies) ====================

    companies.append(
        Company(
            company_id=generate_company_id("Databricks"),
            name="Databricks",
            sector=Sector.DATA_INFRA,
            wave_category=WaveCategory.WAVE_2,
            bottleneck_solved="Unified data analytics and AI platform",
            funding_rounds=[
                FundingRound(
                    date=datetime(2023, 9, 14),
                    amount=500_000_000,
                    lead_investor="Counter Ventures",
                    valuation=43_000_000_000,
                    round_type="Series I",
                ),
            ],
            total_funding=4_000_000_000,
            last_valuation=43_000_000_000,
            patent_grants=[
                PatentGrant(
                    grant_date=datetime(2024, 2, 5),
                    patent_id="US11567890",
                    title="Distributed data lakehouse architecture",
                    citation_count=156,
                    technology_cluster="Data Infrastructure",
                ),
            ],
            patent_count=89,
            executive_hires=[
                ExecutiveHire(
                    date=datetime(2024, 1, 15),
                    role="Chief Financial Officer",
                    name="Dave Conte",
                    previous_company="Salesforce",
                    is_ipo_signal=True,
                ),
            ],
            employee_count=6200,
            engineer_pct=58.0,
            faang_talent_pct=32.0,
            public_proxies=[PublicProxy(ticker="SNOW", exposure_type="Data platform competitor", correlation_score=0.74)],
            fortune_500_customers=420,
            estimated_arr=2_400_000_000,
            ipo_probability_6mo=0.65,
            ipo_probability_12mo=0.88,
            expected_ipo_date=datetime(2026, 2, 1),
            founded_date=datetime(2013, 1, 1),
            headquarters="San Francisco, CA",
            website="https://databricks.com",
        )
    )

    companies.append(
        Company(
            company_id=generate_company_id("Fivetran"),
            name="Fivetran",
            sector=Sector.DATA_INFRA,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="Automated data pipeline integration",
            funding_rounds=[
                FundingRound(
                    date=datetime(2022, 10, 31),
                    amount=240_000_000,
                    lead_investor="General Atlantic",
                    valuation=5_600_000_000,
                    round_type="Series D",
                ),
            ],
            total_funding=678_000_000,
            last_valuation=5_600_000_000,
            patent_grants=[],
            patent_count=12,
            executive_hires=[],
            employee_count=1850,
            engineer_pct=55.0,
            faang_talent_pct=24.0,
            public_proxies=[],
            fortune_500_customers=165,
            estimated_arr=450_000_000,
            ipo_probability_6mo=0.42,
            ipo_probability_12mo=0.68,
            founded_date=datetime(2012, 1, 1),
            headquarters="Oakland, CA",
            website="https://fivetran.com",
        )
    )

    for i, (name, funding, valuation, arr, customers) in enumerate([
        ("dbt Labs", 582_000_000, 4_200_000_000, 325_000_000, 285),
        ("Starburst Data", 414_000_000, 3_350_000_000, 175_000_000, 145),
        ("ClickHouse", 350_000_000, 2_000_000_000, 95_000_000, 220),
        ("Airbyte", 181_000_000, 1_500_000_000, 42_000_000, 180),
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.DATA_INFRA,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Data infrastructure - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 8), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Sequoia", "Andreessen Horowitz", "Accel"]),
                        valuation=valuation,
                        round_type="Series D",
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[],
                patent_count=random.randint(5, 30),
                executive_hires=[],
                employee_count=random.randint(400, 2000),
                engineer_pct=random.uniform(50, 65),
                faang_talent_pct=random.uniform(18, 32),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.15, 0.45),
                ipo_probability_12mo=random.uniform(0.35, 0.65),
                founded_date=datetime(random.randint(2016, 2020), 1, 1),
                headquarters=random.choice(["San Francisco, CA", "New York, NY"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    # ==================== SEMICONDUCTORS (7 companies) ====================

    companies.append(
        Company(
            company_id=generate_company_id("Tenstorrent"),
            name="Tenstorrent",
            sector=Sector.SEMICONDUCTORS,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="Scalable AI chip architecture with RISC-V cores",
            funding_rounds=[
                FundingRound(
                    date=datetime(2024, 8, 20),
                    amount=693_000_000,
                    lead_investor="Samsung",
                    valuation=2_600_000_000,
                    round_type="Series D",
                ),
            ],
            total_funding=1_134_000_000,
            last_valuation=2_600_000_000,
            patent_grants=[
                PatentGrant(
                    grant_date=datetime(2024, 4, 10),
                    patent_id="US11678901",
                    title="Tensor processing with distributed RISC-V architecture",
                    citation_count=34,
                    technology_cluster="AI Chip Architecture",
                ),
            ],
            patent_count=178,
            executive_hires=[],
            employee_count=820,
            engineer_pct=76.0,
            faang_talent_pct=38.0,
            public_proxies=[PublicProxy(ticker="NVDA", exposure_type="AI chip competitor", correlation_score=0.61)],
            fortune_500_customers=24,
            estimated_arr=65_000_000,
            ipo_probability_6mo=0.18,
            ipo_probability_12mo=0.42,
            founded_date=datetime(2016, 1, 1),
            headquarters="Toronto, Canada",
            website="https://tenstorrent.com",
        )
    )

    for i, (name, funding, valuation, arr, customers, patents) in enumerate([
        ("SiFive", 680_000_000, 2_500_000_000, 120_000_000, 45, 245),
        ("Esperanto Technologies", 258_000_000, 800_000_000, 38_000_000, 18, 89),
        ("Graphcore", 710_000_000, 2_770_000_000, 85_000_000, 32, 156),
        ("Mythic AI", 165_000_000, 450_000_000, 15_000_000, 12, 67),
        ("Untether AI", 125_000_000, 350_000_000, 8_000_000, 8, 42),
        ("Rain AI", 33_000_000, 150_000_000, 2_000_000, 4, 18),
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.SEMICONDUCTORS,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Specialized chip architecture - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 9), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Intel Capital", "Qualcomm Ventures", "SoftBank"]),
                        valuation=valuation,
                        round_type=random.choice(["Series C", "Series D"]),
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[
                    PatentGrant(
                        grant_date=datetime(2024, random.randint(1, 10), random.randint(1, 28)),
                        patent_id=f"US116{random.randint(10000, 99999)}",
                        title=f"{name} chip architecture patent",
                        citation_count=random.randint(10, 80),
                        technology_cluster="AI Chips",
                    )
                ],
                patent_count=patents,
                executive_hires=[],
                employee_count=random.randint(200, 900),
                engineer_pct=random.uniform(70, 85),
                faang_talent_pct=random.uniform(25, 45),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.08, 0.25),
                ipo_probability_12mo=random.uniform(0.20, 0.48),
                founded_date=datetime(random.randint(2015, 2020), 1, 1),
                headquarters=random.choice(["Santa Clara, CA", "San Jose, CA", "Austin, TX"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    # ==================== CYBERSECURITY (6 companies) ====================

    companies.append(
        Company(
            company_id=generate_company_id("Wiz"),
            name="Wiz",
            sector=Sector.CYBERSECURITY,
            wave_category=WaveCategory.WAVE_1,
            bottleneck_solved="Cloud security posture management at scale",
            funding_rounds=[
                FundingRound(
                    date=datetime(2024, 5, 7),
                    amount=1_000_000_000,
                    lead_investor="Andreessen Horowitz",
                    valuation=12_000_000_000,
                    round_type="Series E",
                ),
            ],
            total_funding=1_900_000_000,
            last_valuation=12_000_000_000,
            patent_grants=[],
            patent_count=23,
            executive_hires=[
                ExecutiveHire(
                    date=datetime(2024, 9, 1),
                    role="Chief Financial Officer",
                    name="Dali Rajic",
                    previous_company="MongoDB",
                    is_ipo_signal=True,
                ),
            ],
            employee_count=1400,
            engineer_pct=62.0,
            faang_talent_pct=34.0,
            public_proxies=[PublicProxy(ticker="PANW", exposure_type="Cloud security competitor", correlation_score=0.68)],
            fortune_500_customers=320,
            estimated_arr=650_000_000,
            ipo_probability_6mo=0.58,
            ipo_probability_12mo=0.82,
            expected_ipo_date=datetime(2026, 3, 15),
            founded_date=datetime(2020, 1, 1),
            headquarters="New York, NY",
            website="https://wiz.io",
        )
    )

    for i, (name, funding, valuation, arr, customers) in enumerate([
        ("Rubrik", 752_000_000, 4_000_000_000, 520_000_000, 245),
        ("1Password", 920_000_000, 6_800_000_000, 425_000_000, 150000),
        ("Transmit Security", 643_000_000, 2_700_000_000, 145_000_000, 85),
        ("Lacework", 1_800_000_000, 8_300_000_000, 285_000_000, 165),
        ("Snyk", 1_010_000_000, 8_500_000_000, 380_000_000, 2400),
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.CYBERSECURITY,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Security bottleneck - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 8), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Sequoia", "Accel", "Insight Partners"]),
                        valuation=valuation,
                        round_type="Series E",
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[],
                patent_count=random.randint(10, 45),
                executive_hires=[],
                employee_count=random.randint(800, 2200),
                engineer_pct=random.uniform(55, 68),
                faang_talent_pct=random.uniform(22, 38),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.25, 0.55),
                ipo_probability_12mo=random.uniform(0.45, 0.78),
                founded_date=datetime(random.randint(2015, 2020), 1, 1),
                headquarters=random.choice(["San Francisco, CA", "Boston, MA", "Tel Aviv, Israel"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    # ==================== QUANTUM (5 companies) ====================

    for i, (name, funding, valuation, arr, customers, patents) in enumerate([
        ("IonQ", 650_000_000, 2_000_000_000, 28_000_000, 14, 142),  # Public already, but included
        ("Rigetti Computing", 320_000_000, 1_500_000_000, 18_000_000, 9, 98),  # Public
        ("PsiQuantum", 665_000_000, 3_150_000_000, 0, 0, 215),  # Pre-revenue
        ("Atom Computing", 198_000_000, 850_000_000, 8_000_000, 6, 67),
        ("QuEra Computing", 42_000_000, 180_000_000, 3_000_000, 5, 34),
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.QUANTUM,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Quantum computing scalability - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 9), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["BlackRock", "Baillie Gifford", "DCVC"]),
                        valuation=valuation,
                        round_type=random.choice(["Series C", "Series D"]),
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[
                    PatentGrant(
                        grant_date=datetime(2024, random.randint(1, 10), random.randint(1, 28)),
                        patent_id=f"US117{random.randint(10000, 99999)}",
                        title=f"{name} quantum architecture",
                        citation_count=random.randint(15, 120),
                        technology_cluster="Quantum Computing",
                    )
                ],
                patent_count=patents,
                executive_hires=[],
                employee_count=random.randint(120, 450),
                engineer_pct=random.uniform(75, 88),
                faang_talent_pct=random.uniform(28, 48),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.05, 0.22),
                ipo_probability_12mo=random.uniform(0.15, 0.42),
                founded_date=datetime(random.randint(2015, 2021), 1, 1),
                headquarters=random.choice(["Berkeley, CA", "Boston, MA", "Palo Alto, CA"]),
                website=f"https://{name.lower().replace(' ', '').replace('computing', '')}.com",
            )
        )

    # ==================== 6G / SATELLITE (5 companies) ====================

    for i, (name, funding, valuation, arr, customers, patents) in enumerate([
        ("AST SpaceMobile", 850_000_000, 2_900_000_000, 15_000_000, 8, 245),  # Public
        ("Lynk Global", 95_000_000, 380_000_000, 4_000_000, 6, 178),
        ("E-Space", 142_000_000, 650_000_000, 0, 0, 89),  # Pre-revenue satellite
        ("Rivada Space Networks", 2_400_000_000, 5_000_000_000, 0, 0, 67),  # Mega-round
        ("Omnispace", 89_000_000, 320_000_000, 5_000_000, 4, 124),
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.SIX_G,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Satellite connectivity - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 9), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Vodafone", "Rakuten", "AT&T"]),
                        valuation=valuation,
                        round_type=random.choice(["Series B", "Series C"]),
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[
                    PatentGrant(
                        grant_date=datetime(2024, random.randint(1, 10), random.randint(1, 28)),
                        patent_id=f"US118{random.randint(10000, 99999)}",
                        title=f"{name} satellite network architecture",
                        citation_count=random.randint(20, 95),
                        technology_cluster="Satellite Communications",
                    )
                ],
                patent_count=patents,
                executive_hires=[],
                employee_count=random.randint(180, 650),
                engineer_pct=random.uniform(68, 78),
                faang_talent_pct=random.uniform(18, 32),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.08, 0.28),
                ipo_probability_12mo=random.uniform(0.18, 0.48),
                founded_date=datetime(random.randint(2017, 2021), 1, 1),
                headquarters=random.choice(["Texas", "Virginia", "London, UK"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    # ==================== GREEN ENERGY (5 companies) ====================

    for i, (name, funding, valuation, arr, customers, patents) in enumerate([
        ("Form Energy", 829_000_000, 1_200_000_000, 0, 5, 156),  # Iron-air battery
        ("Antora Energy", 150_000_000, 500_000_000, 0, 3, 78),  # Thermal storage
        ("Twelve", 645_000_000, 1_400_000_000, 18_000_000, 12, 234),  # Carbon transformation
        ("ESS Inc", 320_000_000, 850_000_000, 42_000_000, 18, 89),  # Iron flow battery
        ("H2 Green Steel", 350_000_000, 1_100_000_000, 0, 0, 45),  # Green steel production
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.GREEN_ENERGY,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Green energy storage/production - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 9), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Breakthrough Energy", "BHP Ventures", "Temasek"]),
                        valuation=valuation,
                        round_type=random.choice(["Series C", "Series D"]),
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[
                    PatentGrant(
                        grant_date=datetime(2024, random.randint(1, 10), random.randint(1, 28)),
                        patent_id=f"US119{random.randint(10000, 99999)}",
                        title=f"{name} energy technology",
                        citation_count=random.randint(12, 78),
                        technology_cluster="Energy Storage",
                    )
                ],
                patent_count=patents,
                executive_hires=[],
                employee_count=random.randint(180, 550),
                engineer_pct=random.uniform(58, 72),
                faang_talent_pct=random.uniform(12, 25),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.05, 0.20),
                ipo_probability_12mo=random.uniform(0.12, 0.38),
                founded_date=datetime(random.randint(2017, 2021), 1, 1),
                headquarters=random.choice(["Massachusetts", "California", "Sweden"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    # ==================== BIOTECH INFRASTRUCTURE (4 companies) ====================

    for i, (name, funding, valuation, arr, customers) in enumerate([
        ("Recursion Pharmaceuticals", 880_000_000, 2_200_000_000, 45_000_000, 12),  # Public
        ("Benchling", 625_000_000, 6_100_000_000, 185_000_000, 850),
        ("Insitro", 643_000_000, 2_800_000_000, 0, 8),  # AI drug discovery
        ("Ginkgo Bioworks", 2_200_000_000, 3_500_000_000, 210_000_000, 45),  # Public
    ]):
        companies.append(
            Company(
                company_id=generate_company_id(name),
                name=name,
                sector=Sector.BIOTECH_INFRA,
                wave_category=WaveCategory.WAVE_1,
                bottleneck_solved=f"Biotech infrastructure - {name}",
                funding_rounds=[
                    FundingRound(
                        date=datetime(2024, random.randint(1, 8), random.randint(1, 28)),
                        amount=funding,
                        lead_investor=random.choice(["Flagship Pioneering", "a16z Bio", "Thrive Capital"]),
                        valuation=valuation,
                        round_type=random.choice(["Series D", "Series E"]),
                    )
                ],
                total_funding=funding,
                last_valuation=valuation,
                patent_grants=[],
                patent_count=random.randint(35, 145),
                executive_hires=[],
                employee_count=random.randint(350, 1200),
                engineer_pct=random.uniform(45, 62),
                faang_talent_pct=random.uniform(15, 28),
                public_proxies=[],
                fortune_500_customers=customers,
                estimated_arr=arr,
                ipo_probability_6mo=random.uniform(0.15, 0.38),
                ipo_probability_12mo=random.uniform(0.28, 0.58),
                founded_date=datetime(random.randint(2014, 2019), 1, 1),
                headquarters=random.choice(["San Francisco, CA", "Boston, MA", "South San Francisco, CA"]),
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
        )

    return companies


def save_companies_to_json(companies: List[Company], filename: str = "companies.json"):
    """Save companies to JSON file"""
    companies_dict = [
        {
            "company_id": c.company_id,
            "name": c.name,
            "sector": c.sector.value,
            "wave_category": c.wave_category.value,
            "bottleneck_solved": c.bottleneck_solved,
            "funding_rounds": [
                {
                    "date": r.date.isoformat(),
                    "amount": r.amount,
                    "lead_investor": r.lead_investor,
                    "valuation": r.valuation,
                    "round_type": r.round_type,
                }
                for r in c.funding_rounds
            ],
            "total_funding": c.total_funding,
            "last_valuation": c.last_valuation,
            "patent_grants": [
                {
                    "grant_date": p.grant_date.isoformat(),
                    "patent_id": p.patent_id,
                    "title": p.title,
                    "citation_count": p.citation_count,
                    "technology_cluster": p.technology_cluster,
                }
                for p in c.patent_grants
            ],
            "patent_count": c.patent_count,
            "executive_hires": [
                {
                    "date": e.date.isoformat(),
                    "role": e.role,
                    "name": e.name,
                    "previous_company": e.previous_company,
                    "is_ipo_signal": e.is_ipo_signal,
                }
                for e in c.executive_hires
            ],
            "employee_count": c.employee_count,
            "engineer_pct": c.engineer_pct,
            "faang_talent_pct": c.faang_talent_pct,
            "public_proxies": [
                {
                    "ticker": p.ticker,
                    "exposure_type": p.exposure_type,
                    "correlation_score": p.correlation_score,
                    "revenue_exposure_pct": p.revenue_exposure_pct,
                }
                for p in c.public_proxies
            ],
            "fortune_500_customers": c.fortune_500_customers,
            "estimated_arr": c.estimated_arr,
            "ipo_probability_6mo": c.ipo_probability_6mo,
            "ipo_probability_12mo": c.ipo_probability_12mo,
            "expected_ipo_date": c.expected_ipo_date.isoformat() if c.expected_ipo_date else None,
            "founded_date": c.founded_date.isoformat(),
            "headquarters": c.headquarters,
            "website": c.website,
        }
        for c in companies
    ]

    with open(filename, "w") as f:
        json.dump(companies_dict, f, indent=2)

    print(f"✅ Saved {len(companies)} companies to {filename}")


if __name__ == "__main__":
    companies = generate_50_companies()
    save_companies_to_json(companies, "/home/user/Tsunami/data/companies.json")
