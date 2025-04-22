import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

class CurrentAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        with h5py.File(self.filename, 'r') as f:
            # lê parâmetros de malha e tempo
            self.dt = f.attrs['dt']
            nit = int(f.attrs['Iterations'])
            self.t = np.linspace(0, (nit - 1) * self.dt, nit)
            # passos espaciais (se precisar)
            dx_dy_dz = np.array(f.attrs['dx_dy_dz'])
            self.dy, self.dz = 2*dx_dy_dz[1], 2*dx_dy_dz[2]

            # parâmetros da fonte devem estar gravados como atributos no .out
            # (adapte ao nome exato que você usar ao gravar)
            self.I0 = f.attrs.get('I0', 1.0)   # valor de pico (A)
            self.a  = f.attrs.get('a', 1e4)    # s^-1
            self.b  = f.attrs.get('b', 5e7)    # s^-1

            # monta vetor de corrente via Ampère
            rxs = list(f['/rxs'].keys())
            if len(rxs) < 4:
                raise ValueError(f"São necessários ≥4 receptores, achei só {len(rxs)}")
            Hy1 = f[f'/rxs/{rxs[0]}/Hy'][:]
            Hz1 = f[f'/rxs/{rxs[1]}/Hz'][:]
            Hy2 = f[f'/rxs/{rxs[2]}/Hy'][:]
            Hz2 = f[f'/rxs/{rxs[3]}/Hz'][:]
            self.current = self.dy*(Hy1 - Hy2) + self.dz*(Hz1 - Hz2)

    def analytical(self):
        """Retorna I(t) = I0 (e^{-a t} - e^{-b t}) no mesmo vetor de tempo."""
        return self.I0 * (np.exp(-self.a * self.t) - np.exp(-self.b * self.t))

    def plot(self, title=r'Corrente no cabo nu amostrada em $x=0$ $m$', save=False, outname=None):
        plt.figure(figsize=(10, 5))
        # curva numérica
        plt.plot(self.t*1e6, self.current,    lw=2, label='gprMax')
        # curva analítica
        plt.plot(self.t*1e6, self.analytical(), '--', lw=2, label=r"$I(t) = I_0(e^{-a t} - e^{-b t})$")
        plt.xlabel('Tempo [µs]')
        plt.ylabel('Corrente [A]')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        if save and outname:
            plt.savefig(outname, dpi=300)
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analisa corrente via Ampère e compara com o analítico'
    )
    parser.add_argument('outputfile', help='arquivo .out do gprMax')
    parser.add_argument('--save', action='store_true', help='salvar figura')
    args = parser.parse_args()

    analyzer = CurrentAnalyzer(args.outputfile)
    base = os.path.splitext(os.path.basename(args.outputfile))[0]
    fig_name = f'{base}_current_compare.png' if args.save else None
    analyzer.plot(save=args.save, outname=fig_name)
