import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros da fonte dupla exponencial ---
I0 = 1.0               # valor de pico (A)
a = 1e4                # s^-1
b = 5e7                # s^-1

# --- Domínio temporal ---
t_max = 5e-6        # 5 µs
dt = 1.92583e-09    # passo de tempo (1 ns)
N = int(t_max / dt) + 1

t = np.linspace(0, t_max, N)
I = I0 * (np.exp(-a * t) - np.exp(-b * t))
print(f"Tamanho do vetor de tempo: {len(t)}")

# --- Salva no formato gprMax ---
with open("double_exponential_a.txt", "w") as f:
    f.write("double_exp\n")
    for ti, Ii in zip(t, I):
        f.write(f"{Ii:.6e}\n")

# --- Salva no formato gprMax ---
# with open("double_exponential.txt", "w") as f:
#     f.write("time double_exp\n")
#     for ti, Ii in zip(t, I):
#         f.write(f"{ti:.3e} {Ii:.6e}\n")

print("Arquivo 'double_exponential_a.txt' salvo.")

# --- Geração do gráfico ---
plt.figure(figsize=(8, 4))
plt.plot(t * 1e6, I, label=r"$I(t) = I_0(e^{-a t} - e^{-b t})$")
plt.title("Fonte dupla exponencial")
plt.xlabel("Tempo (µs)")
plt.ylabel("Corrente (A)")
plt.xlim(0, t_max * 1e6)
plt.ylim(0, 1.1 * I0)
plt.grid(False)
plt.legend()
plt.tight_layout()
plt.show()
