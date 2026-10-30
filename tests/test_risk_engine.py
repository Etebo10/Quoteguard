from app.rules.risk_engine import (
    analyze_quote_risks,
    detect_margin_risk,
)


def test_critical_margin():

    result = detect_margin_risk(0.08)

    assert result is not None
    assert result.severity == "CRITICAL"
    assert result.risk_type == "LOW_MARGIN"


def test_healthy_margin():

    result = detect_margin_risk(0.30)

    assert result is None


def test_combined_risks():

    results = analyze_quote_risks(
        expected_margin=0.12,
        estimation_variance=0.20,
    )

    assert len(results) == 2