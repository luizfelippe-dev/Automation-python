import os

print("Iniciando a remoção da letra 'Z' dos nomes dos arquivos...")

caminho_pasta_principal = 'D:/br/SIART'

def remover_z_nos_nomes(pasta):
    print(f"Processando pasta: {pasta}")

    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)

        if os.path.isfile(caminho_arquivo) and arquivo.startswith('Z'):
            # Remove a letra 'Z' do início do nome do arquivo
            novo_nome = os.path.join(pasta, arquivo[1:])  # Remove o primeiro caractere
            os.rename(caminho_arquivo, novo_nome)
            print(f"Renomeado: {caminho_arquivo} -> {novo_nome}")

def processar_pastas(caminho_pasta_principal):
    for subpasta in os.listdir(caminho_pasta_principal):
        caminho_subpasta = os.path.join(caminho_pasta_principal, subpasta)
        print(f"Verificando subpasta: {caminho_subpasta}")

        if os.path.isdir(caminho_subpasta):
            remover_z_nos_nomes(caminho_subpasta)

processar_pastas(caminho_pasta_principal)

print("Finalizando a remoção da letra 'Z' dos nomes dos arquivos...")
