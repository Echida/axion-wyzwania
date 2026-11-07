# Challenge 3 — Does the CNOT help? It depends on the data

## 1. Hypothesis (written and committed BEFORE running any experiment)

**Area:** Ansatz (lecture slides 16–22).

**Model:** the variational classifier from slide 31: two qubits, angle encoding RY(x₁), RY(x₂),
ansatz RY(θ₁), RY(θ₂), CNOT(q₀ → q₁), RY(θ₃), RY(θ₄), measure ⟨Z₀⟩, predict ŷ = sign(f).
The "no-CNOT" model is identical except that the CNOT is removed.

**Hypothesis:** The usefulness of the CNOT depends on the *type* of the data.
- If the label depends on only one feature, the CNOT is unnecessary and can even mislead the model,
  because it mixes in information from x₂ that is irrelevant.
- If the label depends on the *combination* of both features, the model without the CNOT cannot see x₂
  at all (only q₀ is measured), so it can only guess; the CNOT model can use both features.

**Datasets** (synthetic, features drawn uniformly from [0, π]):
- **Rule A (single feature):** y = +1 if x₁ > π/2, otherwise y = −1.
- **Rule B (joint features):** y = +1 if x₁ and x₂ are on the same side of π/2, otherwise y = −1.

**Prediction (test accuracy after training):**

|            | without CNOT | with CNOT |
|------------|--------------|-----------|
| Rule A     | ~75 %        | ~60 %     |
| Rule B     | ~50 %        | ~75 %     |

**What counts as "the prediction held":**
1. Ordering: on Rule A, no-CNOT ≥ CNOT; on Rule B, CNOT > no-CNOT, and no-CNOT is close to chance (≤ 60 %).
2. Each measured accuracy is within ±10 percentage points of the predicted value.
   Rationale: with 100 test points and true accuracy ≈ 75 %, the sampling standard deviation is
   √(0.75·0.25/100) ≈ 4.3 points; ±10 ≈ 2 standard deviations, i.e. the range explainable by test-set chance alone.

### 1b. Secondary experiment: depth L = 3

**Idea:** like adding neurons in a classical network, repeating the ansatz block (RY + CNOT + RY, slide 18)
three times should raise accuracy in every case.

**Prediction (test accuracy, L = 3):**

|            | without CNOT | with CNOT |
|------------|--------------|-----------|
| Rule A     | ~80 %        | ~70 %     |
| Rule B     | ~60 %        | ~80 %     |

Note on Rule B without CNOT: q₀ still cannot see x₂, so the model has no real way to learn the rule;
any accuracy above 50 % would come from chance agreement ("a broken clock is right twice a day").

**Held if:** each L = 3 accuracy is ≥ the corresponding L = 1 accuracy, and within ±10 points of the value above.

## 2. Experimental setup (fixed in advance)

- 200 training points, 100 test points per rule; same points for both models.
- Training: parameter-shift gradients (slide 39), MSE loss (slide 34), plain gradient descent, lr = 0.1, 50 epochs (slide 47).
- Initial θ drawn from U(−0.1, 0.1).
- Exact expectation values (StatevectorEstimator); 5 random seeds, report mean ± std.
- Plots: learning curves (loss, accuracy per epoch) and decision maps over the (x₁, x₂) square.

## 3. Results

_To be filled in after the experiment._

## 4. Did the prediction hold?

_To be filled in after the experiment._

## 5. What would change if…

…the CNOT direction were reversed (control q₁, target q₀)?

**Prediction (written before running the extra experiment; L = 1, with CNOT, 5 seeds):**
- Rule A: ~50 %. The measured qubit q₀ now depends directly on x₂, which is irrelevant for Rule A and should confuse the model.
- Rule B: ~62 % (same as the normal direction). Rule B depends symmetrically on both features, so the direction of the CNOT should not matter.
