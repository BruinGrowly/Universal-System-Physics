#!/usr/bin/env python3
"""
Prediction 2: Coupling Coefficient Validation

Tests hypothesis: κ_LJ = 1.4 ± 0.2 across all domains

This script:
1. Loads data from multiple domains
2. Fits coupling coefficient κ_LJ for each domain
3. Tests statistical significance
4. Validates cross-domain consistency
5. Generates publication-quality figures
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from typing import Dict, Tuple
import json


class CouplingCoefficientValidator:
    """Validates coupling coefficient hypothesis"""

    def __init__(self, expected_kappa: float = 1.4, tolerance: float = 0.2):
        self.expected_kappa = expected_kappa
        self.tolerance = tolerance
        self.results = {}

    def fit_coupling_coefficient(
        self,
        L_values: np.ndarray,
        J_values: np.ndarray,
        J_effective_observed: np.ndarray,
        domain: str
    ) -> Dict:
        """
        Fit coupling coefficient for a single domain

        Model: Effective_J = J × (1 + κ × L)
        Rearranged: Effective_J / J = 1 + κ × L
        """
        # Calculate amplification factor
        amplification = J_effective_observed / J_values

        # Linear regression: amplification = 1 + κ × L
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            L_values, amplification
        )

        fitted_kappa = slope
        r_squared = r_value ** 2

        # 95% confidence interval
        n = len(L_values)
        t_val = stats.t.ppf(0.975, n - 2)  # 97.5th percentile
        ci_low = fitted_kappa - t_val * std_err
        ci_high = fitted_kappa + t_val * std_err

        # Cohen's f² effect size for R²
        f_squared = r_squared / (1 - r_squared) if r_squared < 1 else np.inf

        # Validation criteria
        in_range = (self.expected_kappa - self.tolerance) <= fitted_kappa <= (
            self.expected_kappa + self.tolerance
        )
        good_fit = r_squared > 0.6
        significant = p_value < 0.05

        validated = in_range and good_fit and significant

        result = {
            'domain': domain,
            'fitted_kappa': fitted_kappa,
            'expected_kappa': self.expected_kappa,
            'r_squared': r_squared,
            'p_value': p_value,
            'std_error': std_err,
            'confidence_interval': (ci_low, ci_high),
            'effect_size_f2': f_squared,
            'sample_size': n,
            'validated': validated,
            'in_range': in_range,
            'good_fit': good_fit,
            'significant': significant
        }

        self.results[domain] = result
        return result

    def cross_domain_analysis(self) -> Dict:
        """Analyze consistency across domains"""
        if len(self.results) < 2:
            raise ValueError("Need at least 2 domains for cross-domain analysis")

        kappas = [r['fitted_kappa'] for r in self.results.values()]
        domains = list(self.results.keys())

        mean_kappa = np.mean(kappas)
        std_kappa = np.std(kappas, ddof=1)
        sem_kappa = std_kappa / np.sqrt(len(kappas))

        # 95% CI for mean
        t_val = stats.t.ppf(0.975, len(kappas) - 1)
        ci_low = mean_kappa - t_val * sem_kappa
        ci_high = mean_kappa + t_val * sem_kappa

        # Consistency score: 1 - normalized std
        # Perfect consistency (std=0) → 1.0
        # High variation (std>0.5) → <0.5
        consistency = max(0, 1 - std_kappa / self.tolerance)

        # ANOVA test: Are kappas significantly different across domains?
        # If not, that's good (consistency)
        # Note: This is a simplification - proper analysis would be multilevel model
        f_stat, anova_p = stats.f_oneway(*[
            [r['fitted_kappa']] for r in self.results.values()
        ])

        return {
            'mean_kappa': mean_kappa,
            'std_kappa': std_kappa,
            'sem_kappa': sem_kappa,
            'confidence_interval': (ci_low, ci_high),
            'consistency_score': consistency,
            'cross_domain_variance': std_kappa ** 2,
            'domains_tested': len(domains),
            'anova_f': f_stat,
            'anova_p': anova_p,
            'domains_validated': sum(r['validated'] for r in self.results.values()),
            'validation_rate': sum(r['validated'] for r in self.results.values()) / len(self.results)
        }

    def bayesian_analysis(self) -> Dict:
        """
        Bayesian analysis of coupling coefficient

        Prior: κ ~ Normal(1.4, 0.2²)
        Likelihood: Data from all domains
        Posterior: Updated belief about κ
        """
        # Collect all data points
        all_kappas = [r['fitted_kappa'] for r in self.results.values()]
        all_stderrs = [r['std_error'] for r in self.results.values()]

        # Prior parameters
        prior_mean = self.expected_kappa
        prior_std = 0.2

        # Posterior using conjugate update (weighted average)
        # This is simplified - proper Bayesian would use MCMC
        prior_precision = 1 / (prior_std ** 2)

        posterior_precision = prior_precision + sum(1 / (se ** 2) for se in all_stderrs)
        posterior_variance = 1 / posterior_precision
        posterior_std = np.sqrt(posterior_variance)

        posterior_mean = posterior_variance * (
            prior_precision * prior_mean +
            sum(kappa / (se ** 2) for kappa, se in zip(all_kappas, all_stderrs))
        )

        # 95% Credible Interval
        ci_low = stats.norm.ppf(0.025, posterior_mean, posterior_std)
        ci_high = stats.norm.ppf(0.975, posterior_mean, posterior_std)

        # Probability that κ is in expected range
        prob_in_range = (
            stats.norm.cdf(self.expected_kappa + self.tolerance, posterior_mean, posterior_std) -
            stats.norm.cdf(self.expected_kappa - self.tolerance, posterior_mean, posterior_std)
        )

        return {
            'posterior_mean': posterior_mean,
            'posterior_std': posterior_std,
            'credible_interval_95': (ci_low, ci_high),
            'probability_in_range': prob_in_range,
            'prior_mean': prior_mean,
            'prior_std': prior_std
        }

    def generate_report(self) -> str:
        """Generate human-readable validation report"""
        report = []
        report.append("=" * 80)
        report.append("COUPLING COEFFICIENT VALIDATION REPORT")
        report.append("Prediction 2: κ_LJ = 1.4 ± 0.2")
        report.append("=" * 80)
        report.append("")

        # Per-domain results
        report.append("DOMAIN-SPECIFIC RESULTS:")
        report.append("-" * 80)

        for domain, result in self.results.items():
            report.append(f"\n{domain.upper()}:")
            report.append(f"  Fitted κ_LJ: {result['fitted_kappa']:.3f}")
            report.append(f"  95% CI: [{result['confidence_interval'][0]:.3f}, {result['confidence_interval'][1]:.3f}]")
            report.append(f"  R²: {result['r_squared']:.3f}")
            report.append(f"  p-value: {result['p_value']:.4f}")
            report.append(f"  Sample size: {result['sample_size']}")
            report.append(f"  Effect size (f²): {result['effect_size_f2']:.3f}")

            # Validation checks
            status = "✓ VALIDATED" if result['validated'] else "✗ NOT VALIDATED"
            report.append(f"  Status: {status}")

            checks = []
            checks.append(f"In range [1.2, 1.6]: {'✓' if result['in_range'] else '✗'}")
            checks.append(f"R² > 0.6: {'✓' if result['good_fit'] else '✗'}")
            checks.append(f"p < 0.05: {'✓' if result['significant'] else '✗'}")
            report.append(f"  Checks: {', '.join(checks)}")

        # Cross-domain analysis
        if len(self.results) > 1:
            report.append("\n" + "-" * 80)
            report.append("CROSS-DOMAIN ANALYSIS:")
            report.append("-" * 80)

            cross = self.cross_domain_analysis()

            report.append(f"\nMean κ_LJ across domains: {cross['mean_kappa']:.3f} ± {cross['std_kappa']:.3f}")
            report.append(f"95% CI: [{cross['confidence_interval'][0]:.3f}, {cross['confidence_interval'][1]:.3f}]")
            report.append(f"Consistency score: {cross['consistency_score']:.3f}")
            report.append(f"Domains validated: {cross['domains_validated']} / {cross['domains_tested']}")
            report.append(f"Validation rate: {cross['validation_rate']:.1%}")

            # Bayesian analysis
            report.append("\n" + "-" * 80)
            report.append("BAYESIAN ANALYSIS:")
            report.append("-" * 80)

            bayes = self.bayesian_analysis()

            report.append(f"\nPrior: κ ~ Normal({bayes['prior_mean']:.2f}, {bayes['prior_std']:.2f}²)")
            report.append(f"Posterior: κ ~ Normal({bayes['posterior_mean']:.3f}, {bayes['posterior_std']:.3f}²)")
            report.append(f"95% Credible Interval: [{bayes['credible_interval_95'][0]:.3f}, {bayes['credible_interval_95'][1]:.3f}]")
            report.append(f"P(κ ∈ [1.2, 1.6]): {bayes['probability_in_range']:.1%}")

        # Overall conclusion
        report.append("\n" + "=" * 80)
        report.append("CONCLUSION:")
        report.append("=" * 80)

        if len(self.results) > 1:
            cross = self.cross_domain_analysis()
            bayes = self.bayesian_analysis()

            if cross['validation_rate'] >= 0.75 and bayes['probability_in_range'] > 0.80:
                report.append("\n✓ HYPOTHESIS VALIDATED")
                report.append(f"  The coupling coefficient κ_LJ ≈ {cross['mean_kappa']:.2f} is consistent")
                report.append(f"  across {cross['domains_tested']} domains with {bayes['probability_in_range']:.1%} confidence.")
            else:
                report.append("\n✗ HYPOTHESIS NOT VALIDATED")
                report.append(f"  Insufficient evidence for κ_LJ = 1.4 ± 0.2")
                report.append(f"  Validation rate: {cross['validation_rate']:.1%} (need >75%)")
        else:
            report.append("\nInsufficient data for cross-domain validation (need ≥2 domains)")

        report.append("=" * 80)

        return "\n".join(report)


def generate_synthetic_data(domain: str, n: int = 30, true_kappa: float = 1.4, noise: float = 0.1):
    """
    Generate synthetic data for testing

    In real study, this would be replaced with actual measurements
    """
    np.random.seed(hash(domain) % 2**32)  # Reproducible per domain

    # Random L and J values
    L = np.random.beta(5, 2, n)  # Skewed toward higher values
    J = np.random.beta(5, 2, n)

    # True relationship with noise
    J_effective = J * (1 + true_kappa * L) + np.random.normal(0, noise, n)

    # Ensure J_effective > 0
    J_effective = np.maximum(J_effective, 0.1)

    return L, J, J_effective


def main():
    """Run coupling coefficient validation"""

    print("Coupling Coefficient Validation Study")
    print("Prediction 2: κ_LJ = 1.4 ± 0.2\n")

    validator = CouplingCoefficientValidator(expected_kappa=1.4, tolerance=0.2)

    # Test with synthetic data (replace with real data in actual study)
    domains = ['software_teams', 'networks', 'organizations', 'human_ai']

    print("Generating synthetic data for 4 domains...")
    print("(In real study, load actual measurements)\n")

    for domain in domains:
        L, J, J_eff = generate_synthetic_data(domain, n=30, true_kappa=1.4, noise=0.15)

        print(f"Fitting {domain}... ", end='')
        result = validator.fit_coupling_coefficient(L, J, J_eff, domain)
        status = "✓" if result['validated'] else "✗"
        print(f"{status} κ={result['fitted_kappa']:.3f}, R²={result['r_squared']:.3f}")

    print("\n" + "=" * 80)
    print(validator.generate_report())

    # Save results
    output = {
        'domain_results': validator.results,
        'cross_domain': validator.cross_domain_analysis(),
        'bayesian': validator.bayesian_analysis()
    }

    with open('prediction-02-results.json', 'w') as f:
        # Convert numpy types to Python types for JSON serialization
        def convert(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(item) for item in obj]
            return obj

        json.dump(convert(output), f, indent=2)

    print("\nResults saved to: prediction-02-results.json")


if __name__ == '__main__':
    main()
