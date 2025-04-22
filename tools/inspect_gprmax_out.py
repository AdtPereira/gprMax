import h5py
import argparse


def print_attrs(attrs, indent=2):
    for attr, value in attrs.items():
        print(" " * indent + f"- {attr}: {value}")


def inspect_gprmax_out(filename):
    with h5py.File(filename, 'r') as f:
        print(f"\n📂 Arquivo: {filename}")
        print("\n🔧 Atributos globais:")
        print_attrs(f.attrs)

        # Receptores
        if 'rxs' in f:
            print("\n📡 Receptores encontrados:")
            for rx in f['rxs']:
                rx_group = f[f'rxs/{rx}']
                name = rx_group.attrs.get('Name', rx)
                pos = rx_group.attrs.get('Position', None)
                print(f"  ▶ {rx}:")
                print(f"     - Nome     : {name}")
                print(f"     - Posição  : {tuple(pos) if pos is not None else 'Não disponível'}")
                print(f"     - Componentes disponíveis:")
                for comp in rx_group.keys():
                    print(f"        • {comp}")

        # Fontes
        if 'srcs' in f:
            print("\n🔌 Fontes encontradas:")
            for src in f['srcs']:
                src_group = f[f'srcs/{src}']
                typ = src_group.attrs.get('Type', 'Desconhecido')
                pos = src_group.attrs.get('Position', None)
                print(f"  ▶ {src}:")
                print(f"     - Tipo     : {typ}")
                print(f"     - Posição  : {tuple(pos) if pos is not None else 'Não disponível'}")

        # Linhas de Transmissão
        if 'tls' in f:
            print("\n📶 Linhas de Transmissão encontradas:")
            for tl in f['tls']:
                tl_group = f[f'tls/{tl}']
                pos = tl_group.attrs.get('Position', None)
                R = tl_group.attrs.get('Resistance', None)
                dl = tl_group.attrs.get('dl', None)
                print(f"  ▶ {tl}:")
                print(f"     - Posição       : {tuple(pos) if pos is not None else 'Não disponível'}")
                print(f"     - Resistência   : {R}")
                print(f"     - Passo (dl)    : {dl}")
                print(f"     - Componentes: {', '.join(tl_group.keys())}")

        print("\n✅ Inspeção concluída.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Inspeciona visualmente um arquivo .out do gprMax (HDF5).')
    parser.add_argument('outputfile', help='Caminho para o arquivo .out do gprMax')
    args = parser.parse_args()

    inspect_gprmax_out(args.outputfile)
