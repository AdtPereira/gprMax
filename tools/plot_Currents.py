#!/usr/bin/env python
# coding: utf-8
# -*- Python -*-
# Copyright (C) 2015-2025: Adilton Júnio
# Script para plotar apenas as correntes Ix, Iy e Iz de cada receptor de um arquivo .out do gprMax

import sys  
import argparse
import h5py
import numpy as np
import matplotlib.pyplot as plt
from gprMax.exceptions import CmdInputError

def plot_currents(filename):
    """
    Abre o arquivo .out do gprMax e plota somente as correntes Ix, Iy e Iz
    (se disponíveis) de cada receptor em função do tempo.
    """
    with h5py.File(filename, 'r') as f:
        nrx = f.attrs.get('nrx', 0)
        if nrx == 0:
            raise CmdInputError(f'No receivers found in {filename}')

        dt = f.attrs['dt']
        iterations = f.attrs['Iterations']
        time = np.linspace(0, (iterations - 1) * dt, iterations)

        for rx in range(1, nrx + 1):
            path = f'/rxs/rx{rx}/'
            available = set(f[path].keys())
            currents = [c for c in ('Ix', 'Iy', 'Iz') if c in available]
            if not currents:
                continue  # pula receptor sem correntes

            fig, ax = plt.subplots(figsize=(10, 4))
            for curr in currents:
                data = f[f'{path}{curr}'][:]
                ax.plot(time, data, label=curr)
            ax.set_xlabel('Time [s]')
            ax.set_ylabel('Current [A]')
            ax.set_title(f'Receptor rx{rx} — correntes')
            ax.grid(which='both', linestyle='-.')
            ax.legend()

        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plota apenas correntes Ix, Iy e Iz de cada receptor em um arquivo .out do gprMax'
    )
    parser.add_argument('outputfile', help='Nome do arquivo .out, incluindo o caminho')
    args = parser.parse_args()

    try:
        plot_currents(args.outputfile)
    except CmdInputError as e:
        print(f'Erro: {e}')
        sys.exit(1)
