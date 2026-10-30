from dataclasses import dataclass


@dataclass
class RiskFinding:
    risk_type: str
    severity: str
    message: str
    recommendation: str


def detect_margin_risk(
    expected_margin: float,
) -> RiskFinding | None:

    if expected_margin < 0.10:
        return RiskFinding(
            risk_type="LOW_MARGIN",
            severity="CRITICAL",
            message=(
                "The expected profit margin is below 10%."
            ),
            recommendation=(
                "Review the selling price or reduce costs "
                "before sending the quote."
            ),
        )

    if expected_margin < 0.15:
        return RiskFinding(
            risk_type="LOW_MARGIN",
            severity="HIGH",
            message=(
                "The expected profit margin is below 15%."
            ),
            recommendation=(
                "Consider increasing the quoted price "
                "or reviewing the cost assumptions."
            ),
        )

    if expected_margin < 0.20:
        return RiskFinding(
            risk_type="LOW_MARGIN",
            severity="MEDIUM",
            message=(
                "The expected profit margin is below 20%."
            ),
            recommendation=(
                "Review whether the margin provides "
                "enough protection against unexpected costs."
            ),
        )

    return None


def detect_cost_overrun_risk(
    estimation_variance: float,
) -> RiskFinding | None:

    if estimation_variance >= 0.25:
        return RiskFinding(
            risk_type="HIGH_COST_OVERRUN",
            severity="CRITICAL",
            message=(
                "Historical jobs show cost overruns of "
                "25% or more."
            ),
            recommendation=(
                "Increase the contingency allowance and "
                "review the cost assumptions."
            ),
        )

    if estimation_variance >= 0.15:
        return RiskFinding(
            risk_type="HIGH_COST_OVERRUN",
            severity="HIGH",
            message=(
                "Historical jobs show significant "
                "cost overruns."
            ),
            recommendation=(
                "Consider increasing contingency before "
                "finalizing the quote."
            ),
        )

    if estimation_variance >= 0.10:
        return RiskFinding(
            risk_type="COST_OVERRUN",
            severity="MEDIUM",
            message=(
                "Historical jobs show moderate cost overruns."
            ),
            recommendation=(
                "Review previous job costs before sending "
                "the quote."
            ),
        )

    return None


def analyze_quote_risks(
    expected_margin: float,
    estimation_variance: float,
) -> list[RiskFinding]:

    findings = []

    margin_risk = detect_margin_risk(
        expected_margin
    )

    if margin_risk:
        findings.append(margin_risk)

    cost_risk = detect_cost_overrun_risk(
        estimation_variance
    )

    if cost_risk:
        findings.append(cost_risk)

    return findings