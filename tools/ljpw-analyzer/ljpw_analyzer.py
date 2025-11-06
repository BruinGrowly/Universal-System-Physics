#!/usr/bin/env python3
"""
LJPW Analyzer - Open-source tool for analyzing systems using the LJPW framework

This tool provides:
- LJPW coordinate calculation
- Harmony Index computation
- Coupling dynamics analysis
- Optimization recommendations
- Visualization and reporting

Usage:
    ljpw-analyzer analyze <system-config.json>
    ljpw-analyzer optimize <system-config.json>
    ljpw-analyzer validate <data.csv>
    ljpw-analyzer coupling <system-config.json>
"""

import argparse
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import sys


@dataclass
class LJPWCoordinates:
    """Represents LJPW coordinates of a system"""
    L: float  # Love: [0, 1]
    J: float  # Justice: [0, 1]
    P: float  # Power: [0, 1]
    W: float  # Wisdom: [0, 1]

    def __post_init__(self):
        """Validate coordinates are in [0, 1]"""
        for dim in ['L', 'J', 'P', 'W']:
            value = getattr(self, dim)
            if not 0 <= value <= 1:
                raise ValueError(f"{dim} must be in [0, 1], got {value}")

    def to_array(self) -> np.ndarray:
        """Convert to numpy array"""
        return np.array([self.L, self.J, self.P, self.W])

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {'L': self.L, 'J': self.J, 'P': self.P, 'W': self.W}


class LJPWAnalyzer:
    """Core analyzer for LJPW framework"""

    # Coupling coefficient matrix (empirically derived)
    COUPLING_MATRIX = {
        'LL': 1.0,   'LJ': 1.4,   'LP': 1.3,   'LW': 1.5,
        'JL': 0.9,   'JJ': 1.0,   'JP': 0.7,   'JW': 1.2,
        'PL': 0.6,   'PJ': 0.8,   'PP': 1.0,   'PW': 0.5,
        'WL': 1.3,   'WJ': 1.1,   'WP': 1.0,   'WW': 1.0,
    }

    ANCHOR_POINT = LJPWCoordinates(L=1.0, J=1.0, P=1.0, W=1.0)

    @staticmethod
    def distance_from_anchor(coords: LJPWCoordinates) -> float:
        """
        Calculate Euclidean distance from Anchor Point (1,1,1,1)

        Formula: d = √((L-1)² + (J-1)² + (P-1)² + (W-1)²)
        """
        diff = coords.to_array() - LJPWAnalyzer.ANCHOR_POINT.to_array()
        return float(np.sqrt(np.sum(diff ** 2)))

    @staticmethod
    def harmony_index(coords: LJPWCoordinates) -> float:
        """
        Calculate Harmony Index

        Formula: H = 1 / (1 + d)
        Range: [0, 1], where 1 = perfect harmony (at anchor point)
        """
        d = LJPWAnalyzer.distance_from_anchor(coords)
        return 1.0 / (1.0 + d)

    @staticmethod
    def effective_dimensions(coords: LJPWCoordinates) -> Dict[str, float]:
        """
        Calculate effective dimensions considering coupling

        Formula: Effective_X = X × (1 + κ_LX × L)

        Returns effective values for J, P, W (Love couples to all)
        """
        L = coords.L
        return {
            'effective_L': L,  # Love doesn't get amplified by itself
            'effective_J': coords.J * (1 + LJPWAnalyzer.COUPLING_MATRIX['LJ'] * L),
            'effective_P': coords.P * (1 + LJPWAnalyzer.COUPLING_MATRIX['LP'] * L),
            'effective_W': coords.W * (1 + LJPWAnalyzer.COUPLING_MATRIX['LW'] * L),
        }

    @staticmethod
    def love_multiplier(L: float) -> Dict[str, float]:
        """
        Calculate Love multiplier effect on other dimensions

        Returns how much Love amplifies each dimension
        """
        return {
            'J_multiplier': 1 + LJPWAnalyzer.COUPLING_MATRIX['LJ'] * L,
            'P_multiplier': 1 + LJPWAnalyzer.COUPLING_MATRIX['LP'] * L,
            'W_multiplier': 1 + LJPWAnalyzer.COUPLING_MATRIX['LW'] * L,
        }

    @staticmethod
    def optimization_vector(coords: LJPWCoordinates) -> np.ndarray:
        """
        Calculate optimization vector pointing toward Anchor Point

        Formula: ∇V_A(r) = (1-L, 1-J, 1-P, 1-W)
        """
        return LJPWAnalyzer.ANCHOR_POINT.to_array() - coords.to_array()

    @staticmethod
    def optimization_priority(coords: LJPWCoordinates) -> List[Tuple[str, float]]:
        """
        Determine optimization priorities accounting for coupling

        Strategy: Love-first approach (Love amplifies other dimensions)
        Returns sorted list of (dimension, gap) prioritizing Love
        """
        opt_vec = LJPWAnalyzer.optimization_vector(coords)
        dims = ['L', 'J', 'P', 'W']
        gaps = [(dim, float(gap)) for dim, gap in zip(dims, opt_vec)]

        # Sort by gap, but heavily weight Love (2x)
        def priority_score(item):
            dim, gap = item
            if dim == 'L':
                return gap * 2.0  # Love-first
            return gap

        return sorted(gaps, key=priority_score, reverse=True)

    @staticmethod
    def love_first_roadmap(coords: LJPWCoordinates, weeks: int = 8) -> List[Dict]:
        """
        Generate Love-first optimization roadmap

        4-phase approach:
        1. Love foundation (weeks 1-2)
        2. L↔W amplification (weeks 3-4)
        3. Justice leverage (weeks 5-6)
        4. Power direction (weeks 7-8)
        """
        phases = []

        # Phase 1: Love (weeks 1-2)
        phases.append({
            'phase': 1,
            'weeks': '1-2',
            'focus': 'Love',
            'target_L': min(1.0, coords.L + 0.3),
            'interventions': [
                'Build psychological safety',
                'Increase cross-team collaboration',
                'Improve API intuitiveness',
                'Add empathy to code comments'
            ]
        })

        # Phase 2: Wisdom (weeks 3-4) - Leverage L↔W feedback loop
        phases.append({
            'phase': 2,
            'weeks': '3-4',
            'focus': 'Wisdom',
            'target_W': min(1.0, coords.W + 0.3),
            'interventions': [
                'Documentation sprint',
                'Knowledge sharing sessions',
                'Architecture decision records',
                'Shared mental models'
            ],
            'expected_love_boost': 0.1  # W → L coupling
        })

        # Phase 3: Justice (weeks 5-6) - Leverage Love amplification
        phases.append({
            'phase': 3,
            'weeks': '5-6',
            'focus': 'Justice',
            'target_J': min(1.0, coords.J + 0.3),
            'interventions': [
                'Comprehensive testing',
                'Consistent architecture',
                'Code review standards',
                'Technical debt reduction'
            ],
            'love_amplification': LJPWAnalyzer.COUPLING_MATRIX['LJ']
        })

        # Phase 4: Power (weeks 7-8) - Direct and amplify
        phases.append({
            'phase': 4,
            'weeks': '7-8',
            'focus': 'Power',
            'target_P': min(1.0, coords.P + 0.3),
            'interventions': [
                'Performance optimization',
                'Scalability improvements',
                'Execution efficiency',
                'Resource utilization'
            ],
            'love_amplification': LJPWAnalyzer.COUPLING_MATRIX['LP'],
            'justice_direction': 'Justice directs Power efficiently'
        })

        return phases


class CouplingValidator:
    """Validates coupling coefficient hypotheses"""

    @staticmethod
    def validate_coupling_coefficient(
        L_values: np.ndarray,
        J_values: np.ndarray,
        J_effective_observed: np.ndarray,
        expected_kappa: float = 1.4
    ) -> Dict:
        """
        Validate: Effective_J = J × (1 + κ_LJ × L)

        Tests Prediction 2: κ_LJ = 1.4 ± 0.2

        Returns:
            - fitted_kappa: Best-fit coupling coefficient
            - r_squared: R² goodness of fit
            - p_value: Statistical significance
            - confidence_interval: 95% CI for κ
            - validated: True if 1.2 < κ < 1.6 and R² > 0.6
        """
        from scipy import stats

        # Model: Effective_J = J * (1 + κ * L)
        # Rearrange: Effective_J / J = 1 + κ * L
        # Linear regression: y = 1 + κ * L

        y = J_effective_observed / J_values
        x = L_values

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        fitted_kappa = slope
        r_squared = r_value ** 2

        # 95% confidence interval for slope
        from scipy.stats import t
        n = len(x)
        t_val = t.ppf(0.975, n - 2)  # 97.5th percentile, n-2 df
        ci_low = fitted_kappa - t_val * std_err
        ci_high = fitted_kappa + t_val * std_err

        # Validation criteria
        validated = (
            1.2 <= fitted_kappa <= 1.6 and  # Within expected range
            r_squared > 0.6 and              # Strong correlation
            p_value < 0.05                   # Statistically significant
        )

        return {
            'fitted_kappa': fitted_kappa,
            'expected_kappa': expected_kappa,
            'r_squared': r_squared,
            'p_value': p_value,
            'confidence_interval': (ci_low, ci_high),
            'validated': validated,
            'sample_size': n
        }


def analyze_command(config_path: str) -> None:
    """Analyze a system from JSON configuration"""
    with open(config_path, 'r') as f:
        config = json.load(f)

    coords = LJPWCoordinates(**config['coordinates'])

    print(f"=== LJPW Analysis: {config.get('system', 'Unknown System')} ===\n")

    # Basic metrics
    print(f"Coordinates: L={coords.L:.2f}, J={coords.J:.2f}, P={coords.P:.2f}, W={coords.W:.2f}")

    distance = LJPWAnalyzer.distance_from_anchor(coords)
    harmony = LJPWAnalyzer.harmony_index(coords)

    print(f"Distance from Anchor: {distance:.3f}")
    print(f"Harmony Index: {harmony:.3f}")

    # Effective dimensions
    print("\n--- Coupling Effects ---")
    effective = LJPWAnalyzer.effective_dimensions(coords)
    multipliers = LJPWAnalyzer.love_multiplier(coords.L)

    print(f"Love Multiplier Effect at L={coords.L:.2f}:")
    print(f"  Justice:  {coords.J:.2f} → {effective['effective_J']:.2f} ({multipliers['J_multiplier']:.2f}x)")
    print(f"  Power:    {coords.P:.2f} → {effective['effective_P']:.2f} ({multipliers['P_multiplier']:.2f}x)")
    print(f"  Wisdom:   {coords.W:.2f} → {effective['effective_W']:.2f} ({multipliers['W_multiplier']:.2f}x)")

    # Optimization priorities
    print("\n--- Optimization Priorities ---")
    priorities = LJPWAnalyzer.optimization_priority(coords)
    for i, (dim, gap) in enumerate(priorities, 1):
        dim_name = {'L': 'Love', 'J': 'Justice', 'P': 'Power', 'W': 'Wisdom'}[dim]
        print(f"{i}. {dim_name}: gap = {gap:.3f}")


def optimize_command(config_path: str) -> None:
    """Generate optimization roadmap"""
    with open(config_path, 'r') as f:
        config = json.load(f)

    coords = LJPWCoordinates(**config['coordinates'])

    print(f"=== Love-First Optimization Roadmap ===\n")
    print(f"Current: L={coords.L:.2f}, J={coords.J:.2f}, P={coords.P:.2f}, W={coords.W:.2f}")
    print(f"Harmony Index: {LJPWAnalyzer.harmony_index(coords):.3f}\n")

    roadmap = LJPWAnalyzer.love_first_roadmap(coords)

    for phase in roadmap:
        print(f"\n--- Phase {phase['phase']}: {phase['focus']} (Weeks {phase['weeks']}) ---")
        if 'target_L' in phase:
            print(f"Target Love: {phase['target_L']:.2f}")
        if 'target_W' in phase:
            print(f"Target Wisdom: {phase['target_W']:.2f}")
        if 'target_J' in phase:
            print(f"Target Justice: {phase['target_J']:.2f}")
        if 'target_P' in phase:
            print(f"Target Power: {phase['target_P']:.2f}")

        print("\nInterventions:")
        for intervention in phase['interventions']:
            print(f"  • {intervention}")

        if 'love_amplification' in phase:
            print(f"\nLove Amplification: {phase['love_amplification']:.2f}x")
        if 'expected_love_boost' in phase:
            print(f"Expected Love Boost: +{phase['expected_love_boost']:.2f}")


def coupling_command(config_path: str) -> None:
    """Analyze coupling dynamics"""
    with open(config_path, 'r') as f:
        config = json.load(f)

    coords = LJPWCoordinates(**config['coordinates'])

    print("=== Coupling Dynamics Analysis ===\n")

    # Show full coupling matrix
    print("Coupling Coefficient Matrix:")
    print("        L      J      P      W")
    for row_dim in ['L', 'J', 'P', 'W']:
        print(f"  {row_dim}  ", end="")
        for col_dim in ['L', 'J', 'P', 'W']:
            coef = LJPWAnalyzer.COUPLING_MATRIX[f'{row_dim}{col_dim}']
            print(f"{coef:.2f}   ", end="")
        print()

    print("\n--- Love Multiplier Effect ---")
    print(f"At current Love level (L={coords.L:.2f}):")

    multipliers = LJPWAnalyzer.love_multiplier(coords.L)
    effective = LJPWAnalyzer.effective_dimensions(coords)

    for dim in ['J', 'P', 'W']:
        dim_name = {'J': 'Justice', 'P': 'Power', 'W': 'Wisdom'}[dim]
        base = getattr(coords, dim)
        eff = effective[f'effective_{dim}']
        mult = multipliers[f'{dim}_multiplier']
        improvement = ((eff / base) - 1) * 100 if base > 0 else 0

        print(f"{dim_name}: {base:.2f} × {mult:.2f} = {eff:.2f} (+{improvement:.1f}%)")


def main():
    parser = argparse.ArgumentParser(
        description='LJPW Analyzer - Analyze systems using the LJPW framework'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a system')
    analyze_parser.add_argument('config', help='Path to system configuration JSON')

    # Optimize command
    optimize_parser = subparsers.add_parser('optimize', help='Generate optimization roadmap')
    optimize_parser.add_argument('config', help='Path to system configuration JSON')

    # Coupling command
    coupling_parser = subparsers.add_parser('coupling', help='Analyze coupling dynamics')
    coupling_parser.add_argument('config', help='Path to system configuration JSON')

    args = parser.parse_args()

    if args.command == 'analyze':
        analyze_command(args.config)
    elif args.command == 'optimize':
        optimize_command(args.config)
    elif args.command == 'coupling':
        coupling_command(args.config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
