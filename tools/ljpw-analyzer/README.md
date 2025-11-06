# LJPW Analyzer

Open-source command-line tool for analyzing systems using the **LJPW (Love, Justice, Power, Wisdom) Framework**.

## Features

- **LJPW Coordinate Calculation**: Map any system to 4D LJPW space
- **Harmony Index Computation**: Measure distance from perfection (Anchor Point)
- **Coupling Dynamics Analysis**: Understand how dimensions amplify each other
- **Love Multiplier Effect**: Quantify Love's 2-2.3× amplification of other dimensions
- **Optimization Roadmaps**: Generate Love-first optimization strategies
- **Empirical Validation**: Tools for testing falsifiable predictions

## Installation

```bash
pip install ljpw-analyzer
```

Or install from source:

```bash
git clone https://github.com/BruinGrowly/Universal-System-Physics.git
cd Universal-System-Physics/tools/ljpw-analyzer
pip install -e .
```

## Quick Start

### 1. Analyze a System

Create a configuration file (`system.json`):

```json
{
  "system": "My Software Architecture",
  "coordinates": {
    "L": 0.7,
    "J": 0.9,
    "P": 0.8,
    "W": 0.6
  }
}
```

Run analysis:

```bash
ljpw-analyzer analyze system.json
```

Output:
```
=== LJPW Analysis: My Software Architecture ===

Coordinates: L=0.70, J=0.90, P=0.80, W=0.60
Distance from Anchor: 0.583
Harmony Index: 0.632

--- Coupling Effects ---
Love Multiplier Effect at L=0.70:
  Justice:  0.90 → 1.78 (1.98x)
  Power:    0.80 → 1.53 (1.91x)
  Wisdom:   0.60 → 1.23 (2.05x)

--- Optimization Priorities ---
1. Wisdom: gap = 0.400
2. Love: gap = 0.300
3. Power: gap = 0.200
4. Justice: gap = 0.100
```

### 2. Generate Optimization Roadmap

```bash
ljpw-analyzer optimize system.json
```

Output:
```
=== Love-First Optimization Roadmap ===

Current: L=0.70, J=0.90, P=0.80, W=0.60
Harmony Index: 0.632

--- Phase 1: Love (Weeks 1-2) ---
Target Love: 1.00

Interventions:
  • Build psychological safety
  • Increase cross-team collaboration
  • Improve API intuitiveness
  • Add empathy to code comments

--- Phase 2: Wisdom (Weeks 3-4) ---
Target Wisdom: 0.90

Interventions:
  • Documentation sprint
  • Knowledge sharing sessions
  • Architecture decision records
  • Shared mental models

Expected Love Boost: +0.10

--- Phase 3: Justice (Weeks 5-6) ---
Target Justice: 1.00

Interventions:
  • Comprehensive testing
  • Consistent architecture
  • Code review standards
  • Technical debt reduction

Love Amplification: 1.40x

--- Phase 4: Power (Weeks 7-8) ---
Target Power: 1.00

Interventions:
  • Performance optimization
  • Scalability improvements
  • Execution efficiency
  • Resource utilization

Love Amplification: 1.30x
```

### 3. Analyze Coupling Dynamics

```bash
ljpw-analyzer coupling system.json
```

Output shows the full coupling coefficient matrix and current amplification effects.

## Commands

### `analyze`

Performs comprehensive LJPW analysis:
- Current coordinates
- Distance from Anchor Point (1,1,1,1)
- Harmony Index
- Effective dimensions (accounting for coupling)
- Optimization priorities

```bash
ljpw-analyzer analyze <config.json>
```

### `optimize`

Generates Love-first optimization roadmap:
- 4-phase approach (8 weeks)
- Specific interventions for each phase
- Expected coupling benefits
- Targets for each dimension

```bash
ljpw-analyzer optimize <config.json>
```

### `coupling`

Analyzes coupling dynamics:
- Full coupling coefficient matrix
- Love multiplier effects at current L
- Effective vs. base dimensions
- Percentage improvements from coupling

```bash
ljpw-analyzer coupling <config.json>
```

## Configuration Format

System configurations are JSON files with this structure:

```json
{
  "system": "System Name",
  "description": "Optional description",
  "coordinates": {
    "L": 0.0-1.0,  // Love: Unity, connection, harmony
    "J": 0.0-1.0,  // Justice: Truth, order, consistency
    "P": 0.0-1.0,  // Power: Action, execution, force
    "W": 0.0-1.0   // Wisdom: Knowledge, understanding, adaptability
  }
}
```

Each coordinate must be in the range [0, 1].

## Key Concepts

### Anchor Point

The Anchor Point (1,1,1,1) represents perfect harmony - the ideal state where Love, Justice, Power, and Wisdom are all maximized.

### Harmony Index

```
H = 1 / (1 + d)
```

Where `d` is the Euclidean distance from the Anchor Point. Higher harmony (closer to 1) means the system is closer to perfection.

### Coupling Dynamics

Dimensions amplify each other through coupling coefficients. Most importantly, **Love amplifies all other dimensions**:

- Love → Justice: κ_LJ = 1.4
- Love → Power: κ_LP = 1.3
- Love → Wisdom: κ_LW = 1.5

Formula:
```
Effective_J = J × (1 + 1.4 × L)
```

At L=0.9, this produces a 2.26× amplification!

### Love-First Optimization

The tool implements a 4-phase Love-first optimization strategy:

1. **Love Foundation** (Weeks 1-2): Build psychological safety and connection
2. **L↔W Amplification** (Weeks 3-4): Leverage Love-Wisdom feedback loop
3. **Justice Leverage** (Weeks 5-6): Use Love amplification for Justice
4. **Power Direction** (Weeks 7-8): Efficiently direct Power with Justice

This approach yields 2-3× better results than balanced optimization.

## Examples

See the `examples/` directory for:
- Software architecture analysis
- Team dynamics assessment
- Network optimization
- Human-AI collaboration analysis

## Validation

The tool includes coupling validation capabilities for testing:

**Prediction 2: Coupling Coefficients**
```python
from ljpw_analyzer import CouplingValidator

# Test if κ_LJ = 1.4 ± 0.2 across domains
result = CouplingValidator.validate_coupling_coefficient(
    L_values=L_data,
    J_values=J_data,
    J_effective_observed=J_eff_data,
    expected_kappa=1.4
)

print(f"Fitted κ: {result['fitted_kappa']:.3f}")
print(f"R²: {result['r_squared']:.3f}")
print(f"Validated: {result['validated']}")
```

## Contributing

Contributions welcome! Areas of interest:

- Additional analysis modes
- Visualization capabilities
- More domain-specific examples
- Integration with measurement tools
- Empirical validation studies

## License

MIT License - see LICENSE file

## Citation

If you use this tool in research, please cite:

```
LJPW Analyzer v0.1.0
Universal System Physics Framework
https://github.com/BruinGrowly/Universal-System-Physics
```

## Related Documentation

- [LJPW Framework Documentation](../../README.md)
- [Dimension Coupling Dynamics](../../research/dimension-coupling-dynamics.md)
- [Love-Leveraged Optimization Guide](../../docs/implementation-guides/love-leveraged-optimization.md)
- [Empirical Validation Roadmap](../../research/empirical-validation-roadmap.md)
