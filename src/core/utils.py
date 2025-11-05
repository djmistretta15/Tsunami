"""
Tech Momentum Arbitrage Engine - Utility Functions
Helper functions for data processing, normalization, and calculations
"""

import re
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import math


def generate_company_id(company_name: str) -> str:
    """Generate deterministic UUID from company name"""
    return hashlib.sha256(company_name.encode()).hexdigest()[:16]


def normalize_company_name(name: str) -> str:
    """Normalize company name for matching"""
    # Remove common suffixes
    suffixes = [
        " Inc",
        " Inc.",
        " LLC",
        " Ltd",
        " Ltd.",
        " Corporation",
        " Corp",
        " Corp.",
    ]
    normalized = name.strip()
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)]
    return normalized.strip()


def calculate_growth_rate(
    values: List[float], periods: List[datetime]
) -> Optional[float]:
    """Calculate compound growth rate from time series"""
    if len(values) < 2 or len(periods) < 2:
        return None

    start_value = values[0]
    end_value = values[-1]
    start_date = periods[0]
    end_date = periods[-1]

    if start_value <= 0:
        return None

    years = (end_date - start_date).days / 365.25
    if years <= 0:
        return None

    cagr = (pow(end_value / start_value, 1 / years) - 1) * 100
    return round(cagr, 2)


def moving_average(values: List[float], window: int = 30) -> float:
    """Calculate simple moving average"""
    if not values or len(values) < window:
        return sum(values) / len(values) if values else 0.0

    recent = values[-window:]
    return sum(recent) / len(recent)


def exponential_moving_average(values: List[float], span: int = 30) -> float:
    """Calculate exponential moving average"""
    if not values:
        return 0.0

    alpha = 2 / (span + 1)
    ema = values[0]

    for value in values[1:]:
        ema = alpha * value + (1 - alpha) * ema

    return ema


def normalize_score(
    value: float, min_val: float, max_val: float, scale: int = 100
) -> float:
    """Normalize a value to 0-scale range"""
    if max_val == min_val:
        return 0.0

    normalized = ((value - min_val) / (max_val - min_val)) * scale
    return max(0, min(scale, normalized))


def sigmoid(x: float, midpoint: float = 0, steepness: float = 1) -> float:
    """Sigmoid function for smooth threshold mapping"""
    return 1 / (1 + math.exp(-steepness * (x - midpoint)))


def calculate_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient"""
    if len(x) != len(y) or len(x) < 2:
        return 0.0

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(
        sum((x[i] - mean_x) ** 2 for i in range(n))
        * sum((y[i] - mean_y) ** 2 for i in range(n))
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


def days_until(target_date: datetime) -> int:
    """Calculate days from now until target date"""
    return (target_date - datetime.now()).days


def probability_decay(
    initial_prob: float, days_elapsed: int, half_life_days: int = 90
) -> float:
    """Apply exponential decay to probability over time"""
    decay_rate = math.log(2) / half_life_days
    return initial_prob * math.exp(-decay_rate * days_elapsed)


def weighted_score(components: Dict[str, float], weights: Dict[str, float]) -> float:
    """Calculate weighted composite score"""
    total = 0.0
    for key, value in components.items():
        if key in weights:
            total += value * weights[key]
    return round(total, 2)


def detect_outliers(values: List[float], threshold: float = 2.0) -> List[int]:
    """Detect outlier indices using z-score method"""
    if len(values) < 3:
        return []

    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return []

    outliers = []
    for i, value in enumerate(values):
        z_score = abs((value - mean) / std_dev)
        if z_score > threshold:
            outliers.append(i)

    return outliers


def extract_keywords(text: str, min_length: int = 4) -> List[str]:
    """Extract keywords from text (simple word tokenization)"""
    # Remove special characters and split
    words = re.findall(r"\b[a-zA-Z]{" + str(min_length) + r",}\b", text.lower())

    # Remove common stop words
    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "been",
        "will",
        "their",
        "what",
        "which",
        "when",
        "where",
        "about",
    }

    keywords = [word for word in words if word not in stop_words]
    return keywords


def calculate_momentum_change(
    current_score: float, previous_score: float
) -> float:
    """Calculate momentum change percentage"""
    if previous_score == 0:
        return 0.0
    return round(((current_score - previous_score) / previous_score) * 100, 2)


def sharpe_ratio(
    returns: List[float], risk_free_rate: float = 0.04, periods_per_year: int = 252
) -> float:
    """Calculate Sharpe ratio for return series"""
    if len(returns) < 2:
        return 0.0

    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return 0.0

    # Annualize
    annualized_return = mean_return * periods_per_year
    annualized_volatility = std_dev * math.sqrt(periods_per_year)

    return (annualized_return - risk_free_rate) / annualized_volatility


def max_drawdown(values: List[float]) -> float:
    """Calculate maximum drawdown from peak"""
    if not values:
        return 0.0

    peak = values[0]
    max_dd = 0.0

    for value in values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak if peak > 0 else 0
        if drawdown > max_dd:
            max_dd = drawdown

    return round(max_dd * 100, 2)  # Return as percentage


def format_currency(amount: float, decimals: int = 0) -> str:
    """Format large currency amounts with K/M/B suffixes"""
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.{decimals}f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.{decimals}f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.{decimals}f}K"
    else:
        return f"${amount:.{decimals}f}"


def calculate_position_size(
    conviction: float,
    risk_level: str,
    base_size: float = 0.02,
    max_size: float = 0.05,
) -> str:
    """Calculate recommended position size based on conviction and risk"""
    # Adjust for conviction (0-1 scale)
    adjusted_size = base_size + (conviction * (max_size - base_size))

    # Adjust for risk
    risk_multipliers = {"Low": 1.0, "Medium": 0.8, "High": 0.6, "Very High": 0.4}

    final_size = adjusted_size * risk_multipliers.get(risk_level, 0.8)

    # Format as percentage range
    lower = max(0.01, final_size - 0.01)
    upper = min(max_size, final_size + 0.01)

    return f"{lower*100:.0f}-{upper*100:.0f}% portfolio"


def time_to_catalyst(days: int) -> str:
    """Convert days to human-readable time estimate"""
    if days < 0:
        return "Past due"
    elif days < 30:
        return f"{days} days"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''}"
    else:
        years = days / 365
        return f"{years:.1f} year{'s' if years >= 2 else ''}"


def confidence_level(score: float) -> str:
    """Convert confidence score to qualitative level"""
    if score >= 0.85:
        return "Very High"
    elif score >= 0.70:
        return "High"
    elif score >= 0.50:
        return "Medium"
    elif score >= 0.30:
        return "Low"
    else:
        return "Very Low"
