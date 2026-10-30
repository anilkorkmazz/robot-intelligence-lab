# Robot Intelligence Lab — Experiment 001

**Experiment type:** Stochastic robot motion and Markov belief prediction  
**Environment:** Five-room discrete state space

## 1. Experiment Objective

This experiment examines how uncertainty in robot motion propagates through a sequence of discrete actions. The simulator samples a ground-truth position while independently predicting a probability distribution over possible locations.

## 2. Initial Conditions

**Initial ground-truth position:** `Office`

The initial belief distribution, in the room order shown below, is:

$$
\mathbf{b}_0 = \begin{bmatrix} 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 \end{bmatrix}
$$

**State order:** `Living Room` → `Kitchen` → `Office` → `Hallway` → `Dining Room`

### Markov Motion Prediction

The belief is propagated using the transition probabilities associated with each commanded action:

$$
b_{t+1}(x') = \sum_{x \in \mathcal{X}} P(x' \mid x,a_t)\,b_t(x)
$$

For a row-vector belief and row-stochastic transition matrix:

$$
\mathbf{b}_{t+1} = \mathbf{b}_t\mathbf{T}_{a_t}
$$

## 3. Action Sequence

`RIGHT` → `RIGHT` → `UP`

**Number of actions:** $3$

## 4. Simulation Results

The following positions are **sampled ground truth** for this run and may change across runs:

| Step | Action | Ground-Truth Position |
|---|---|---|
| 0 | START | Office |
| 1 | RIGHT | Hallway |
| 2 | RIGHT | Dining Room |
| 3 | UP | Kitchen |

## 5. Final Belief Distribution

The predicted belief after step $3$ is:

| State | Predicted Probability |
|---|---:|
| Living Room | $0.2560$ |
| Kitchen | $0.5120$ |
| Office | $0.0400$ |
| Hallway | $0.0640$ |
| Dining Room | $0.1280$ |

### Probability Normalization

$$
\sum_{x \in \mathcal{X}} b_{3}(x) = 0.2560 + 0.5120 + 0.0400 + 0.0640 + 0.1280 = 1.0000
$$

### Most Probable State

$$
x_{\mathrm{MAP}} = \arg\max_{x \in \mathcal{X}} b_{3}(x) = \text{Kitchen}
$$

$$
P(X_{3} = \text{Kitchen}) = 0.5120
$$

## 6. Experiment Evaluation

| Metric | Result |
|---|---|
| Number of actions | 3 |
| Initial ground-truth position | Office |
| Final ground-truth position | Kitchen |
| Most probable predicted position | Kitchen |
| Maximum belief probability | $0.5120$ |
| Sum of belief probabilities | $1.0000$ |

**Ground truth vs. belief:** The robot's actual position is sampled from its motion model; the predicted belief is calculated over all possible states without reading that sampled position.

## 7. Conclusion

After **3** commanded movement(s), the sampled robot position was **Kitchen**. The highest predicted belief was assigned to **Kitchen** ($0.5120$). The belief distribution describes uncertainty rather than directly revealing the robot's true location.
