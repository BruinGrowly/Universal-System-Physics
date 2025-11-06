#!/usr/bin/env python3
"""
LJPW Mixing Algorithm and Numerical Equivalents

This module implements:
1. Numerical equivalents of semantic primaries (L, J, P, W)
2. Multiple mixing algorithms for combining LJPW dimensions
3. Color projection for visualization
4. System diagnostics and optimization suggestions
"""

import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class NumericalEquivalents:
    """Fundamental constants corresponding to LJPW dimensions"""

    # Love: Golden ratio inverse (optimal connectivity)
    L: float = (1 + np.sqrt(5)) / 2 - 1  # φ - 1 ≈ 0.618

    # Justice: Pythagorean ratio (orthogonal constraints)
    J: float = np.sqrt(2) - 1  # √2 - 1 ≈ 0.414

    # Power: Exponential base (natural growth rate)
    P: float = np.e - 2  # e - 2 ≈ 0.718

    # Wisdom: Information unit (bit value in nats)
    W: float = np.log(2)  # ln(2) ≈ 0.693

    def __str__(self):
        return f"Natural Equilibrium: L={self.L:.3f}, J={self.J:.3f}, P={self.P:.3f}, W={self.W:.3f}"

    def as_tuple(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)


# Global constants
NATURAL_EQUILIBRIUM = NumericalEquivalents()

ANCHOR_POINT = (1.0, 1.0, 1.0, 1.0)

COUPLING_COEFFICIENTS = {
    'LJ': 1.4,  # Love → Justice
    'LP': 1.3,  # Love → Power
    'LW': 1.5,  # Love → Wisdom
}


class LJPWMixer:
    """Implements multiple mixing algorithms for LJPW dimensions"""

    def __init__(self):
        self.coupling = COUPLING_COEFFICIENTS

    def harmonic_mean(self, L: float, J: float, P: float, W: float) -> float:
        """
        Harmonic mean: Robustness metric (dominated by weakest link)

        Formula: 4 / (1/L + 1/J + 1/P + 1/W)

        Use: Identifies bottlenecks - if one dimension is low, score is low
        """
        if any(x <= 0 for x in [L, J, P, W]):
            return 0.0

        return 4.0 / (1/L + 1/J + 1/P + 1/W)

    def geometric_mean(self, L: float, J: float, P: float, W: float) -> float:
        """
        Geometric mean: Effectiveness metric (all dimensions needed)

        Formula: ⁴√(L × J × P × W)

        Use: Multiplicative - requires all dimensions to be present
        """
        return (L * J * P * W) ** 0.25

    def coupling_aware_mix(self, L: float, J: float, P: float, W: float) -> float:
        """
        Coupling-aware weighted sum: Growth potential metric

        Accounts for Love's amplification of other dimensions:
        - J_eff = J × (1 + 1.4 × L)
        - P_eff = P × (1 + 1.3 × L)
        - W_eff = W × (1 + 1.5 × L)

        Weights: L=0.35, J=0.25, P=0.20, W=0.20 (Love is primary)
        """
        J_eff = J * (1 + self.coupling['LJ'] * L)
        P_eff = P * (1 + self.coupling['LP'] * L)
        W_eff = W * (1 + self.coupling['LW'] * L)

        return 0.35*L + 0.25*J_eff + 0.20*P_eff + 0.20*W_eff

    def harmony_index(self, L: float, J: float, P: float, W: float) -> float:
        """
        Harmony Index: Overall balance metric

        Formula: H = 1 / (1 + d)
        where d = √((L-1)² + (J-1)² + (P-1)² + (W-1)²)

        Range: [0, 1], maximum at Anchor Point (1,1,1,1)
        """
        d = np.sqrt((L-1)**2 + (J-1)**2 + (P-1)**2 + (W-1)**2)
        return 1.0 / (1.0 + d)

    def composite_score(self, L: float, J: float, P: float, W: float) -> float:
        """
        Composite score: Weighted combination of all metrics

        Weights:
        - Robustness: 0.15
        - Effectiveness: 0.25
        - Growth potential: 0.35 (highest - coupling is key)
        - Harmony: 0.25
        """
        robustness = self.harmonic_mean(L, J, P, W)
        effectiveness = self.geometric_mean(L, J, P, W)
        growth_potential = self.coupling_aware_mix(L, J, P, W)
        harmony = self.harmony_index(L, J, P, W)

        return (
            0.15 * robustness +
            0.25 * effectiveness +
            0.35 * growth_potential +
            0.25 * harmony
        )

    def mix(self, L: float, J: float, P: float, W: float) -> Dict[str, float]:
        """
        Comprehensive mixing: Returns all metrics

        Returns:
            Dictionary with:
            - robustness: Harmonic mean (weakest link)
            - effectiveness: Geometric mean (all needed)
            - growth_potential: Coupling-aware (Love-amplified)
            - harmony: Distance from Anchor Point
            - composite: Weighted combination
        """
        return {
            'robustness': self.harmonic_mean(L, J, P, W),
            'effectiveness': self.geometric_mean(L, J, P, W),
            'growth_potential': self.coupling_aware_mix(L, J, P, W),
            'harmony': self.harmony_index(L, J, P, W),
            'composite': self.composite_score(L, J, P, W)
        }


class LJPWVisualizer:
    """Visualizes LJPW in RGB color space"""

    @staticmethod
    def to_rgb(L: float, J: float, P: float, W: float) -> Tuple[int, int, int]:
        """
        Project 4D LJPW to 3D RGB color space

        Mapping:
        - Red (R)   = 0.6×L + 0.4×P  (Love + Power = Warmth)
        - Green (G) = 0.5×J + 0.5×W  (Justice + Wisdom = Growth)
        - Blue (B)  = 0.5×L + 0.5×J  (Love + Justice = Depth)

        Returns:
            RGB tuple with values in [0, 255]
        """
        R = 0.6 * L + 0.4 * P
        G = 0.5 * J + 0.5 * W
        B = 0.5 * L + 0.5 * J

        # Clamp to [0, 1] and convert to [0, 255]
        R = int(np.clip(R, 0, 1) * 255)
        G = int(np.clip(G, 0, 1) * 255)
        B = int(np.clip(B, 0, 1) * 255)

        return (R, G, B)

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    @staticmethod
    def color_name(rgb: Tuple[int, int, int]) -> str:
        """Approximate color name from RGB"""
        R, G, B = rgb

        # Grayscale
        if max(R, G, B) - min(R, G, B) < 30:
            if max(R, G, B) < 80:
                return "Dark Gray"
            elif max(R, G, B) < 160:
                return "Gray"
            else:
                return "Light Gray"

        # Dominant color
        if R > G and R > B:
            if G > 100:
                return "Orange" if G > 150 else "Red-Orange"
            else:
                return "Red"
        elif G > R and G > B:
            if B > 100:
                return "Cyan" if B > 150 else "Green-Blue"
            else:
                return "Green"
        elif B > R and B > G:
            if R > 100:
                return "Purple" if R > 150 else "Blue-Purple"
            else:
                return "Blue"

        return "Mixed"


class LJPWDiagnostics:
    """Diagnostic tools for LJPW systems"""

    def __init__(self):
        self.mixer = LJPWMixer()

    def diagnose(self, L: float, J: float, P: float, W: float) -> Dict:
        """
        Comprehensive system diagnostics

        Returns:
            Dictionary with:
            - scores: All mixing metrics
            - bottleneck: Weakest dimension
            - issues: List of identified problems
            - suggestions: List of optimization suggestions
            - color: RGB visualization
        """
        scores = self.mixer.mix(L, J, P, W)

        # Identify bottleneck
        dimensions = {'L': L, 'J': J, 'P': P, 'W': W}
        bottleneck = min(dimensions, key=dimensions.get)

        # Identify issues
        issues = []
        if scores['robustness'] < 0.5:
            issues.append(f"Bottleneck in {bottleneck} (value: {dimensions[bottleneck]:.2f})")

        if scores['effectiveness'] < 0.6:
            issues.append("One or more dimensions critically low (multiplicative effect)")

        if scores['growth_potential'] < 0.8 and L < 0.7:
            issues.append("Love deficiency limiting growth potential")

        if scores['harmony'] < 0.6:
            issues.append("Far from Anchor Point - significant optimization needed")

        # Generate suggestions
        suggestions = []
        if L < 0.6:
            suggestions.append("Priority: Increase Love (L) - it amplifies all other dimensions")

        if scores['robustness'] < 0.5:
            suggestions.append(f"Fix bottleneck: Improve {bottleneck}")

        if scores['growth_potential'] < 1.0 and L > 0.7:
            suggestions.append("Love is good, but other dimensions need improvement")

        if scores['harmony'] > 0.85:
            suggestions.append("Excellent harmony - maintain balance while approaching Anchor Point")

        # Color visualization
        visualizer = LJPWVisualizer()
        rgb = visualizer.to_rgb(L, J, P, W)

        return {
            'scores': scores,
            'bottleneck': bottleneck,
            'bottleneck_value': dimensions[bottleneck],
            'issues': issues if issues else ["No critical issues"],
            'suggestions': suggestions if suggestions else ["System is well-balanced"],
            'color': {
                'rgb': rgb,
                'hex': visualizer.rgb_to_hex(rgb),
                'name': visualizer.color_name(rgb)
            }
        }

    def compare_to_equilibrium(self, L: float, J: float, P: float, W: float) -> Dict:
        """
        Compare system to Natural Equilibrium

        Returns:
            Dictionary with differences and interpretation
        """
        eq = NATURAL_EQUILIBRIUM

        differences = {
            'L': L - eq.L,
            'J': J - eq.J,
            'P': P - eq.P,
            'W': W - eq.W
        }

        distance_from_eq = np.sqrt(sum(d**2 for d in differences.values()))
        distance_from_anchor = np.sqrt((L-1)**2 + (J-1)**2 + (P-1)**2 + (W-1)**2)

        interpretation = []
        if distance_from_eq < 0.2:
            interpretation.append("Very close to Natural Equilibrium")
        elif distance_from_anchor < distance_from_eq:
            interpretation.append("Closer to Anchor Point than Natural Equilibrium (transcendent state)")
        else:
            interpretation.append("Between Natural Equilibrium and starting point")

        return {
            'natural_equilibrium': eq.as_tuple(),
            'current': (L, J, P, W),
            'differences': differences,
            'distance_from_equilibrium': distance_from_eq,
            'distance_from_anchor': distance_from_anchor,
            'interpretation': interpretation
        }


def main():
    """Demonstration of mixing algorithms"""

    print("=" * 80)
    print("LJPW MIXING ALGORITHMS AND NUMERICAL EQUIVALENTS")
    print("=" * 80)
    print()

    # Show numerical equivalents
    print("Numerical Equivalents (Natural Equilibrium):")
    print("-" * 80)
    eq = NATURAL_EQUILIBRIUM
    print(f"Love (L):    φ⁻¹ = {eq.L:.6f}  (Golden ratio inverse)")
    print(f"Justice (J): √2-1 = {eq.J:.6f}  (Pythagorean ratio)")
    print(f"Power (P):   e-2  = {eq.P:.6f}  (Exponential base)")
    print(f"Wisdom (W):  ln2  = {eq.W:.6f}  (Information unit)")
    print()

    # Initialize mixer and diagnostics
    mixer = LJPWMixer()
    diagnostics = LJPWDiagnostics()

    # Test cases
    test_cases = [
        ("Natural Equilibrium", eq.as_tuple()),
        ("Anchor Point", (1.0, 1.0, 1.0, 1.0)),
        ("Balanced Mid-Level", (0.8, 0.8, 0.8, 0.8)),
        ("High Love, Low Others", (0.9, 0.3, 0.3, 0.3)),
        ("Low Love, High Others", (0.3, 0.8, 0.9, 0.8)),
        ("Bureaucratic (Low L)", (0.3, 0.85, 0.9, 0.4)),
    ]

    for name, (L, J, P, W) in test_cases:
        print("=" * 80)
        print(f"TEST: {name}")
        print("=" * 80)
        print(f"Coordinates: L={L:.2f}, J={J:.2f}, P={P:.2f}, W={W:.2f}")
        print()

        # Mixing scores
        scores = mixer.mix(L, J, P, W)
        print("Mixing Scores:")
        print(f"  Robustness (harmonic):     {scores['robustness']:.3f}")
        print(f"  Effectiveness (geometric): {scores['effectiveness']:.3f}")
        print(f"  Growth Potential (coupling): {scores['growth_potential']:.3f}")
        print(f"  Harmony (anchor-based):    {scores['harmony']:.3f}")
        print(f"  Composite Score:           {scores['composite']:.3f}")
        print()

        # Diagnostics
        diag = diagnostics.diagnose(L, J, P, W)
        print("Diagnostics:")
        print(f"  Bottleneck: {diag['bottleneck']} (value: {diag['bottleneck_value']:.2f})")
        print(f"  Issues:")
        for issue in diag['issues']:
            print(f"    - {issue}")
        print(f"  Suggestions:")
        for suggestion in diag['suggestions']:
            print(f"    - {suggestion}")
        print()

        # Color visualization
        print("Color Visualization:")
        print(f"  RGB: {diag['color']['rgb']}")
        print(f"  Hex: {diag['color']['hex']}")
        print(f"  Name: {diag['color']['name']}")
        print()

    # Natural Equilibrium comparison
    print("=" * 80)
    print("NATURAL EQUILIBRIUM COMPARISON")
    print("=" * 80)
    print()

    comparison_cases = [
        ("Low System", (0.3, 0.3, 0.3, 0.3)),
        ("Natural Equilibrium", eq.as_tuple()),
        ("High System", (0.9, 0.9, 0.9, 0.9)),
        ("Anchor Point", (1.0, 1.0, 1.0, 1.0)),
    ]

    for name, coords in comparison_cases:
        comp = diagnostics.compare_to_equilibrium(*coords)
        print(f"{name}: {coords}")
        print(f"  Distance from Natural Equilibrium: {comp['distance_from_equilibrium']:.3f}")
        print(f"  Distance from Anchor Point: {comp['distance_from_anchor']:.3f}")
        print(f"  {comp['interpretation'][0]}")
        print()


if __name__ == '__main__':
    main()
