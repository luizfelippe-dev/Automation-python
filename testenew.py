import os

print("Iniciando o processamento das pastas...")

caminho_pasta_principal = 'D:/br/SIART'

def realizar_automacao_em_pasta(pasta):
    print(f"Processando pasta: {pasta}")

    arquivos_para_processar = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".zip")]
    
    if not arquivos_para_processar:
        print(f"Nenhum arquivo .zip encontrado em {pasta}.")
        return

    arquivos_por_prefixo = {}
    
    for arquivo in arquivos_para_processar:
        nome_arquivo = os.path.basename(arquivo)

        # Verifica os primeiros x caracteres do nome do arquivo
        prefixo = nome_arquivo[:23]
        if prefixo not in arquivos_por_prefixo:
            arquivos_por_prefixo[prefixo] = []
        arquivos_por_prefixo[prefixo].append(arquivo)

    # Renomear arquivos que têm o mesmo prefixo
    for prefixo, arquivos in arquivos_por_prefixo.items():
        if len(arquivos) > 1:
            print(f"Encontrados arquivos com o mesmo prefixo: {prefixo}.")
            # Encontra o arquivo de maior tamanho
            arquivo_mantido = max(arquivos, key=os.path.getsize)
            print(f"Mantendo arquivo: {arquivo_mantido}")

            # Renomeia os demais arquivos
            for arquivo in arquivos:
                if arquivo != arquivo_mantido:  # Ignora o arquivo mantido
                    print(f"Arquivo {arquivo} será marcado por prefixo duplicado.")
                    # Adiciona 'Z' ao início do nome do arquivo
                    novo_nome = os.path.join(pasta, 'Z' + os.path.basename(arquivo))
                    os.rename(arquivo, novo_nome)

def processar_pastas(caminho_pasta_principal):
    for subpasta in os.listdir(caminho_pasta_principal):
        caminho_subpasta = os.path.join(caminho_pasta_principal, subpasta)
        print(f"Verificando subpasta: {caminho_subpasta}")
        
        if os.path.isdir(caminho_subpasta):
            realizar_automacao_em_pasta(caminho_subpasta)

processar_pastas(caminho_pasta_principal)

print("Finalizando o processamento das pastas...")
