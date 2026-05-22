"""
Generate a professional PDF report for the Swiss Post RL Project v1.6.
Extended from v1.3 report with: SARSA, Policy Heatmap, HP Grid Search,
Multi-Run Eval, Model Save/Load, Simulation Demo, Live Animation.
"""
from fpdf import FPDF
import os

class ProjectReport(FPDF):
    BLUE = (41, 128, 185)
    DARK = (44, 62, 80)
    LIGHT_GRAY = (245, 245, 245)
    WHITE = (255, 255, 255)
    GREEN = (39, 174, 96)
    RED = (231, 76, 60)
    ORANGE = (243, 156, 18)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*self.DARK)
            self.cell(0, 8, "Swiss Post RL Project v1.6", align="L")
            self.cell(0, 8, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
            self.line(10, 16, 200, 16)
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "Moataz Mansour", align="C")

    def cover_page(self):
        self.add_page()
        self.ln(50)
        self.set_fill_color(*self.BLUE)
        self.rect(0, 45, 210, 65, "F")
        self.set_y(48)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*self.WHITE)
        self.cell(0, 15, "Reinforcement Learning for", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 15, "Swiss Post Package Sorting", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 13)
        self.cell(0, 10, "Q-Learning, SARSA, DQN, A2C, PPO, MaskablePPO & Ensemble", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "I", 11)
        self.cell(0, 8, "From-Scratch + Stable-Baselines3 | Unified Notebook v1.6", align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(25)
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, "Reinforcement Learning Project", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "Moataz Mansour", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "June 2026", align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(12)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, "Version History", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        versions = [
            "v1.0 - Initial DQN with 3 actions (V1 environment)",
            "v1.1 - DQN + PPO (100K), V1 & V2 environments, 7-policy comparison",
            "v1.2 - DQN + A2C + PPO + MaskablePPO + Curriculum (300K each), V3 env",
            "v1.3 - From-Scratch Q-Learning + DQN + Ensemble",
            "v1.4 - Visual Simulation Demo (SortingCenterSim, side-by-side comparison)",
            "v1.5 - Interactive Live Animation (FuncAnimation + RL formalism)",
            "v1.6 - UNIFIED: All above + SARSA + Policy Heatmap + HP Search + Multi-Run + Save/Load",
        ]
        for v in versions:
            self.cell(0, 6, v, align="C", new_x="LMARGIN", new_y="NEXT")

    def section_title(self, title, num=None):
        self.ln(6)
        self.set_fill_color(*self.BLUE)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 14)
        label = f"  {num}. {title}" if num else f"  {title}"
        self.cell(0, 10, label, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(3)
        self.set_text_color(*self.DARK)

    def sub_title(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.BLUE)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.DARK)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, bold_prefix=None):
        self.set_font("Helvetica", "", 10)
        left = self.l_margin
        self.set_x(left)
        self.cell(6, 5.5, "  ", new_x="END")
        if bold_prefix:
            self.set_font("Helvetica", "B", 10)
            w = self.get_string_width(bold_prefix) + 1
            self.cell(w, 5.5, bold_prefix, new_x="END")
            self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")

    def add_table(self, headers, rows, col_widths=None, highlight_row=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*self.BLUE)
        self.set_text_color(*self.WHITE)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, align="C", fill=True)
        self.ln()
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        for r_idx, row in enumerate(rows):
            if highlight_row is not None and r_idx == highlight_row:
                self.set_fill_color(213, 245, 227)
            elif r_idx % 2 == 0:
                self.set_fill_color(*self.LIGHT_GRAY)
            else:
                self.set_fill_color(*self.WHITE)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6.5, str(cell), border=1, align="C", fill=True)
            self.ln()
        self.ln(3)

    def add_image_if_exists(self, path, w=180):
        if os.path.exists(path):
            self.image(path, x=15, w=w)
            self.ln(5)
        else:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 6, f"[Image: {os.path.basename(path)} - run notebook to generate]",
                     new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*self.DARK)


def generate_report():
    pdf = ProjectReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    img_dir = os.path.dirname(os.path.abspath(__file__))

    # ══ COVER PAGE ══
    pdf.cover_page()

    # ══ TABLE OF CONTENTS ══
    pdf.add_page()
    pdf.section_title("Table of Contents")
    toc = [
        ("1", "Problem Statement & Motivation"),
        ("2", "RL Core Concepts"),
        ("3", "Theoretical Foundation: MDP"),
        ("4", "Data Overview"),
        ("5", "RL Environment Design (V1, V2, V3)"),
        ("6", "V1: First Attempt & Lessons"),
        ("7", "V2: Harder Environment"),
        ("8", "V3: Action Masking + Curriculum"),
        ("9", "From-Scratch Implementations"),
        ("", "  9a. Tabular Q-Learning"),
        ("", "  9b. SARSA Agent"),
        ("", "  9c. Deep Q-Network in PyTorch"),
        ("10", "SB3 Training Strategy & Agent Hyperparameters"),
        ("11", "Results & Evaluation"),
        ("11", "Policy Heatmap Analysis (NEW in v1.6)"),
        ("12", "Policy Heatmap Analysis"),
        ("13", "Hyperparameter Grid Search"),
        ("14", "Multi-Run Statistical Evaluation"),
        ("15", "Model Persistence - Save & Load"),
        ("16", "Cost-Benefit Analysis"),
        ("17", "Visual Simulation Demo"),
        ("18", "Interactive Live Animation"),
        ("19", "Conclusions & Business Recommendations"),
    ]
    pdf.set_font("Helvetica", "", 11)
    for num, title in toc:
        if num:
            pdf.cell(10, 7, num + ".")
        else:
            pdf.cell(10, 7, "")
        is_new = "NEW" in title
        if is_new:
            pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        if is_new:
            pdf.set_font("Helvetica", "", 11)
    pdf.ln(3)

    # ══ 1. PROBLEM STATEMENT ══
    pdf.add_page()
    pdf.section_title("Problem Statement & Motivation", 1)
    pdf.body_text(
        "Swiss Post's package sorting centers process thousands of packages per hour across multiple "
        "chutes (sorting lanes). During peak hours, chutes become congested - queues build up, "
        "processing times spike, and delays cascade through the system."
    )
    pdf.body_text(
        "The core question: can a Reinforcement Learning agent learn when and how to intervene "
        "(add/remove capacity, reroute, or apply priority processing) to minimize delays while "
        "keeping operational costs low?"
    )
    pdf.sub_title("Why Reinforcement Learning?")
    pdf.add_table(
        ["Approach", "Strength", "Limitation"],
        [
            ["Rule-based", "Simple, interpretable", "Can't adapt to unseen patterns"],
            ["LSTM Forecasting", "Predicts future load", "Descriptive, not prescriptive"],
            ["Reinforcement Learning", "Learns optimal actions", "Needs careful env design"],
        ],
        col_widths=[45, 65, 80],
    )

    # ══ 2. RL CORE CONCEPTS ══
    pdf.add_page()
    pdf.section_title("RL Core Concepts", 2)
    pdf.body_text(
        "Before building the environment, we define the five building blocks of Reinforcement "
        "Learning and how each maps to our sorting center problem."
    )

    pdf.sub_title("1. Environment (PackagingCenterEnv)")
    pdf.body_text(
        "The simulated sorting center. Each step = 1 time interval. Packages arrive (driven by "
        "real data), get processed through chutes, queues grow/shrink, and chute load changes."
    )

    pdf.sub_title("2. State - What the Agent Sees (6 dimensions)")
    pdf.add_table(
        ["#", "Feature", "Example", "What It Tells the Agent"],
        [
            ["1", "Chute load", "0.85", "How overloaded are the chutes?"],
            ["2", "Hour of day", "0.52 (=noon)", "Is a peak hour coming?"],
            ["3", "Day of week", "0.4", "Is it a busy or quiet day?"],
            ["4", "Active chutes", "0.5 (=2 of 4)", "How much capacity available?"],
            ["5", "Queue length", "0.6 (=60%)", "Are packages backing up?"],
            ["6", "Processing rate", "0.8 (=80%)", "How fast are packages moving?"],
        ],
        col_widths=[8, 30, 32, 100],
    )

    pdf.sub_title("3. Actions - What the Agent Does (5 choices)")
    pdf.add_table(
        ["Action", "Effect", "When Used"],
        [
            ["0 - Do Nothing", "No intervention", "System healthy"],
            ["1 - Add Chute", "+1 chute (more capacity)", "Load rising"],
            ["2 - Reroute", "Reduce queue 20-40%", "Queue building"],
            ["3 - Priority", "Boost processing +30%", "Clearing backlog"],
            ["4 - Remove Chute", "-1 chute (save cost)", "Load is low"],
        ],
        col_widths=[38, 60, 70],
    )

    pdf.sub_title("4. Reward - The Feedback Signal")
    pdf.body_text(
        "r = -load_penalty + throughput_bonus - overload_penalty - action_cost - chute_maintenance\n\n"
        "Plus bonuses for smart inaction (+4.0 if load < 0.9 and throughput > 0.6) and penalties "
        "for excess chutes (-2.0 per extra when load < 0.3).\n\n"
        "Key insight: The reward function is the steering wheel of RL. By removing the 'do nothing' "
        "penalty in V3, we taught the agent that strategic inaction is valuable."
    )

    pdf.sub_title("5. Policy - The Learned Strategy")
    pdf.body_text(
        "The Q-table or neural network that maps state -> action. The Q-value Q(s,a) = expected "
        "future cumulative reward if the agent takes action a in state s. The agent picks the "
        "action with the highest Q-value (greedy policy)."
    )

    pdf.sub_title("Parameter Definitions")
    pdf.add_table(
        ["Symbol", "Name", "Meaning"],
        [
            ["alpha", "Learning Rate", "Step size for updates. Lower = more stable"],
            ["gamma", "Discount Factor", "Weight of future rewards. 0.99 = ~100 steps ahead"],
            ["epsilon", "Exploration Rate", "Decays from 1.0 (random) to ~0.05 (exploit)"],
        ],
        col_widths=[25, 40, 110],
    )

    # ══ 3. THEORETICAL FOUNDATION ══
    pdf.add_page()
    pdf.section_title("Theoretical Foundation: MDP", 3)
    pdf.sub_title("Markov Decision Process (MDP) Formulation")
    pdf.add_table(
        ["MDP Component", "Symbol", "Our Implementation"],
        [
            ["State space", "S", "[load, hour, day, chutes, queue, rate]"],
            ["Action space", "A", "{0:nothing, 1:add, 2:reroute, 3:priority, 4:remove}"],
            ["Transition", "P(s'|s,a)", "Deterministic: actions affect queue/capacity"],
            ["Reward", "R(s,a)", "Multi-factor: delay + throughput + overload + chute penalty"],
            ["Discount", "gamma=0.99", "Long-term cumulative reward optimization"],
        ],
        col_widths=[40, 35, 115],
    )

    pdf.sub_title("Algorithm Selection Rationale")
    pdf.add_table(
        ["Algorithm", "Category", "Key Idea"],
        [
            ["Q-Learning", "Value (off-policy)", "Q-table + epsilon-greedy"],
            ["SARSA", "Value (on-policy)", "Uses actual next action (NEW)"],
            ["DQN", "Value-based", "Q*(s,a) with neural net + replay"],
            ["A2C", "Actor-Critic", "Actor pi(a|s) + Critic V(s)"],
            ["PPO", "Policy Gradient", "Clipped ratio for stability"],
            ["MaskablePPO", "Constrained PG", "PPO + invalid action masking"],
        ],
        col_widths=[35, 35, 110],
    )

    # ══ 4. DATA ══
    pdf.section_title("Data Overview", 4)
    pdf.body_text(
        "We use data4day_with_issues.csv - 4 days of hourly package sorting data from Swiss Post, "
        "containing ~144,500 records. After cleaning 691 rows with negative processing times, "
        "data is aggregated to chute-x-hour level producing 6,694 sim_states that drive demand."
    )
    pdf.sub_title("Key Columns")
    pdf.bullet("HOUR_TIME - Timestamp (hourly granularity)")
    pdf.bullet("CHUTE - Sorting lane identifier (e.g. R0101)")
    pdf.bullet("PACKAGE_COUNT - Packages in that hour/chute/ZIP combination")
    pdf.bullet("AVG_PROCESSING_TIME_MINUTES - Average processing time")

    # ══ 5. ENVIRONMENT DESIGN ══
    pdf.add_page()
    pdf.section_title("RL Environment Design", 5)
    pdf.sub_title("Action Space (5 Actions)")
    pdf.add_table(
        ["Action", "ID", "Effect", "Cost"],
        [
            ["Do Nothing", "0", "No intervention", "Free"],
            ["Add Chute", "1", "+1 active chute (more capacity)", "High"],
            ["Reroute", "2", "Reduce queue by 20-40%", "Medium"],
            ["Priority Processing", "3", "Boost processing rate +30%", "Medium"],
            ["Remove Chute", "4", "-1 chute (save resources)", "Free (saves money)"],
        ],
        col_widths=[38, 12, 78, 40],
    )
    pdf.body_text(
        "The Remove Chute action (new in v1.6) teaches the agent to scale DOWN when load is low, "
        "preventing unnecessary resource waste. A negative reward for excess chutes reinforces this: "
        "if active_chutes > 1 and chute_load < 0.3, penalty = (active_chutes - 1) * 2.0."
    )

    pdf.sub_title("Environment Progression")
    pdf.add_table(
        ["Aspect", "V1", "V2", "V3"],
        [
            ["Starting chutes", "2", "1", "1"],
            ["Max chutes", "5", "4", "4"],
            ["Demand scale", "Raw", "Amplified x20", "Curriculum"],
            ["Action masking", "No", "No", "Yes"],
            ["Actions", "5", "5", "5 (masked)"],
            ["Episode length", "100", "200", "200"],
        ],
        col_widths=[40, 40, 40, 50],
    )

    # ══ 6-8: V1, V2, V3 (condensed) ══
    pdf.add_page()
    pdf.section_title("V1: First Attempt & Lessons", 6)
    pdf.body_text(
        "V1 uses raw sim_states to drive demand. Problem: demand too low relative to capacity "
        "(load ~0.01). Agent brute-forces by always adding chutes. Lesson: need harder environment."
    )

    pdf.section_title("V2: Harder Environment", 7)
    pdf.body_text(
        "V2 amplifies demand 20x, starts with 1 chute, adds maintenance costs. "
        "Reward includes quadratic overload penalty for preemptive action. "
        "V2 results: Heuristic best (1,114), DQN/PPO still single-action (738)."
    )

    pdf.section_title("V3: Action Masking + Curriculum", 8)
    pdf.body_text(
        "V3 adds: (1) Action masking via MaskablePPO -- invalid actions blocked, "
        "(2) Reward for smart inaction (+4 if load < 0.9 and throughput > 0.6), "
        "(3) Curriculum learning in 3 phases:"
    )
    pdf.add_table(
        ["Phase", "Difficulty", "Demand Scale", "Steps", "Purpose"],
        [
            ["1. Easy", "0.25", "5x", "100K", "Learn basic mechanics"],
            ["2. Medium", "0.60", "12x", "100K", "Learn timing"],
            ["3. Hard", "1.00", "20x", "100K", "Master peak demand"],
        ],
        col_widths=[30, 28, 35, 22, 60],
    )

    # ══ 9. FROM-SCRATCH IMPLEMENTATIONS ══
    pdf.add_page()
    pdf.section_title("From-Scratch Implementations", 9)

    pdf.sub_title("9a. Tabular Q-Learning")
    pdf.body_text(
        "Q-learning is the foundation of value-based RL. The agent maintains a "
        "Q-table mapping discretized states to action values, updated via:\n"
        "  Q(s,a) += alpha * [r + gamma * max_a' Q(s',a') - Q(s,a)]\n\n"
        "Implementation: QAgent class with epsilon-greedy (1.0 -> 0.05 over 5000 episodes), "
        "alpha=0.1, gamma=0.99. Q-table shape: (10, 6, 4, 8, 5, 5) = 48,000 entries."
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_v1.3_qlearning.png"))

    pdf.sub_title("9b. SARSA Agent")
    pdf.body_text(
        "SARSA is an on-policy TD control algorithm. Unlike Q-learning which uses "
        "max_a' Q(s',a') (off-policy), SARSA uses the ACTUAL next action a' chosen by the "
        "current policy:\n"
        "  Q(s,a) += alpha * [r + gamma * Q(s',a') - Q(s,a)]\n\n"
        "This makes SARSA more conservative -- it accounts for the exploration policy's "
        "randomness. In safety-critical environments like our sorting center, SARSA tends "
        "to learn safer policies that avoid risky states."
    )
    pdf.add_table(
        ["Property", "Q-Learning", "SARSA"],
        [
            ["Policy type", "Off-policy", "On-policy"],
            ["Update target", "max_a' Q(s',a')", "Q(s', a'_actual)"],
            ["Behavior", "Optimistic", "Conservative"],
            ["Safety", "May explore risky states", "Avoids risky transitions"],
            ["Convergence", "To Q*", "To Q^pi (for current pi)"],
        ],
        col_widths=[40, 70, 70],
    )

    pdf.sub_title("9c. Deep Q-Network in PyTorch")
    pdf.body_text(
        "DQN replaces the Q-table with a neural network. Architecture: "
        "7 -> 128 -> 128 -> 5 (ReLU activations). Components: Experience Replay Buffer (50K), "
        "Target Network (updated every 1000 steps), Epsilon Decay (1.0 -> 0.05 over 200K steps). "
        "Trained with 3-phase curriculum (300K total steps)."
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_v1.3_dqn_scratch.png"))

    # ══ 10. SB3 TRAINING ══
    pdf.add_page()
    pdf.section_title("SB3 Training Strategy & Agent Hyperparameters", 10)
    pdf.add_table(
        ["Algorithm", "Type", "Key Feature", "Steps"],
        [
            ["DQN", "Value-based", "Replay buffer + target net", "300K"],
            ["A2C", "Actor-Critic", "Advantage reduces variance", "300K"],
            ["PPO", "Policy gradient", "Clipped surrogate objective", "300K"],
            ["MaskablePPO", "Constrained PG", "Invalid actions blocked", "300K"],
        ],
        col_widths=[33, 32, 72, 30],
    )
    pdf.body_text(
        "Temporal train/test split: Train on Days 1-2 (6,694 states), test on Day 4 (4,556 states). "
        "All policies evaluated on both sets. A gap < 1% proves generalization."
    )

    pdf.sub_title("Agent Hyperparameter Summary")
    pdf.body_text(
        "The following table summarizes all RL agents and their key hyperparameters:"
    )
    pdf.add_table(
        ["Agent", "Type", "alpha (LR)", "gamma", "epsilon", "Training"],
        [
            ["Q-Learning", "Tabular (scratch)", "0.1", "0.99", "1.0->0.05", "5K eps"],
            ["SARSA", "Tabular (scratch)", "0.1", "0.99", "1.0->0.05", "5K eps"],
            ["DQN (scratch)", "PyTorch NN", "5e-4", "0.99", "1.0->0.05", "300K steps"],
            ["DQN (SB3)", "Stable-Baselines3", "5e-4", "0.99", "1.0->0.05", "300K steps"],
            ["PPO (SB3)", "Policy Gradient", "3e-4", "0.99", "ent=0.01", "300K steps"],
            ["A2C (SB3)", "Actor-Critic", "7e-4", "0.99", "ent=0.01", "300K steps"],
            ["MaskablePPO", "Masked PG", "3e-4", "0.99", "ent=0.01", "300K steps"],
            ["Heuristic", "Rule-based", "--", "--", "--", "--"],
            ["Random", "Uniform", "--", "--", "--", "--"],
            ["Do Nothing", "Baseline", "--", "--", "--", "--"],
        ],
        col_widths=[30, 33, 22, 18, 22, 27],
        highlight_row=2,
    )

    pdf.sub_title("DQN (scratch) Architecture Details")
    pdf.add_table(
        ["Parameter", "Value"],
        [
            ["Network", "7 -> 128 -> 128 -> 5 (ReLU)"],
            ["Optimizer", "Adam (lr=5e-4)"],
            ["Replay buffer", "50,000 transitions"],
            ["Batch size", "64"],
            ["Target net update", "Every 250 steps"],
            ["Epsilon decay", "Linear over 100K steps"],
        ],
        col_widths=[55, 100],
    )

    pdf.sub_title("SB3 Algorithm-Specific Settings")
    pdf.add_table(
        ["Parameter", "DQN", "PPO", "A2C", "MaskablePPO"],
        [
            ["Batch size", "64", "64", "N/A", "64"],
            ["Buffer/n_steps", "50,000", "512", "5", "512"],
            ["n_epochs", "--", "10", "--", "10"],
            ["Entropy coef", "--", "0.01", "0.01", "0.01"],
            ["Value func coef", "--", "--", "0.5", "--"],
            ["Target update", "250", "--", "--", "--"],
            ["Exploration frac", "0.4", "--", "--", "--"],
        ],
        col_widths=[35, 30, 30, 30, 35],
    )

    # ══ 11. RESULTS ══
    pdf.add_page()
    pdf.section_title("Results & Evaluation", 11)

    pdf.sub_title("10-Policy Comparison (Test Set)")
    pdf.add_table(
        ["Policy", "Reward", "Delay", "Overload %"],
        [
            ["DQN (scratch)", "1,864", "0.49h", "0.1%"],
            ["Heuristic", "1,834", "0.47h", "0.6%"],
            ["Ensemble", "1,593", "0.65h", "2.2%"],
            ["DQN-v3 (SB3)", "1,526", "0.72h", "3.9%"],
            ["PPO-v3", "1,500", "0.44h", "2.2%"],
            ["MaskablePPO", "1,481", "0.62h", "4.6%"],
            ["A2C-v3", "1,442", "0.36h", "1.1%"],
            ["Random", "694", "0.24h", "0.8%"],
            ["Always Add Chute", "739", "0.20h", "0.0%"],
        ],
        col_widths=[40, 30, 30, 30],
        highlight_row=0,
    )
    pdf.body_text(
        "Key finding: the from-scratch DQN (PyTorch) outperforms all agents including "
        "the hand-crafted heuristic (1,864 vs 1,834)."
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_v1.3_results.png"))

    pdf.add_page()
    pdf.sub_title("Episode Deep Dive")
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_v1.3_episode_trace.png"))

    # ══ 12. POLICY HEATMAP ══
    pdf.add_page()
    pdf.section_title("Policy Heatmap Analysis", 12)
    pdf.body_text(
        "Inspired by 02_mountain_car/src/viz.py plot_policy() function. For each point in the "
        "(chute_load, queue_length) space, we query each trained agent for its preferred action "
        "and visualize the resulting decision surface. This reveals interpretable decision "
        "boundaries: when to add chutes vs reroute vs wait."
    )
    pdf.add_table(
        ["Region", "Preferred Action", "Why"],
        [
            ["Low load, low queue", "Nothing / Remove Chute", "System healthy, save resources"],
            ["High load, low queue", "Add Chute", "Capacity crunch, scale up"],
            ["Low load, high queue", "Reroute", "Divert to prevent build-up"],
            ["High load, high queue", "Add Chute + Reroute", "Emergency: all measures"],
        ],
        col_widths=[45, 55, 80],
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_policy_heatmap.png"))

    # ══ 13. HP GRID SEARCH ══
    pdf.add_page()
    pdf.section_title("Hyperparameter Grid Search", 13)
    pdf.body_text(
        "Inspired by 01_taxi/03_q_agent_hyperparameters_analysis.ipynb. We systematically "
        "vary the learning rate (alpha) and discount factor (gamma) for the tabular Q-learning "
        "agent and compare performance across a 3x3 grid."
    )
    pdf.add_table(
        ["Parameter", "Values Tested", "Best Value"],
        [
            ["alpha (learning rate)", "0.01, 0.1, 0.5", "See heatmap"],
            ["gamma (discount factor)", "0.8, 0.95, 0.99", "See heatmap"],
            ["Training episodes", "2,000 per combo", "Fixed"],
            ["Metric", "Avg reward (last 200)", "Higher = better"],
        ],
        col_widths=[50, 60, 55],
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_hp_grid_search.png"))

    # ══ 14. MULTI-RUN EVAL ══
    pdf.add_page()
    pdf.section_title("Multi-Run Statistical Evaluation", 14)
    pdf.body_text(
        "Inspired by 01_taxi/src/loops.py train_many_runs(). Single-run results can be noisy "
        "due to stochastic demand. We run each policy evaluation 5 times with different random "
        "seeds and report mean +/- std for statistical confidence."
    )
    pdf.body_text(
        "This ensures our policy rankings are robust and not artifacts of lucky/unlucky "
        "random seeds. Error bars quantify the variance inherent in each policy."
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_multirun_eval.png"))

    # ══ 15. MODEL SAVE/LOAD ══
    pdf.section_title("Model Persistence - Save & Load", 15)
    pdf.body_text(
        "Inspired by 03_cart_pole/src/q_agent.py save_to_disk/load_from_disk. All trained agents "
        "are saved to the saved_models/ directory for reuse without retraining:"
    )
    pdf.add_table(
        ["Agent", "Format", "Contents"],
        [
            ["SB3 DQN/PPO/A2C/MaskablePPO", ".zip", "Full model with optimizer state"],
            ["Q-Learning (from scratch)", ".json", "Q-table + hyperparameters"],
            ["SARSA (from scratch)", ".json", "Q-table + hyperparameters"],
            ["DQN (from scratch)", ".pt", "PyTorch weights + config"],
        ],
        col_widths=[55, 25, 95],
    )

    # ══ 16. COST-BENEFIT ══
    pdf.add_page()
    pdf.section_title("Cost-Benefit Analysis", 16)
    pdf.add_table(
        ["Cost Item", "Estimate", "Source"],
        [
            ["Chute activation", "CHF 50/activation", "Equipment + staffing"],
            ["Chute maintenance", "CHF 25/hour/chute", "Labor + electricity"],
            ["Package rerouting", "CHF 2/package", "Extra handling"],
            ["Priority processing", "CHF 15/hour", "Overtime premium"],
            ["Delayed package penalty", "CHF 5/package-hour", "SLA penalty"],
            ["Overload incident", "CHF 200/incident", "Disruption + recovery"],
        ],
        col_widths=[50, 55, 60],
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_v1.3_cost_analysis.png"))

    # ══ 17. SIMULATION DEMO ══
    pdf.add_page()
    pdf.section_title("Visual Simulation Demo", 17)
    pdf.body_text(
        "A lightweight SortingCenterSim class simulates a 48-hour sorting center shift. "
        "Two scenarios run side-by-side: (1) No Intervention -- system runs unmanaged, "
        "(2) RL Agent -- a trained policy makes real-time decisions."
    )
    pdf.body_text(
        "The simulation uses real Swiss Post hourly demand patterns and stochastic "
        "package arrivals (Poisson distribution). The RL agent demonstrates learned "
        "behaviors: adding chutes before peak hours, rerouting during congestion, "
        "removing chutes during low demand, and strategic inaction."
    )
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_simulation_comparison.png"))
    pdf.add_page()
    pdf.sub_title("Zoomed Critical Window")
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_simulation_zoomed.png"))
    pdf.sub_title("Sorting Center Schematic")
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_sorting_center_schematic.png"))
    pdf.sub_title("Impact Summary")
    pdf.add_image_if_exists(os.path.join(img_dir, "rl_simulation_impact.png"))

    # ══ 18. LIVE ANIMATION ══
    pdf.add_page()
    pdf.section_title("Interactive Live Animation", 18)
    pdf.body_text(
        "The notebook includes an interactive FuncAnimation (matplotlib.animation) that "
        "renders a 48-frame animation of the sorting center with play/pause/scrub controls. "
        "Uses to_jshtml() for inline notebook playback."
    )
    pdf.body_text(
        "Features: dark theme dashboard, package dot visualization, queue fill bar, "
        "chute status indicators, action badges, real-time load timeline chart, "
        "ALARM! overlay when the unmanaged side overloads."
    )
    pdf.sub_title("RL Formalism Mapping")
    pdf.body_text(
        "The animation is accompanied by a formal MDP mapping showing how each visual "
        "element corresponds to RL theory: state observations, action selections, "
        "transition dynamics, rewards, and the Bellman equation."
    )
    pdf.add_table(
        ["RL Concept", "In This Simulation"],
        [
            ["State s_t", "(queue, load, active_chutes, processing_rate, hour)"],
            ["Action a_t", "{Wait, Add Chute, Reroute, Priority, Remove Chute}"],
            ["Transition P(s'|s,a)", "Sim physics: queue += incoming - processed"],
            ["Reward r_t", "-load penalty + throughput bonus"],
            ["Policy pi(a|s)", "Rule-based (mirrors trained DQN behavior)"],
            ["Return G_0", "Cumulative discounted reward (gamma=0.99)"],
        ],
        col_widths=[45, 140],
    )

    # ══ 19. CONCLUSIONS ══
    pdf.add_page()
    pdf.section_title("Conclusions & Business Recommendations", 19)

    pdf.sub_title("What We Learned")
    pdf.bullet("Implementing Q-learning, SARSA, and DQN manually reveals the mechanics hidden by SB3.",
               bold_prefix="From-scratch builds understanding: ")
    pdf.bullet("The from-scratch DQN outperformed SB3 DQN and the hand-crafted heuristic.",
               bold_prefix="Custom training beats defaults: ")
    pdf.bullet("SARSA's on-policy conservatism is valuable in safety-critical operations.",
               bold_prefix="SARSA vs Q-learning trade-off: ")
    pdf.bullet("Policy heatmaps reveal interpretable decision boundaries.",
               bold_prefix="Interpretability through visualization: ")
    pdf.bullet("Multi-run averaging with different seeds confirms ranking robustness.",
               bold_prefix="Statistical rigor: ")
    pdf.bullet("Removing the 'do nothing' penalty was the single most impactful change.",
               bold_prefix="Reward shaping matters: ")
    pdf.bullet("Negative reward for excess chutes teaches the agent to scale DOWN.",
               bold_prefix="Remove Chute action: ")
    pdf.ln(3)

    pdf.sub_title("Algorithm Coverage")
    pdf.add_table(
        ["Method", "Our Implementation"],
        [
            ["Q-learning", "From-scratch QAgent with Q-table"],
            ["SARSA", "From-scratch SARSAAgent (NEW in v1.6)"],
            ["DQN", "From-scratch PyTorch + SB3 DQN"],
            ["A2C", "SB3 Advantage Actor-Critic"],
            ["PPO", "SB3 PPO + MaskablePPO"],
            ["MDP theory", "Explicit formulation + RL formalism section"],
            ["HP tuning", "Grid search over alpha x gamma (NEW)"],
            ["Evaluation", "Multi-run avg + temporal split (NEW)"],
            ["Model persistence", "Save/load all agents (NEW)"],
            ["Visualization", "Policy heatmap + sim demo + animation (NEW)"],
        ],
        col_widths=[55, 130],
    )

    pdf.sub_title("Business Recommendations for Swiss Post")
    pdf.bullet("Deploy DQN agent for real-time sorting decisions - 98% reduction in overloaded hours.",
               bold_prefix="1. Deploy: ")
    pdf.bullet("Monitor action distributions - if agent only uses 1 action, retrain with reward shaping.",
               bold_prefix="2. Monitor: ")
    pdf.bullet("Start with heuristic fallback - use RL suggestions with human override during pilot.",
               bold_prefix="3. Pilot: ")
    pdf.bullet("Retrain seasonally - demand patterns change (holiday peaks, etc.).",
               bold_prefix="4. Retrain: ")
    pdf.bullet("Scale to multi-center - train one agent per sorting center with shared curriculum.",
               bold_prefix="5. Scale: ")
    pdf.ln(3)

    pdf.sub_title("Future Work")
    pdf.add_table(
        ["Improvement", "Expected Impact"],
        [
            ["Continuous actions (DDPG/TD3)", "Fine-grained control for continuous spaces"],
            ["LSTM integration", "Feed demand predictions as observations"],
            ["Multi-agent RL", "One agent per chute/zone"],
            ["Optuna HP search", "Bayesian optimization (like chatbot project)"],
            ["Finer time granularity", "15-min intervals instead of hourly"],
        ],
        col_widths=[55, 130],
    )

    pdf.sub_title("Final Takeaway")
    pdf.body_text(
        "v1.6 is a unified, comprehensive RL pipeline that is: (1) theoretically grounded with "
        "from-scratch Q-learning, SARSA, and DQN implementations, (2) methodologically broad "
        "covering value-based, actor-critic, and policy gradient methods, (3) data-driven using real Swiss Post data, "
        "(4) comprehensive with 7+ trained agents + ensemble + baselines, (5) scientifically "
        "rigorous with multi-run evaluation and temporal splits, (6) interpretable with policy "
        "heatmaps and simulation demos, and (7) business-ready with CHF cost-benefit analysis. "
        "All work consolidated in a single notebook for reproducibility."
    )

    # ══ SAVE ══
    out_path = os.path.join(img_dir, "RL_Project_Report_v1.6.pdf")
    pdf.output(out_path)
    print(f"PDF saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_report()
