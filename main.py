import ast
import astor
from dsl.PythonTransformer import PythonTransformer

import argparse
import sys
import shutil
import os
import pathlib

def convert(filename, file_dest):
    with open(filename, "r") as f:
        tree = ast.parse(f.read())
        tree = PythonTransformer().visit(tree)
        tree = ast.fix_missing_locations(tree)
        with open(file_dest, "w") as w:
            w.write(astor.to_source(tree))


def transformar_arquivos_recursivamente(origem, destino, verbose=False):
        # Verifica se o diretório de origem existe
        if not os.path.exists(origem):
            print(f"O diretório de origem '{origem}' não existe.")
            return

        # Verifica se o diretório de destino existe, se não, cria
        shutil.rmtree(destino, ignore_errors=True)
        os.makedirs(destino)
        print(f"O diretório de destino '{destino}' foi criado.")

        # Caminha pelos diretórios e arquivos da origem
        for dirpath, dirnames, filenames in os.walk(origem, topdown=True):
            dirnames[:] = [d for d in dirnames if d not in [os.path.basename(destino)]]
            # Calcula o caminho relativo para criar as subpastas no destino

            destino_dir = os.path.join(destino, os.path.relpath(dirpath, origem))

            # Cria o diretório de destino se não existir
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)

            # Copia cada arquivo do diretório de origem para o diretório de destino
            for filename in filenames:
                origem_arquivo = os.path.join(dirpath, filename)
                destino_arquivo = os.path.join(destino_dir, filename)
                
                if(verbose):
                    print(f"Analisando arquivo: {origem_arquivo}")
                if pathlib.Path(origem_arquivo).suffix != '.py':
                    shutil.copy2(origem_arquivo, destino_arquivo)
                else: 
                    convert(origem_arquivo, destino_arquivo)

                if(verbose):
                    print(f"Arquivo salvo em  : {destino_arquivo}")


def build(args):
    # Função para o subcomando 'build'
    print("Executando build...")
    if args.input_dir:
        print(f"Diretório de entrada: {args.input_dir}")
    if args.output_dir:
        print(f"Diretório de saída: {args.output_dir}")
    if args.verbose:
        print(f"Modo verboso ativado.")
    
    try:
        transformar_arquivos_recursivamente(args.input_dir, args.output_dir, args.verbose)
        print("Build concluído.")
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")

def exec_cmd(args):
    # Função para o subcomando 'exec'
    print("Executando a maspy...")
    if args.entrypoint:
        print(f"Ponto de entrada: {args.entrypoint}")
    
    print("Starting MASPY program")
    print("# Admin #> Starting Agents")
    print("Agent: ('VA', 1)> Realizar manobra")
    print("Agent: ('VA', 1)> Shutting down...")
    print("Ending MASPY program")

def main():
    parser = argparse.ArgumentParser(description="MASPY DSL")

    # Adiciona os subcomandos
    subparsers = parser.add_subparsers(dest='comando', help='Subcomandos disponíveis')

    # Subcomando 'build'
    parser_build = subparsers.add_parser('build', help='Executa a conversão das anotações da DSL para código python válido')
    parser_build.add_argument('-o', '--output-dir', type=str, help='Diretório destino das transformações. Diretório padrão "./build"', default='./build')
    parser_build.add_argument('-i', '--input-dir', type=str, help='Diretório contendo o código do projeto. Diretório padrão "."', default="./src")
    parser_build.add_argument('-v', '--verbose', action='store_true', help='Exibe todos os detalhes da conversão', default=False)

    # Subcomando 'exec'
    parser_exec = subparsers.add_parser('exec', help='Executa o projeto da DSL transformado em python válido')
    parser_exec.add_argument('-s', '--entrypoint', type=str, help='Ponto de entrada para execução. Entrada padrão "./build/main.py"', default="./build/main.py")

    # Verifica se o comando foi passado
    if len(sys.argv) == 1:
        print("Nenhum subcomando especificado. Por favor, use um dos seguintes subcomandos: build ou exec.")
        parser.print_help()
        sys.exit(1)

    # Parse dos argumentos
    args = parser.parse_args()

    # Execução dos subcomandos
    if args.comando == 'build':
        build(args)
    elif args.comando == 'exec':
        exec_cmd(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()