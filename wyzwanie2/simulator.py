"""Mini quantum simulator (AXION Wyzwanie 2).
State = numpy vector, gates = matrices, measurement = sampling from |amplitude|^2.
Qubit order: |q0 q1>, q0 is the LEFT digit, CNOT control = q0."""
import numpy as np

# basis states
ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)
ket00 = np.kron(ket0, ket0)

# single-qubit gates
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

def Ry(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)

# two-qubit gate: control q0, target q1
CNOT = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]], dtype=complex)

def apply_gate(state, gate, target):
    """Apply a single-qubit gate to qubit `target` (0 = left, 1 = right) of a 2-qubit state."""
    full = np.kron(gate, I) if target == 0 else np.kron(I, gate)
    return full @ state

def measure(state, shots=1000):
    """Measure `shots` times: sample basis labels with Born-rule probabilities and count them."""
    probs = np.abs(state) ** 2
    n = int(np.log2(len(state)))
    labels = [format(i, f"0{n}b") for i in range(len(state))]
    outcomes = np.random.choice(labels, size=shots, p=probs)
    return {l: int(np.sum(outcomes == l)) for l in labels}

if __name__ == "__main__":
    # Test 1: H·H|0> = |0>
    assert np.allclose(H @ (H @ ket0), ket0), "Test 1 failed"
    print("Test 1 passed: H·H|0> = |0>")

    # Test 2: Bell state gives only 00 and 11
    bell = CNOT @ apply_gate(ket00, H, 0)
    counts = measure(bell, shots=1000)
    print("Bell measurement:", counts)
    assert counts["01"] == 0 and counts["10"] == 0, "Test 2 failed"
    print("Test 2 passed: only 00 and 11")
