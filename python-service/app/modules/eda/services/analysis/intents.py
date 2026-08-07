from enum import Enum


class Intent(str, Enum):
    OVERVIEW = "overview"
    RELATIONSHIP = "relationship"
    COMPARISON = "comparison"
    TREND = "trend"
    DISTRIBUTION = "distribution"
    RANKING = "ranking"
    COMPOSITION = "composition"
    DIAGNOSTIC = "diagnostic"
    SEGMENTATION = "segmentation"
    ANOMALY = "anomaly"
    PREDICTION = "prediction"
    WHAT_IF = "what_if"
    RECOMMENDATION = "recommendation"
    EXPLAIN = "explain"