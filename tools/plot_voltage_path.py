# Copyright (C) 2025: Adilton Júnio
# Adaptado com base no utilitário original do gprMax (University of Edinburgh)
# Código atualizado para adaptar automaticamente à quantidade real de receptores existentes

import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os


def compute_voltage_from_field_auto(filename, output_component='Ez', dz=1.0):
    """
    Calcula a tensão induzida integrando o campo elétrico Ez ao longo da direção z,
    adaptando-se automaticamente à quantidade real de receptores contidos no arquivo.

    Parâmetros:
        filename (str): caminho para o arquivo .out do gprMax
        output_component (str): componente do campo a ser integrado ('Ez')
        dz (float): passo entre os receptores

    Retorno:
        t (np.ndarray): vetor de tempo
        voltage_vs_time (np.ndarray): tensão ao longo do tempo
    """
    f = h5py.File(filename, 'r')
    dt = f.attrs['dt']
    n_iterations = f.attrs['Iterations']
    t = np.linspace(0, (n_iterations - 1) * dt, num=n_iterations)

    rx_group = f['/rxs']
    ez_along_path = []

    for rx_name in rx_group:
        rx_path = f'/rxs/{rx_name}/{output_component}'
        if output_component in f[f'/rxs/{rx_name}']:
            ez_along_path.append(f[rx_path][:])
        else:
            raise KeyError(f"Componente '{output_component}' não encontrada em {rx_name}")

    f.close()

    ez_along_path = np.array(ez_along_path)
    voltage_vs_time = -np.trapezoid(ez_along_path, dx=dz, axis=0)

    return t, voltage_vs_time


def plot_voltage(t, voltage, title='Tensão induzida por integração de $E_z$', save=False, filename=None):
    plt.figure(figsize=(10, 5))
    plt.plot(t * 1e6, voltage, lw=2)
    plt.xlabel('Tempo [µs]')
    plt.ylabel('Tensão [V]')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    if save and filename:
        plt.savefig(filename, dpi=300)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Calcula e plota a tensão no fio enterrado por integração automática de Ez nos receptores verticais.'
    )
    parser.add_argument('outputfile', help='Caminho do arquivo .out gerado pelo gprMax')
    parser.add_argument('--dz', type=float, default=1.0, help='Passo de espaçamento entre receptores (default=1.0)')
    parser.add_argument('--save', action='store_true', help='Salvar figura em arquivo PNG')

    args = parser.parse_args()

    t, voltage = compute_voltage_from_field_auto(args.outputfile, dz=args.dz)

    outname = os.path.splitext(os.path.basename(args.outputfile))[0]
    fig_name = f'{outname}_voltage.png' if args.save else None
    plot_voltage(t, voltage, save=args.save, filename=fig_name)
