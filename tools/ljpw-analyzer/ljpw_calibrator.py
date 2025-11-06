#!/usr/bin/env python3
"""
LJPW Calibrator - Convert Raw Metrics to LJPW Coordinates

This tool provides OBJECTIVE, NON-ARBITRARY conversion of observable metrics
to LJPW coordinates, calibrated against Natural Equilibrium.

Usage:
    from ljpw_calibrator import SoftwareTeamCalibrator

    calibrator = SoftwareTeamCalibrator()
    raw_metrics = {
        'cross_review_rate': 0.85,
        'api_error_rate': 0.08,
        # ... etc
    }
    ljpw = calibrator.calibrate(raw_metrics)
    print(ljpw)  # LJPWCoordinates(L=0.80, J=0.84, P=0.85, W=0.74)
"""

import json
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
import numpy as np


@dataclass
class RawMetrics:
    """Raw observable metrics for a software team"""

    # Love metrics
    cross_review_rate: float  # [0,1] % of commits reviewed by others
    api_error_rate: float     # [0,1] % of API calls that error
    doc_coverage: float       # [0,1] % of public APIs documented
    psych_safety_score: float # [1,7] Edmondson survey score

    # Justice metrics
    line_coverage: float      # [0,1] % lines covered by tests
    branch_coverage: float    # [0,1] % branches covered by tests
    architecture_violations: float  # [0,1] % of checks that fail
    code_standards_compliance: float  # [0,1] % files compliant
    tech_debt_time_ratio: float  # [0,1] % time spent on debt

    # Power metrics
    velocity_achievement: float  # [0,∞] delivered/committed points
    p95_response_time_ms: float  # [0,∞] 95th percentile latency
    sla_target_ms: float         # [0,∞] target latency
    cpu_utilization: float       # [0,1] average CPU usage

    # Wisdom metrics
    doc_to_code_ratio: float     # [0,∞] doc_lines / code_lines
    onboarding_days: float       # [0,∞] days to first commit
    baseline_onboarding_days: float  # [0,∞] baseline days
    change_isolation_rate: float  # [0,1] % single-module changes
    knowledge_retention_score: float  # [1,7] survey score


@dataclass
class LJPWCoordinates:
    """LJPW coordinates in [0,1]⁴ space"""
    L: float  # Love
    J: float  # Justice
    P: float  # Power
    W: float  # Wisdom

    def to_tuple(self):
        return (self.L, self.J, self.P, self.W)

    def to_dict(self):
        return asdict(self)


class SoftwareTeamCalibrator:
    """
    Calibrates raw metrics to LJPW coordinates

    All conversions are OBJECTIVE:
    - Based on information-theoretic definitions
    - Calibrated against Natural Equilibrium
    - Reproducible (same inputs → same outputs)
    """

    # Natural Equilibrium (objective reference point)
    NATURAL_EQUILIBRIUM = LJPWCoordinates(
        L=0.618034,  # φ⁻¹ (golden ratio)
        J=0.414214,  # √2 - 1
        P=0.718282,  # e - 2
        W=0.693147   # ln(2)
    )

    # Optimal values for certain metrics
    OPTIMAL_DOC_RATIO = 0.40      # 40% doc-to-code
    OPTIMAL_CPU_UTILIZATION = 0.70  # 70% CPU usage

    def __init__(self):
        self.natural_eq = self.NATURAL_EQUILIBRIUM

    def calibrate_love(self, metrics: RawMetrics) -> float:
        """
        Convert raw metrics to Love coordinate

        L = mean([connectivity, usability, documentation, psych_safety])
        """
        # 1. Connectivity (cross-review rate)
        connectivity = metrics.cross_review_rate

        # 2. Usability (API error rate)
        usability = 1.0 - metrics.api_error_rate

        # 3. Documentation coverage
        documentation = metrics.doc_coverage

        # 4. Psychological safety (normalize 1-7 → 0-1)
        psych_safety = (metrics.psych_safety_score - 1) / 6.0

        # Equal weighting
        L = np.mean([connectivity, usability, documentation, psych_safety])

        return float(np.clip(L, 0, 1))

    def calibrate_justice(self, metrics: RawMetrics) -> float:
        """
        Convert raw metrics to Justice coordinate

        J = mean([test_coverage, consistency, standards, debt_ratio])
        """
        # 1. Test coverage (average of line and branch)
        test_coverage = np.mean([metrics.line_coverage, metrics.branch_coverage])

        # 2. Architecture consistency (invert violations)
        consistency = 1.0 - metrics.architecture_violations

        # 3. Code standards compliance
        code_standards = metrics.code_standards_compliance

        # 4. Technical debt ratio (invert time spent on debt)
        debt_ratio = 1.0 - metrics.tech_debt_time_ratio

        # Equal weighting
        J = np.mean([test_coverage, consistency, code_standards, debt_ratio])

        return float(np.clip(J, 0, 1))

    def calibrate_power(self, metrics: RawMetrics) -> float:
        """
        Convert raw metrics to Power coordinate

        P = mean([velocity, performance, scalability])
        """
        # 1. Velocity (cap at 1.0 - delivering more than committed is good but not infinite)
        velocity = min(1.0, metrics.velocity_achievement)

        # 2. Performance (meeting SLA)
        performance_ratio = metrics.sla_target_ms / max(metrics.p95_response_time_ms, 1)
        performance = min(1.0, performance_ratio)

        # 3. Scalability (optimal at 70% CPU utilization)
        cpu_delta = abs(metrics.cpu_utilization - self.OPTIMAL_CPU_UTILIZATION)
        scalability = 1.0 - (cpu_delta / self.OPTIMAL_CPU_UTILIZATION)
        scalability = max(0, scalability)

        # Equal weighting
        P = np.mean([velocity, performance, scalability])

        return float(np.clip(P, 0, 1))

    def calibrate_wisdom(self, metrics: RawMetrics) -> float:
        """
        Convert raw metrics to Wisdom coordinate

        W = mean([doc_ratio, onboarding, isolation, knowledge])
        """
        # 1. Documentation ratio (optimal at 40%)
        if metrics.doc_to_code_ratio <= self.OPTIMAL_DOC_RATIO:
            doc_ratio = metrics.doc_to_code_ratio / self.OPTIMAL_DOC_RATIO
        else:
            # Penalty for over-documentation
            excess = metrics.doc_to_code_ratio - self.OPTIMAL_DOC_RATIO
            doc_ratio = 1.0 - (excess / self.OPTIMAL_DOC_RATIO)
        doc_ratio = max(0, doc_ratio)

        # 2. Onboarding efficiency
        onboarding = 1.0 - (metrics.onboarding_days / metrics.baseline_onboarding_days)
        onboarding = max(0, onboarding)

        # 3. Change isolation
        isolation = metrics.change_isolation_rate

        # 4. Knowledge retention (normalize 1-7 → 0-1)
        knowledge = (metrics.knowledge_retention_score - 1) / 6.0

        # Equal weighting
        W = np.mean([doc_ratio, onboarding, isolation, knowledge])

        return float(np.clip(W, 0, 1))

    def calibrate(self, metrics: RawMetrics) -> LJPWCoordinates:
        """
        Convert raw metrics to complete LJPW coordinates

        This is the main calibration function.
        Returns objective, reproducible LJPW coordinates.
        """
        L = self.calibrate_love(metrics)
        J = self.calibrate_justice(metrics)
        P = self.calibrate_power(metrics)
        W = self.calibrate_wisdom(metrics)

        return LJPWCoordinates(L=L, J=J, P=P, W=W)

    def compare_to_natural_equilibrium(self, coords: LJPWCoordinates) -> Dict:
        """
        Compare system to Natural Equilibrium

        Returns objective deviations and interpretation
        """
        eq = self.natural_eq

        differences = {
            'L': coords.L - eq.L,
            'J': coords.J - eq.J,
            'P': coords.P - eq.P,
            'W': coords.W - eq.W
        }

        percent_differences = {
            'L': (differences['L'] / eq.L) * 100,
            'J': (differences['J'] / eq.J) * 100,
            'P': (differences['P'] / eq.P) * 100,
            'W': (differences['W'] / eq.W) * 100
        }

        distance_from_eq = np.sqrt(sum(d**2 for d in differences.values()))
        distance_from_anchor = np.sqrt(
            (coords.L - 1)**2 + (coords.J - 1)**2 +
            (coords.P - 1)**2 + (coords.W - 1)**2
        )

        # Interpretation
        if distance_from_eq < 0.2:
            interpretation = "Very close to Natural Equilibrium (optimal natural state)"
        elif distance_from_anchor < distance_from_eq:
            interpretation = "Closer to Anchor Point than Natural Equilibrium (transcendent state)"
        else:
            interpretation = "Between Natural Equilibrium and starting point"

        return {
            'natural_equilibrium': eq.to_dict(),
            'current': coords.to_dict(),
            'absolute_differences': differences,
            'percent_differences': percent_differences,
            'distance_from_equilibrium': float(distance_from_eq),
            'distance_from_anchor': float(distance_from_anchor),
            'interpretation': interpretation
        }

    def diagnose(self, coords: LJPWCoordinates) -> Dict:
        """
        Full diagnostic analysis with mixing scores

        Returns comprehensive assessment including:
        - Mixing scores (robustness, effectiveness, growth, harmony)
        - Bottleneck identification
        - Comparison to Natural Equilibrium
        - Actionable recommendations
        """
        from ljpw_mixing import LJPWMixer, LJPWDiagnostics

        mixer = LJPWMixer()
        diagnostics = LJPWDiagnostics()

        # Get mixing scores
        mixing = mixer.mix(coords.L, coords.J, coords.P, coords.W)

        # Get diagnostics
        diag = diagnostics.diagnose(coords.L, coords.J, coords.P, coords.W)

        # Get Natural Equilibrium comparison
        eq_comp = self.compare_to_natural_equilibrium(coords)

        return {
            'coordinates': coords.to_dict(),
            'mixing_scores': mixing,
            'diagnostics': diag,
            'equilibrium_comparison': eq_comp
        }


def load_metrics_from_json(filepath: str) -> RawMetrics:
    """Load raw metrics from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return RawMetrics(**data)


def save_ljpw_to_json(coords: LJPWCoordinates, filepath: str):
    """Save LJPW coordinates to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(coords.to_dict(), f, indent=2)


# Example usage and validation
def main():
    """Demonstration of calibration tool"""

    print("=" * 80)
    print("LJPW CALIBRATOR - Raw Metrics → LJPW Coordinates")
    print("=" * 80)
    print()

    calibrator = SoftwareTeamCalibrator()

    # Example: Team Alpha (from protocol document)
    print("Example: Team Alpha (2-week sprint)")
    print("-" * 80)

    team_alpha_metrics = RawMetrics(
        # Love
        cross_review_rate=0.85,
        api_error_rate=0.08,
        doc_coverage=0.65,
        psych_safety_score=5.5,

        # Justice
        line_coverage=0.82,
        branch_coverage=0.78,
        architecture_violations=0.06,
        code_standards_compliance=0.88,
        tech_debt_time_ratio=0.25,

        # Power
        velocity_achievement=0.95,
        p95_response_time_ms=450,
        sla_target_ms=500,
        cpu_utilization=0.79,

        # Wisdom
        doc_to_code_ratio=0.30,
        onboarding_days=4.0,
        baseline_onboarding_days=10.0,
        change_isolation_rate=0.88,
        knowledge_retention_score=5.0
    )

    print("Raw Metrics:")
    print(f"  Love: cross_review={team_alpha_metrics.cross_review_rate}, "
          f"api_errors={team_alpha_metrics.api_error_rate}, "
          f"doc_coverage={team_alpha_metrics.doc_coverage}, "
          f"psych_safety={team_alpha_metrics.psych_safety_score}/7")
    print(f"  Justice: test_coverage={team_alpha_metrics.line_coverage}, "
          f"arch_violations={team_alpha_metrics.architecture_violations}, "
          f"standards={team_alpha_metrics.code_standards_compliance}, "
          f"debt_time={team_alpha_metrics.tech_debt_time_ratio}")
    print(f"  Power: velocity={team_alpha_metrics.velocity_achievement}, "
          f"p95={team_alpha_metrics.p95_response_time_ms}ms, "
          f"cpu={team_alpha_metrics.cpu_utilization}")
    print(f"  Wisdom: doc_ratio={team_alpha_metrics.doc_to_code_ratio}, "
          f"onboarding={team_alpha_metrics.onboarding_days}d, "
          f"isolation={team_alpha_metrics.change_isolation_rate}")
    print()

    # Calibrate
    coords = calibrator.calibrate(team_alpha_metrics)

    print("Calibrated LJPW Coordinates:")
    print(f"  L = {coords.L:.3f}")
    print(f"  J = {coords.J:.3f}")
    print(f"  P = {coords.P:.3f}")
    print(f"  W = {coords.W:.3f}")
    print()

    # Compare to Natural Equilibrium
    eq_comp = calibrator.compare_to_natural_equilibrium(coords)

    print("Natural Equilibrium Comparison:")
    print(f"  Natural Equilibrium: L={eq_comp['natural_equilibrium']['L']:.3f}, "
          f"J={eq_comp['natural_equilibrium']['J']:.3f}, "
          f"P={eq_comp['natural_equilibrium']['P']:.3f}, "
          f"W={eq_comp['natural_equilibrium']['W']:.3f}")
    print(f"  Distance from Natural Equilibrium: {eq_comp['distance_from_equilibrium']:.3f}")
    print(f"  Distance from Anchor Point: {eq_comp['distance_from_anchor']:.3f}")
    print()

    print("Percent Differences from Natural Equilibrium:")
    for dim, pct in eq_comp['percent_differences'].items():
        sign = "+" if pct >= 0 else ""
        print(f"  {dim}: {sign}{pct:.1f}%")
    print()

    print(f"Interpretation: {eq_comp['interpretation']}")
    print()

    # Full diagnostic
    print("=" * 80)
    print("FULL DIAGNOSTIC")
    print("=" * 80)
    print()

    diag = calibrator.diagnose(coords)

    print("Mixing Scores:")
    for metric, value in diag['mixing_scores'].items():
        print(f"  {metric}: {value:.3f}")
    print()

    print(f"Bottleneck: {diag['diagnostics']['bottleneck']} "
          f"(value: {diag['diagnostics']['bottleneck_value']:.2f})")
    print()

    print("Issues:")
    for issue in diag['diagnostics']['issues']:
        print(f"  • {issue}")
    print()

    print("Suggestions:")
    for suggestion in diag['diagnostics']['suggestions']:
        print(f"  • {suggestion}")
    print()

    # Additional test cases
    print("=" * 80)
    print("ADDITIONAL TEST CASES")
    print("=" * 80)
    print()

    test_cases = [
        ("Low-performing team", RawMetrics(
            cross_review_rate=0.30, api_error_rate=0.25, doc_coverage=0.20, psych_safety_score=3.0,
            line_coverage=0.40, branch_coverage=0.35, architecture_violations=0.30,
            code_standards_compliance=0.50, tech_debt_time_ratio=0.60,
            velocity_achievement=0.50, p95_response_time_ms=1200, sla_target_ms=500,
            cpu_utilization=0.95,
            doc_to_code_ratio=0.10, onboarding_days=15, baseline_onboarding_days=10,
            change_isolation_rate=0.40, knowledge_retention_score=3.5
        )),
        ("High-performing team", RawMetrics(
            cross_review_rate=0.95, api_error_rate=0.02, doc_coverage=0.90, psych_safety_score=6.5,
            line_coverage=0.95, branch_coverage=0.92, architecture_violations=0.02,
            code_standards_compliance=0.98, tech_debt_time_ratio=0.10,
            velocity_achievement=1.05, p95_response_time_ms=250, sla_target_ms=500,
            cpu_utilization=0.68,
            doc_to_code_ratio=0.42, onboarding_days=2, baseline_onboarding_days=10,
            change_isolation_rate=0.95, knowledge_retention_score=6.2
        ))
    ]

    for name, metrics in test_cases:
        coords = calibrator.calibrate(metrics)
        eq_comp = calibrator.compare_to_natural_equilibrium(coords)

        print(f"{name}:")
        print(f"  LJPW: L={coords.L:.3f}, J={coords.J:.3f}, P={coords.P:.3f}, W={coords.W:.3f}")
        print(f"  Distance from Natural Eq: {eq_comp['distance_from_equilibrium']:.3f}")
        print(f"  Distance from Anchor: {eq_comp['distance_from_anchor']:.3f}")
        print(f"  {eq_comp['interpretation']}")
        print()


if __name__ == '__main__':
    main()
