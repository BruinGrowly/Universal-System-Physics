# Measurement Protocol: Software Teams

## Objective: Convert Observable Metrics → LJPW Coordinates

This protocol enables **objective, non-arbitrary** measurement of LJPW dimensions in software teams using quantifiable data.

---

## Overview

**Domain**: Software Development Teams (5-50 people)
**Time Period**: 2-week sprint (minimum) to 3-month quarter (ideal)
**Data Sources**: Git repos, issue trackers, CI/CD, surveys
**Output**: LJPW coordinates (L, J, P, W) ∈ [0,1]⁴

---

## Part 1: Love (L) - Mutual Information / Connectivity

**Definition**: `L = I(X;Y) / H(X)` = Mutual information between team members / Maximum possible

### Metrics (4 components, equal weight)

#### 1.1 Cross-Team Code Review (Connectivity)

**What to Measure**:
```python
# From Git data
total_commits = count(commits)
cross_reviewed = count(commits_reviewed_by_someone_else)
self_merged = count(commits_merged_by_author)

connectivity_score = cross_reviewed / total_commits
```

**Interpretation**:
- 0.0 = No one reviews anyone else's code (isolated)
- 0.5 = Half of commits get external review
- 1.0 = Every commit reviewed by teammates (full connectivity)

**Data Source**: Git history
```bash
git log --all --format="%H|%an|%cn" | analyze_reviews.py
```

---

#### 1.2 API Usability (Low Surprise / High Predictability)

**What to Measure**:
```python
# From production logs / error tracking
api_calls_total = count(api_invocations)
api_errors = count(4xx_errors + 5xx_errors)
api_retries = count(retry_attempts)

surprise_rate = (api_errors + api_retries) / api_calls_total
usability_score = 1 - surprise_rate
```

**Interpretation**:
- 0.0 = APIs always fail or need retries (high surprise)
- 0.5 = 50% success rate on first try
- 1.0 = APIs work as expected (zero surprise)

**Data Source**: Application logs, error tracking (Sentry, DataDog)
```python
# From error tracking API
error_rate = sentry.get_error_rate(time_period="2weeks")
usability = 1 - error_rate
```

---

#### 1.3 Documentation Coverage (Shared Understanding)

**What to Measure**:
```python
# From codebase analysis
public_functions = count(exported_functions + public_methods)
documented_functions = count(functions_with_docstrings)
outdated_docs = count(docs_modified_before_code_changed)

doc_coverage = documented_functions / public_functions
doc_freshness = 1 - (outdated_docs / documented_functions)
documentation_score = mean([doc_coverage, doc_freshness])
```

**Interpretation**:
- 0.0 = No documentation exists
- 0.5 = Half of public APIs documented
- 1.0 = Complete, up-to-date documentation

**Data Source**: Static analysis
```bash
# Python example
pylint --load-plugins=pylint.extensions.docparams --docstring-min-length=10
# Generate documentation_score
```

---

#### 1.4 Psychological Safety (Survey)

**What to Measure**:
```python
# From validated psychological safety survey
# (Edmondson 1999, 7 items, 7-point Likert scale)

questions = [
    "If you make a mistake on this team, it is often held against you", # Reverse scored
    "Members of this team are able to bring up problems and tough issues",
    "People on this team sometimes reject others for being different", # Reverse
    "It is safe to take a risk on this team",
    "It is difficult to ask other members of this team for help", # Reverse
    "No one on this team would deliberately act in a way that undermines my efforts",
    "Working with members of this team, my unique skills and talents are valued and utilized"
]

# Score: 1 (Strongly Disagree) to 7 (Strongly Agree)
# Reverse items: reverse_score = 8 - raw_score

psych_safety_score = mean(all_responses) / 7.0  # Normalize to [0,1]
```

**Interpretation**:
- 0.0 = Extremely unsafe to speak up
- 0.5 = Moderate safety
- 1.0 = Complete psychological safety

**Data Source**: Anonymous team survey (Google Forms, SurveyMonkey)

---

### Love Composite Score

```python
L = mean([
    connectivity_score,      # 0.25 weight
    usability_score,         # 0.25 weight
    documentation_score,     # 0.25 weight
    psych_safety_score       # 0.25 weight
])
```

**Example Calculation**:
```
Team Alpha (2-week sprint):
  Connectivity:     0.85 (85% cross-reviewed)
  Usability:        0.92 (8% API error rate)
  Documentation:    0.65 (65% coverage)
  Psych Safety:     0.78 (5.5/7 survey score)

L = (0.85 + 0.92 + 0.65 + 0.78) / 4 = 0.80
```

---

## Part 2: Justice (J) - Constraint Satisfaction / Order

**Definition**: `J = Constraints_Met / Total_Constraints`

### Metrics (4 components, equal weight)

#### 2.1 Test Coverage (Verification Constraints)

**What to Measure**:
```python
# From code coverage tools
lines_covered = count(lines_executed_by_tests)
total_lines = count(lines_of_code)
branches_covered = count(branches_tested)
total_branches = count(decision_points)

line_coverage = lines_covered / total_lines
branch_coverage = branches_covered / total_branches
test_coverage_score = mean([line_coverage, branch_coverage])
```

**Interpretation**:
- 0.0 = No tests exist
- 0.5 = Half of code/branches tested
- 1.0 = Complete test coverage

**Data Source**: Coverage tools
```bash
# Python
pytest --cov=myapp --cov-report=json
# Parse coverage.json for scores

# JavaScript
jest --coverage --coverageReporters=json
# Parse coverage-final.json
```

---

#### 2.2 Architecture Consistency (Structural Constraints)

**What to Measure**:
```python
# From static analysis / linters
architecture_rules = [
    "No circular dependencies",
    "Layers respect dependency direction",
    "No direct database access from UI",
    "All services behind interfaces",
    # ... project-specific rules
]

total_checks = count(architecture_rules) * count(modules)
violations = count(rule_violations_detected)

consistency_score = 1 - (violations / total_checks)
```

**Interpretation**:
- 0.0 = Architecture completely violated
- 0.5 = Half of modules violate rules
- 1.0 = Perfect architectural compliance

**Data Source**: Architecture linters
```bash
# Python
import-linter --config=.import-linter.ini

# Java
archunit-maven-plugin check

# Generate consistency_score
```

---

#### 2.3 Code Standards Compliance (Style Constraints)

**What to Measure**:
```python
# From style checkers
total_files = count(source_files)
compliant_files = count(files_passing_linter)
total_violations = sum(violations_per_file)
max_violations = total_files * average_violations_per_file_baseline

compliance_score = compliant_files / total_files
severity_score = 1 - (total_violations / max_violations)
code_standards_score = mean([compliance_score, severity_score])
```

**Interpretation**:
- 0.0 = No files comply with standards
- 0.5 = Half of files compliant
- 1.0 = Perfect compliance

**Data Source**: Linters/formatters
```bash
# Python
pylint myapp/ --output-format=json > pylint_report.json
black --check myapp/

# JavaScript
eslint src/ --format json > eslint_report.json

# Generate code_standards_score
```

---

#### 2.4 Technical Debt Ratio (Resource Constraints)

**What to Measure**:
```python
# From time tracking / estimation
total_development_hours = sum(hours_logged)
debt_remediation_hours = sum(hours_on_refactoring + hours_on_bug_fixes)
debt_interest_hours = debt_remediation_hours * 0.5  # Estimate

productive_hours = total_development_hours - debt_interest_hours
debt_ratio = 1 - (debt_interest_hours / total_development_hours)
```

**Interpretation**:
- 0.0 = All time spent fighting technical debt
- 0.5 = Half of time on new features, half on debt
- 1.0 = Zero technical debt

**Data Source**: Issue tracker, time logs
```python
# From JIRA/GitHub
total_hours = jira.get_time_logged(sprint_id)
debt_hours = jira.get_time_logged(label="tech-debt")
debt_ratio = 1 - (debt_hours / total_hours)
```

---

### Justice Composite Score

```python
J = mean([
    test_coverage_score,     # 0.25 weight
    consistency_score,       # 0.25 weight
    code_standards_score,    # 0.25 weight
    debt_ratio              # 0.25 weight
])
```

**Example Calculation**:
```
Team Alpha:
  Test Coverage:    0.82 (82% lines, 78% branches → 80%)
  Consistency:      0.94 (6% architecture violations)
  Code Standards:   0.88 (88% files compliant)
  Debt Ratio:       0.75 (25% time on debt)

J = (0.82 + 0.94 + 0.88 + 0.75) / 4 = 0.85
```

---

## Part 3: Power (P) - Channel Capacity / Throughput

**Definition**: `P = C_actual / C_max`

### Metrics (3 components, equal weight)

#### 3.1 Delivery Velocity (Feature Throughput)

**What to Measure**:
```python
# From sprint tracking
story_points_delivered = sum(completed_stories_points)
story_points_committed = sum(sprint_planned_points)
historical_average = mean(last_6_sprints_velocity)

velocity_achievement = story_points_delivered / story_points_committed
velocity_trend = story_points_delivered / historical_average
velocity_score = mean([velocity_achievement, velocity_trend])
```

**Interpretation**:
- 0.0 = Delivering nothing
- 0.5 = Delivering 50% of capacity
- 1.0 = Delivering at or above capacity

**Data Source**: Sprint tracking
```python
# From JIRA
sprint = jira.get_sprint(sprint_id)
velocity_score = sprint.completed_points / sprint.committed_points
```

---

#### 3.2 System Performance (Response Time)

**What to Measure**:
```python
# From application monitoring
p95_response_time_ms = percentile(response_times, 95)
sla_target_ms = 500  # Example SLA
performance_ratio = sla_target_ms / p95_response_time_ms

performance_score = min(1.0, performance_ratio)  # Cap at 1.0
```

**Interpretation**:
- 0.0 = System infinitely slow
- 0.5 = 2x slower than SLA
- 1.0 = Meeting or exceeding SLA

**Data Source**: APM tools (DataDog, New Relic)
```python
# From DataDog API
p95 = datadog.get_metric("api.response_time.p95")
performance_score = min(1.0, 500 / p95)
```

---

#### 3.3 Scalability Headroom (Capacity Utilization)

**What to Measure**:
```python
# From infrastructure monitoring
current_load = current_requests_per_second
max_capacity = tested_maximum_rps  # From load testing
cpu_utilization = mean(cpu_usage_percent) / 100
memory_utilization = mean(memory_usage_percent) / 100

load_ratio = current_load / max_capacity
resource_ratio = mean([cpu_utilization, memory_utilization])

# Optimal is ~70% (room to scale, not over-provisioned)
optimal_utilization = 0.70
scalability_score = 1 - abs(resource_ratio - optimal_utilization) / optimal_utilization
```

**Interpretation**:
- 0.0 = At capacity limit (can't scale) or idle (wasted)
- 0.5 = Moderately utilized
- 1.0 = Optimal utilization (~70%)

**Data Source**: Infrastructure monitoring
```python
# From Prometheus
cpu = prometheus.query("avg(cpu_usage)")
scalability_score = 1 - abs(cpu - 0.70) / 0.70
```

---

### Power Composite Score

```python
P = mean([
    velocity_score,          # 0.33 weight
    performance_score,       # 0.33 weight
    scalability_score        # 0.33 weight
])
```

**Example Calculation**:
```
Team Alpha:
  Velocity:       0.95 (delivered 95% of committed points)
  Performance:    0.88 (p95 = 450ms vs SLA 500ms)
  Scalability:    0.71 (at 79% utilization, optimal is 70%)

P = (0.95 + 0.88 + 0.71) / 3 = 0.85
```

---

## Part 4: Wisdom (W) - Processing Efficiency / Learning

**Definition**: `W = η_actual / η_max`

### Metrics (4 components, equal weight)

#### 4.1 Documentation Ratio (Knowledge Capture)

**What to Measure**:
```python
# From repository analysis
documentation_lines = count(lines_in_docs_files + docstrings)
code_lines = count(lines_of_code_excluding_comments)

doc_ratio = documentation_lines / code_lines
# Optimal ratio ~0.3-0.5 (30-50% doc to code)
optimal_doc_ratio = 0.40

# Score: 1.0 at optimal, decreases as you move away
if doc_ratio <= optimal_doc_ratio:
    documentation_ratio_score = doc_ratio / optimal_doc_ratio
else:
    # Penalty for over-documentation
    documentation_ratio_score = 1.0 - (doc_ratio - optimal_doc_ratio) / optimal_doc_ratio
    documentation_ratio_score = max(0, documentation_ratio_score)
```

**Interpretation**:
- 0.0 = No documentation or excessive documentation
- 0.5 = 20% doc ratio (below optimal)
- 1.0 = Optimal 40% doc ratio

**Data Source**: Repository analysis
```bash
cloc myapp/ --by-file --json > cloc_report.json
# Calculate doc_lines / code_lines
```

---

#### 4.2 Onboarding Efficiency (Learning Speed)

**What to Measure**:
```python
# From HR / team tracking
new_engineer_days_to_first_commit = [5, 3, 7, 4]  # Recent hires
baseline_days = 10  # Industry/company baseline

mean_onboarding_days = mean(new_engineer_days_to_first_commit)
onboarding_efficiency = 1 - (mean_onboarding_days / baseline_days)
onboarding_efficiency = max(0, onboarding_efficiency)  # Don't go negative
```

**Interpretation**:
- 0.0 = Takes as long as baseline (or longer)
- 0.5 = 50% faster than baseline
- 1.0 = Instant productivity

**Data Source**: HR records + Git
```python
# Track: hire_date → first_commit_date
first_commits = git.get_first_commits_by_author(new_hires)
onboarding_days = [(commit_date - hire_date).days for commit_date, hire_date in ...]
onboarding_efficiency = 1 - (mean(onboarding_days) / 10)
```

---

#### 4.3 Change Isolation (Knowledge Locality)

**What to Measure**:
```python
# From Git analysis
total_commits = count(commits)
localized_commits = count(commits_touching_single_module)
ripple_commits = count(commits_touching_multiple_modules)

isolation_ratio = localized_commits / total_commits
```

**Interpretation**:
- 0.0 = Every change ripples across codebase
- 0.5 = Half of changes are localized
- 1.0 = Perfect isolation (changes never ripple)

**Data Source**: Git history
```bash
# For each commit, count files changed
git log --name-only --format="%H" | analyze_change_scope.py
```

---

#### 4.4 Knowledge Retention (Survey)

**What to Measure**:
```python
# Survey questions (7-point Likert)
knowledge_questions = [
    "I understand how our system works end-to-end",
    "I can explain our architecture to new team members",
    "I know where to find information when I need it",
    "Our team has documented lessons learned from incidents",
    "Important knowledge is not trapped in one person's head"
]

# Score: 1 (Strongly Disagree) to 7 (Strongly Agree)
knowledge_retention_score = mean(all_responses) / 7.0
```

**Interpretation**:
- 0.0 = No shared knowledge
- 0.5 = Moderate knowledge sharing
- 1.0 = Complete knowledge retention

**Data Source**: Team survey

---

### Wisdom Composite Score

```python
W = mean([
    documentation_ratio_score,  # 0.25 weight
    onboarding_efficiency,      # 0.25 weight
    isolation_ratio,            # 0.25 weight
    knowledge_retention_score   # 0.25 weight
])
```

**Example Calculation**:
```
Team Alpha:
  Doc Ratio:      0.75 (30% ratio, below 40% optimal)
  Onboarding:     0.60 (4 days vs 10 baseline → 60% faster)
  Isolation:      0.88 (88% of changes localized)
  Knowledge:      0.71 (5.0/7 survey score)

W = (0.75 + 0.60 + 0.88 + 0.71) / 4 = 0.74
```

---

## Complete Example: Team Alpha Measurement

### Raw Data Collected (2-week sprint)

```yaml
Love:
  cross_review_rate: 0.85
  api_error_rate: 0.08  → usability: 0.92
  doc_coverage: 0.65
  psych_safety_survey: 5.5/7 → 0.79

Justice:
  line_coverage: 0.82, branch_coverage: 0.78 → 0.80
  architecture_violations: 6% → consistency: 0.94
  code_standards: 88% compliant → 0.88
  tech_debt_time: 25% → debt_ratio: 0.75

Power:
  velocity: 95% of committed points → 0.95
  p95_response_time: 450ms (SLA 500ms) → 0.88
  cpu_utilization: 79% (optimal 70%) → 0.71

Wisdom:
  doc_ratio: 30% (optimal 40%) → 0.75
  onboarding: 4 days (baseline 10) → 0.60
  change_isolation: 88% → 0.88
  knowledge_survey: 5.0/7 → 0.71
```

### LJPW Coordinates

```python
L = (0.85 + 0.92 + 0.65 + 0.79) / 4 = 0.80
J = (0.80 + 0.94 + 0.88 + 0.75) / 4 = 0.84
P = (0.95 + 0.88 + 0.71) / 3 = 0.85
W = (0.75 + 0.60 + 0.88 + 0.71) / 4 = 0.74
```

**Team Alpha**: **(0.80, 0.84, 0.85, 0.74)**

### Comparison to Natural Equilibrium

```
Team Alpha:          (L=0.80, J=0.84, P=0.85, W=0.74)
Natural Equilibrium: (L=0.62, J=0.41, P=0.72, W=0.69)

Differences:
  L: +29% (strong connectivity)
  J: +105% (very high order)
  P: +18% (strong throughput)
  W: +7% (slightly above natural)

Distance from Natural Equilibrium: 0.51
Distance from Anchor Point: 0.36

Interpretation: Well above Natural Equilibrium, trending toward Anchor Point
```

### Mixing Scores

```python
Robustness (harmonic):     0.806
Effectiveness (geometric): 0.807
Growth Potential (coupling): 1.396  (coupling active!)
Harmony (anchor):          0.735
Composite:                 0.982

Bottleneck: W (0.74 - lowest dimension)
Suggestion: Improve documentation and onboarding to unlock more growth
```

---

## Data Collection Checklist

### Automated (No Manual Effort)

- [ ] Git history (commits, reviews, changes)
- [ ] Code coverage reports (CI/CD)
- [ ] Linter/formatter results (CI/CD)
- [ ] Application metrics (APM tools)
- [ ] Infrastructure metrics (monitoring)
- [ ] Sprint velocity (issue tracker API)

### Semi-Automated (Periodic Setup)

- [ ] Architecture rules (configure once, auto-check)
- [ ] SLA targets (configure once, auto-monitor)
- [ ] Baseline values (measure once, track delta)

### Manual (Minimal)

- [ ] Psychological safety survey (quarterly)
- [ ] Knowledge retention survey (quarterly)
- [ ] Time categorization (if not auto-tracked)

**Total Setup Time**: ~4 hours initial setup, ~15 minutes per sprint ongoing

---

## Validation: Why This is Objective

Each metric is:

1. **Quantifiable**: Counts, ratios, timings (not opinions)
2. **Reproducible**: Same inputs → same outputs
3. **Automatable**: Extracted from tools, not surveys (mostly)
4. **Comparable**: Measured against Natural Equilibrium baseline
5. **Actionable**: Identifies specific improvement areas

**This is not "rate your team's Love on a scale of 1-10"** - it's **"measure mutual information via cross-review rates, API error rates, documentation coverage, and validated psychological safety instruments"**.

---

## Next Steps

1. **Implement Calibration Tool** (converts these raw metrics → LJPW)
2. **Run Validation Study** (test if Natural Equilibrium predicts performance)
3. **Create Domain-Specific Protocols** (networks, organizations, AI interactions)

---

*Measurement Protocol Version: 1.0*
*Domain: Software Development Teams*
*Last Updated: November 2025*
