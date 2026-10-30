"""Generate a GitHub-friendly Markdown report from robot simulation history."""

from pathlib import Path

from robot_lab.worlds.house import ROOMS


def generate_experiment_report(history, file_path):
    """Write a Markdown experiment report and return its Path.

    Args:
        history: Nonempty records from RobotSimulation.get_history().
            Each record contains step, action, true_position, and belief.
        file_path: Destination file path (str or pathlib.Path).

    The report is generated from the provided history, not fixed example data.
    """
    if not history:
        raise ValueError("history must contain at least an initial state")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    first_record = history[0]
    last_record = history[-1]
    initial_belief = first_record["belief"]
    final_belief = last_record["belief"]
    actions = [str(record["action"]) for record in history[1:]]
    total_steps = len(history) - 1
    final_step = last_record["step"]
    most_likely_room = max(ROOMS, key=final_belief.get)
    most_likely_probability = final_belief[most_likely_room]
    total_probability = sum(final_belief[room] for room in ROOMS)

    def latex_room(room):
        # Escape common LaTeX-sensitive characters in room names.
        name = str(room).replace("\\", r"\textbackslash{}")
        for old, new in (("_", r"\_"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#")):
            name = name.replace(old, new)
        return rf"\text{{{name}}}"

    lines = [
        f"# Robot Intelligence Lab — {path.stem.replace('_', ' ').title()}",
        "",
        "**Experiment type:** Stochastic robot motion and Markov belief prediction  ",
        "**Environment:** Five-room discrete state space",
        "",
        "## 1. Experiment Objective",
        "",
        "This experiment examines how uncertainty in robot motion propagates "
        "through a sequence of discrete actions. The simulator samples a "
        "ground-truth position while independently predicting a probability "
        "distribution over possible locations.",
        "",
        "## 2. Initial Conditions",
        "",
        f"**Initial ground-truth position:** `{first_record['true_position']}`",
        "",
        "The initial belief distribution, in the room order shown below, is:",
        "",
        "$$",
        r"\mathbf{b}_0 = \begin{bmatrix} "
        + " & ".join(f"{initial_belief[room]:.4f}" for room in ROOMS)
        + r" \end{bmatrix}",
        "$$",
        "",
        "**State order:** " + " → ".join(f"`{room}`" for room in ROOMS),
        "",
        "### Markov Motion Prediction",
        "",
        "The belief is propagated using the transition probabilities "
        "associated with each commanded action:",
        "",
        "$$",
        r"b_{t+1}(x') = \sum_{x \in \mathcal{X}} P(x' \mid x,a_t)\,b_t(x)",
        "$$",
        "",
        "For a row-vector belief and row-stochastic transition matrix:",
        "",
        "$$",
        r"\mathbf{b}_{t+1} = \mathbf{b}_t\mathbf{T}_{a_t}",
        "$$",
        "",
        "## 3. Action Sequence",
        "",
        " → ".join(f"`{action}`" for action in actions)
        if actions else "No movement commands were executed.",
        "",
        f"**Number of actions:** ${total_steps}$",
        "",
        "## 4. Simulation Results",
        "",
        "The following positions are **sampled ground truth** for this run "
        "and may change across runs:",
        "",
        "| Step | Action | Ground-Truth Position |",
        "|---|---|---|",
    ]

    for record in history:
        # Preserve the original report table contract for existing consumers.
        lines.append(
            f"| {record['step']} | {record['action']} | "
            f"{record['true_position']} |"
        )

    lines.extend([
        "",
        "## 5. Final Belief Distribution",
        "",
        f"The predicted belief after step ${final_step}$ is:",
        "",
        "| State | Predicted Probability |",
        "|---|---:|",
    ])

    for room in ROOMS:
        lines.append(f"| {room} | ${final_belief[room]:.4f}$ |")

    terms = " + ".join(f"{final_belief[room]:.4f}" for room in ROOMS)
    lines.extend([
        "",
        "### Probability Normalization",
        "",
        "$$",
        rf"\sum_{{x \in \mathcal{{X}}}} b_{{{final_step}}}(x) "
        rf"= {terms} = {total_probability:.4f}",
        "$$",
        "",
        "### Most Probable State",
        "",
        "$$",
        rf"x_{{\mathrm{{MAP}}}} = \arg\max_{{x \in \mathcal{{X}}}} "
        rf"b_{{{final_step}}}(x) = {latex_room(most_likely_room)}",
        "$$",
        "",
        "$$",
        rf"P(X_{{{final_step}}} = {latex_room(most_likely_room)}) "
        rf"= {most_likely_probability:.4f}",
        "$$",
        "",
        "## 6. Experiment Evaluation",
        "",
        "| Metric | Result |",
        "|---|---|",
        f"| Number of actions | {total_steps} |",
        f"| Initial ground-truth position | {first_record['true_position']} |",
        f"| Final ground-truth position | {last_record['true_position']} |",
        f"| Most probable predicted position | {most_likely_room} |",
        f"| Maximum belief probability | ${most_likely_probability:.4f}$ |",
        f"| Sum of belief probabilities | ${total_probability:.4f}$ |",
        "",
        "**Ground truth vs. belief:** The robot's actual position is "
        "sampled from its motion model; the predicted belief is calculated "
        "over all possible states without reading that sampled position.",
        "",
        "## 7. Conclusion",
        "",
        f"After **{total_steps}** commanded movement(s), the sampled robot "
        f"position was **{last_record['true_position']}**. The highest "
        f"predicted belief was assigned to **{most_likely_room}** "
        f"(${most_likely_probability:.4f}$). "
        "The belief distribution describes uncertainty rather than "
        "directly revealing the robot's true location.",
        "",
    ])

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
