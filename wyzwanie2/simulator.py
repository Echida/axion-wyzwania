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

def uygula(durum, kapi, hedef):
    """Apply a single-qubit gate to qubit `hedef` (0 = left, 1 = right) of a 2-qubit state."""
    buyuk = np.kron(kapi, I) if hedef == 0 else np.kron(I, kapi)
    return buyuk @ durum

def olc(durum, shots=1000):
    """Measure `shots` times: sample basis labels with Born-rule probabilities and count them."""
    olasilik = np.abs(durum) ** 2
    n = int(np.log2(len(durum)))
    etiketler = [format(i, f"0{n}b") for i in range(len(durum))]
    sonuclar = np.random.choice(etiketler, size=shots, p=olasilik)
    return {e: int(np.sum(sonuclar == e)) for e in etiketler}

if __name__ == "__main__":
    # Test 1: H·H|0> = |0>
    assert np.allclose(H @ (H @ ket0), ket0), "Test 1 failed"
    print("Test 1 passed: H·H|0> = |0>")

    # Test 2: Bell state gives only 00 and 11
    bell = CNOT @ uygula(ket00, H, 0)
    sayim = olc(bell, shots=1000)
    print("Bell measurement:", sayim)
    assert sayim["01"] == 0 and sayim["10"] == 0, "Test 2 failed"
    print("Test 2 passed: only 00 and 11")
