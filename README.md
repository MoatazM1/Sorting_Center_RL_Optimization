# 📦 Swiss Post Package Sorting Optimization with RL

**Moataz Mansour**

This project uses **Reinforcement Learning** to optimize **Swiss Post's package sorting centers**. An RL agent learns when and how to intervene (add/remove chutes, reroute packages, priority processing) to minimize delays while keeping costs low.

---

## 🚀 Objective

Can an RL agent learn optimal resource management for a dynamic sorting center with stochastic demand?

1. 🎯 Predict demand using LSTM time series forecasting
2. 🤖 Train RL agents to make real-time sorting decisions
3. 📊 Compare 10 policies: from-scratch (Q-Learning, SARSA, DQN) + SB3 (DQN, PPO, A2C, MaskablePPO) + baselines

---

## 🧠 Project Structure

| File | Description |
|------|-------------|
| `3Reinforcement_Learning_v1.6.ipynb` | **Unified notebook** — all RL work in one place (v1.6) |
| `1Random_forest.ipynb` | Baseline model using tree-based methods |
| `2LSTM.ipynb` | Time series delay prediction using LSTM |
| `generate_report_v16.py` | PDF report generator |
| `RL_Project_Report_v1.6.pdf` | 📄 Full project report |
| `data4day_with_issues.csv` | 4-day dataset (~144K records) with injected congestion |
| `saved_models/` | Persisted trained agents (7 files) |

---

## 🎮 MDP Formulation

| MDP Component | Symbol | Implementation |
|---------------|--------|----------------|
| State space | S | [load, hour, day, chutes, queue, rate] |
| Action space | A | {0:nothing, 1:add_chute, 2:reroute, 3:priority, 4:remove_chute} |
| Transition | P(s'\|s,a) | Deterministic: actions affect queue/capacity |
| Reward | R(s,a) | Multi-factor: delay + throughput + overload + chute penalty |
| Discount | γ | 0.99 |

---

## 🧪 Environment Progression

| Aspect | V1 | V2 | V3 |
|--------|----|----|-----|
| Starting chutes | 2 | 1 | 1 |
| Max chutes | 5 | 4 | 4 |
| Demand scale | Raw | Amplified ×20 | Curriculum |
| Action masking | No | No | Yes |
| Episode length | 100 | 200 | 200 |

---

## 📚 Algorithm Selection

| Algorithm | Category | Key Idea |
|-----------|----------|----------|
| Q-Learning | Value (off-policy) | Q-table + epsilon-greedy |
| SARSA | Value (on-policy) | Uses actual next action |
| DQN | Value-based | Q\*(s,a) with neural net + replay |
| A2C | Actor-Critic | Actor π(a\|s) + Critic V(s) |
| PPO | Policy Gradient | Clipped surrogate objective |
| MaskablePPO | Constrained PG | PPO + invalid action masking |

> **Why not SAC/TD3?** These require continuous action spaces. Our sorting center uses 5 discrete actions.

---

## 🤖 RL Agent Hyperparameter Summary

| # | Agent | Type | α (LR) | γ (Discount) | ε (Exploration) | Training | Test Reward |
|---|-------|------|---------|--------------|-----------------|----------|-------------|
| 1 | Q-Learning | Tabular (scratch) | 0.1 | 0.99 | 1.0→0.05 (decay 0.999/ep) | 5K episodes | 997 |
| 2 | SARSA | Tabular (scratch) | 0.1 | 0.99 | 1.0→0.05 (decay 0.999/ep) | 5K episodes | 666 |
| 3 | **DQN (scratch)** | PyTorch NN | 5e-4 | 0.99 | 1.0→0.05 (linear/100K) | 300K steps | **1,819** |
| 4 | DQN (SB3) | Stable-Baselines3 | 5e-4 | 0.99 | 1.0→0.05 (40% frac) | 300K steps | 1,801 |
| 5 | PPO (SB3) | Policy Gradient | 3e-4 | 0.99 | entropy=0.01 | 300K steps | -6.5M |
| 6 | A2C (SB3) | Actor-Critic | 7e-4 | 0.99 | entropy=0.01 | 300K steps | -2,508 |
| 7 | MaskablePPO | Masked PG (sb3-contrib) | 3e-4 | 0.99 | entropy=0.01 | 300K steps | 1,315 |
| 8 | Heuristic | Rule-based | — | — | — | — | 1,316 |
| 9 | Random | Uniform | — | — | — | — | -1,037 |
| 10 | Do Nothing | Baseline | — | — | — | — | -6.5M |

### DQN (scratch) Architecture

| Parameter | Value |
|-----------|-------|
| Network | 7 → 128 → 128 → 5 (ReLU) |
| Optimizer | Adam (lr=5×10⁻⁴) |
| Replay buffer | 50,000 transitions |
| Batch size | 64 |
| Target net update | Every 250 steps |
| Epsilon decay | Linear over 100K steps |

### SB3 Algorithm-Specific Settings

| Parameter | DQN | PPO | A2C | MaskablePPO |
|-----------|-----|-----|-----|-------------|
| Batch size | 64 | 64 | N/A (online) | 64 |
| Buffer / n_steps | 50,000 | 512 | 5 | 512 |
| n_epochs | — | 10 | — | 10 |
| Entropy coef | — | 0.01 | 0.01 | 0.01 |
| Value func coef | — | — | 0.5 | — |
| Target update interval | 250 | — | — | — |
| Exploration fraction | 0.4 | — | — | — |
| Training strategy | 3-phase curriculum | 3-phase curriculum | 3-phase curriculum | 3-phase curriculum |

### HP Grid Search Winner (Q-Learning)

| α | γ | Avg Reward |
|---|---|-----------|
| **0.01** | **0.8** | **934.3** (best) |
| 0.01 | 0.95 | 891.7 |
| 0.1 | 0.8 | 899.5 |
| 0.5 | 0.99 | 483.5 (worst) |

---

## 📊 Training Strategy: 3-Phase Curriculum

| Phase | Difficulty | Demand Scale | Steps | Purpose |
|-------|-----------|--------------|-------|---------|
| 1. Easy | 0.25 | 5× | 100K | Learn basic mechanics |
| 2. Medium | 0.60 | 12× | 100K | Learn timing |
| 3. Hard | 1.00 | 20× | 100K | Master peak demand |

---

## 📎 Results Summary

- **Best agent**: DQN from scratch (reward 1,819) — outperforms SB3 DQN and hand-crafted heuristic
- **Simulation impact**: 98% reduction in overloaded hours, 90% queue reduction, 34% throughput improvement
- **PPO/A2C failure**: PPO collapsed to "do nothing" (-6.5M), A2C only reroutes (-2,508)
- **Multi-run evaluation** (5 runs × 20 episodes): DQN scratch 1,812 ± 17 confirms statistical robustness
- **Policy heatmaps** reveal interpretable decision boundaries per agent
- **All models saved** to `saved_models/` for reuse without retraining

---

## 💰 Cost-Benefit Analysis

| Cost Item | Estimate | Source |
|-----------|----------|--------|
| Chute activation | CHF 50/activation | Equipment + staffing |
| Chute maintenance | CHF 25/hour/chute | Labor + electricity |
| Package rerouting | CHF 2/package | Extra handling |
| Priority processing | CHF 15/hour | Overtime premium |
| Delayed package penalty | CHF 5/package-hour | SLA penalty |
| Overload incident | CHF 200/incident | Disruption + recovery |

---

## 🎬 Visual Demos

- **Simulation comparison**: Do Nothing vs RL Agent over 48 hours
- **Zoomed critical window**: Hour-by-hour decision trace
- **Sorting center schematic**: System architecture diagram
- **Live animation**: 48-frame FuncAnimation with play/pause controls
- **RL formalism mapping**: MDP components visualized

---

## 📦 Dataset

- `data4day_with_issues.csv` — 4 days of hourly package sorting data (~144K records)
- Columns: HOUR_TIME, CHUTE, PACKAGE_COUNT, AVG_PROCESSING_TIME_MINUTES
- Train/test split: Days 1-2 (train) / Day 4 (test)
- 691 rows with negative processing times cleaned

---

## 🔄 Version History

| Version | Changes |
|---------|---------|
| v1.0 | Initial DQN with 3 actions (V1 environment) |
| v1.1 | DQN + PPO (100K), V1 & V2 environments, 7-policy comparison |
| v1.2 | DQN + A2C + PPO + MaskablePPO + Curriculum (300K each), V3 env |
| v1.3 | From-Scratch Q-Learning + DQN + Ensemble |
| v1.4 | Visual Simulation Demo (SortingCenterSim, side-by-side comparison) |
| v1.5 | Interactive Live Animation (FuncAnimation + RL formalism) |
| **v1.6** | **UNIFIED: All above + SARSA + Policy Heatmap + HP Search + Multi-Run + Save/Load** |

---

## 🛠 Dependencies

```bash
pip install gymnasium stable-baselines3 sb3-contrib matplotlib seaborn pandas numpy torch fpdf2
```

---

## 📓 Notebook Cell Map

| Cells | Part | Content |
|-------|------|---------|
| 1–3 | Intro & Theory | Objective, RL concepts, MDP formulation |
| 4–9 | Part 1 | Data loading, aggregation, LSTM predictions, dashboard |
| 10–16 | Part 2–3 | V1 environment, training, callbacks, visualization |
| 17–22 | Part 4 | From-scratch Q-Learning (tabular, 5K episodes) |
| 23–25 | Part 5 | From-scratch SARSA + comparison |
| 26–27 | Part 6 | V2 environment (harder demand) |
| 28–29 | Part 7 | V3 environment + action masking |
| 30–32 | Part 8 | From-scratch DQN (PyTorch, 300K steps) |
| 33–34 | Part 9 | SB3 training (4 algorithms × 300K steps) |
| 35–36 | Part 10 | 10-policy evaluation (temporal split) |
| 37–38 | Part 11 | Results dashboard |
| 39–40 | Part 12 | Cost-benefit analysis (CHF) |
| 41–42 | Part 13 | Policy heatmap |
| 43–44 | Part 14 | HP grid search (α × γ) |
| 45–46 | Part 15 | Multi-run evaluation (5×20) |
| 47–48 | Part 16 | Model save/load |
| 49–55 | Part 17 | Simulation demo (48 hours) |
| 56–62 | Part 18 | Live animation + RL formalism |
| 63 | Part 19 | Conclusions, hyperparameter summary, business recommendations |

---

## 🚀 How to Reproduce

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac

# 3. Install dependencies
pip install gymnasium stable-baselines3 sb3-contrib matplotlib seaborn pandas numpy torch fpdf2

# 4. Place data4day_with_issues.csv in project folder

# 5. Open 3Reinforcement_Learning_v1.6.ipynb in VS Code

# 6. Select .venv kernel

# 7. Run All Cells (~45 minutes for full training)
```

---

## 📂 Project Structure

```
Sorting_center_M6AML_project/
├── 3Reinforcement_Learning_v1.6.ipynb   # Main notebook (63 cells)
├── generate_report_v16.py               # PDF report generator
├── RL_Project_Report_v1.6.pdf           # Generated PDF report
├── README.md                            # This document
├── data4day_with_issues.csv             # Raw data (~144K records)
├── saved_models/                        # Persisted trained agents
│   ├── dqn_v3_sorting_center.zip        # SB3 DQN
│   ├── ppo_v3_sorting_center.zip        # SB3 PPO
│   ├── a2c_v3_sorting_center.zip        # SB3 A2C
│   ├── masked_ppo_sorting_center.zip    # SB3 MaskablePPO
│   ├── q_agent.json                     # Q-Learning Q-table
│   ├── sarsa_agent.json                 # SARSA Q-table
│   └── dqn_scratch.pt                   # PyTorch DQN weights
└── oldversion/                          # Previous notebook versions
```

---

*Report generated from notebook `3Reinforcement_Learning_v1.6.ipynb` — Swiss Post Sorting Center RL Optimization*
