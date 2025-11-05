"""
Tech Momentum Arbitrage Engine - Core Data Schemas
Defines the canonical data structures for the entire system
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class Sector(str, Enum):
    """Technology sector classifications"""
    AI_INFRA = "AI_Infra"
    DATA_INFRA = "Data_Infra"
    SEMICONDUCTORS = "Semiconductors"
    CYBERSECURITY = "Cybersecurity"
    QUANTUM = "Quantum"
    SIX_G = "6G"
    GREEN_ENERGY = "Green_Energy"
    BIOTECH_INFRA = "Biotech_Infra"


class WaveCategory(str, Enum):
    """Wave progression stages"""
    WAVE_1 = "Wave1"  # REPLACE
    WAVE_2 = "Wave2"  # ARBITRAGE
    WAVE_3 = "Wave3"  # EMBED
    WAVE_4 = "Wave4"  # OWN


class DivergenceFlag(str, Enum):
    """Momentum divergence classifications"""
    CONFIRMED_MOMENTUM = "CONFIRMED_MOMENTUM"  # High Hype + High Build
    MISPRICED_OPPORTUNITY = "MISPRICED_OPPORTUNITY"  # Low Hype + High Build
    BUBBLE_RISK = "BUBBLE_RISK"  # High Hype + Low Build
    NO_SIGNAL = "NO_SIGNAL"  # Low Hype + Low Build


class TradeRecommendation(str, Enum):
    """Trade signal recommendations"""
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    SHORT = "SHORT"
    FADE = "FADE"


class FundingRound(BaseModel):
    """Individual funding round data"""
    date: datetime
    amount: float  # USD
    lead_investor: str
    valuation: Optional[float] = None
    round_type: str  # Seed, Series A, B, C, etc.


class PatentGrant(BaseModel):
    """Patent grant information"""
    grant_date: datetime
    patent_id: str
    title: str
    citation_count: int
    technology_cluster: str
    forward_citations: int = 0


class ExecutiveHire(BaseModel):
    """Key executive hire tracking"""
    date: datetime
    role: str
    name: str
    previous_company: str
    is_ipo_signal: bool = False  # CFO/CCO hires


class PublicProxy(BaseModel):
    """Public market exposure proxy"""
    ticker: str
    exposure_type: str
    correlation_score: float
    revenue_exposure_pct: Optional[float] = None


class Company(BaseModel):
    """Core company entity schema"""
    company_id: str
    name: str
    sector: Sector
    wave_category: WaveCategory
    bottleneck_solved: str

    # Funding data
    funding_rounds: List[FundingRound] = []
    total_funding: float = 0.0
    last_valuation: Optional[float] = None

    # Innovation signals
    patent_grants: List[PatentGrant] = []
    patent_count: int = 0

    # Talent signals
    executive_hires: List[ExecutiveHire] = []
    employee_count: int = 0
    engineer_pct: float = 0.0
    faang_talent_pct: float = 0.0

    # Market presence
    public_proxies: List[PublicProxy] = []
    fortune_500_customers: int = 0
    estimated_arr: Optional[float] = None

    # Timing signals
    ipo_probability_6mo: float = 0.0
    ipo_probability_12mo: float = 0.0
    expected_ipo_date: Optional[datetime] = None

    # Metadata
    founded_date: datetime
    headquarters: str
    website: str
    last_updated: datetime = Field(default_factory=datetime.now)


class MomentumScore(BaseModel):
    """Dual-track momentum scoring output"""
    company_id: str
    company_name: str

    # Track A: Narrative Momentum (Hype)
    media_velocity: float  # 0-100
    social_signal: float  # 0-100
    vc_buzz: float  # 0-100
    conference_presence: float  # 0-100
    search_trends: float  # 0-100
    hype_score: float  # Weighted composite

    # Track B: Execution Momentum (Build)
    revenue_indicators: float  # 0-100
    customer_logos: float  # 0-100
    patent_velocity: float  # 0-100
    talent_density: float  # 0-100
    product_milestones: float  # 0-100
    build_score: float  # Weighted composite

    # Composite & divergence
    momentum_score: float  # (Hype * 0.4) + (Build * 0.6)
    momentum_change_7d: float
    momentum_change_30d: float
    divergence_flag: DivergenceFlag

    timestamp: datetime = Field(default_factory=datetime.now)


class MoatScore(BaseModel):
    """Competitive moat analysis"""
    company_id: str
    company_name: str

    # Five moat dimensions
    regulatory_moat: float  # 0-100
    network_effects: float  # 0-100
    capital_intensity: float  # 0-100
    data_moat: float  # 0-100
    switching_costs: float  # 0-100

    # Weighted composite (regulatory 30%, network 25%, capital 20%, data 15%, switching 10%)
    total_moat_score: float

    # Wave classification based on moat
    wave_potential: WaveCategory
    durability_rating: str  # Low, Medium, High, Very High

    timestamp: datetime = Field(default_factory=datetime.now)


class Catalyst(BaseModel):
    """Timing catalyst for investable events"""
    catalyst_type: str  # IPO_FILING, PRODUCT_LAUNCH, REGULATORY_APPROVAL, etc.
    estimated_date: datetime
    confidence: float  # 0-1
    probability_6mo: float
    probability_12mo: float
    leading_indicators: List[str]
    risk_factors: List[str]


class EmergingBottleneck(BaseModel):
    """Bottleneck discovery output"""
    bottleneck_name: str
    description: str
    confidence: float
    evidence: List[str]

    # Investable proxies
    private_companies: List[str]
    public_proxies: List[str]

    # Market sizing
    estimated_market_size: Optional[float] = None
    market_size_year: Optional[int] = None

    # Classification
    wave_classification: WaveCategory
    sector: Sector
    priority: str  # LOW, MEDIUM, HIGH, CRITICAL

    discovered_date: datetime = Field(default_factory=datetime.now)


class SecondOrderPlay(BaseModel):
    """Second-order arbitrage opportunity"""
    primary_technology: str
    primary_momentum_score: float

    supplier_company: str
    supplier_ticker: Optional[str] = None
    exposure_type: str
    dependency_score: float  # 0-1
    price_correlation: float  # -1 to 1

    thesis: str
    entry_timing: str
    risk_adjusted_return: str  # Low, Medium, High

    timestamp: datetime = Field(default_factory=datetime.now)


class TradeSignal(BaseModel):
    """Generated trade signal with full analysis"""
    rank: int
    company: str
    company_id: str
    sector: Sector

    # Momentum metrics
    momentum_score: float
    momentum_change_7d: float
    hype_score: float
    build_score: float
    moat_score: float

    # Exposure routes
    public_proxy: Optional[str] = None
    pre_ipo_access: Optional[str] = None
    synthetic_exposure: Optional[str] = None

    # Trade mechanics
    recommendation: TradeRecommendation
    conviction: float  # 0-1
    position_size: str  # e.g., "3-5% portfolio"
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None

    # Timing & catalysts
    next_catalyst: Optional[str] = None
    catalyst_date: Optional[datetime] = None
    entry_timing: str

    # Risk assessment
    risk_factors: List[str]
    expected_return: Optional[str] = None
    time_horizon: str

    generated_date: datetime = Field(default_factory=datetime.now)


class WeeklyAlphaReport(BaseModel):
    """Comprehensive weekly intelligence report"""
    report_date: datetime

    top_10_momentum_plays: List[TradeSignal]
    emerging_bottlenecks: List[EmergingBottleneck]
    second_order_plays: List[SecondOrderPlay]

    # Portfolio actions
    portfolio_rebalance_actions: List[Dict[str, Any]]

    # Market context
    ipo_window_health: str
    macro_conditions: Dict[str, Any]

    # Performance metrics
    signals_generated: int
    high_conviction_count: int
    average_momentum_score: float


class BacktestResult(BaseModel):
    """Historical backtest performance"""
    start_date: datetime
    end_date: datetime

    # Performance metrics
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    alpha_vs_qqq: float
    win_rate: float

    # Signal accuracy
    ipo_prediction_accuracy: float
    momentum_signal_accuracy: float

    # Top performers
    best_signals: List[Dict[str, Any]]
    worst_signals: List[Dict[str, Any]]

    # Validation
    validation_date: datetime = Field(default_factory=datetime.now)
