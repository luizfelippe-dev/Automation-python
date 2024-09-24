import os

print("Iniciando o processamento das pastas...")

caminho_pasta_principal = 'D:/pt/CONTABILIDADE'

def realizar_automacao_em_pasta(pasta):
    print(f"Processando pasta: {pasta}")

    arquivos_para_processar = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".zip")]
    
    if not arquivos_para_processar:
        print(f"Nenhum arquivo .zip encontrado em {pasta}.")
        return

    arquivos_por_prefixo = {}
    
    for arquivo in arquivos_para_processar:
        nome_arquivo = os.path.basename(arquivo)

        # Verifica os primeiros 25 caracteres do nome do arquivo
        prefixo = nome_arquivo[:25]
        if prefixo not in arquivos_por_prefixo:
            arquivos_por_prefixo[prefixo] = []
        arquivos_por_prefixo[prefixo].append(arquivo)

    # Renomear arquivos que têm o mesmo prefixo
    for prefixo, arquivos in arquivos_por_prefixo.items():
        if len(arquivos) > 1:
            print(f"Encontrados arquivos com o mesmo prefixo: {prefixo}.")
            # Mantém o primeiro arquivo e adiciona 'Z' nos outros
            arquivo_mantido = arquivos[0]  # Mantém o primeiro arquivo
            for arquivo in arquivos[1:]:  # Renomeia os demais
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

#Este codigo esta funcional, mas preciso que ele funcione com outra verificação, ao inves de verificar por quantidade de caracteres, ele ira verificar dentro dos caracteres, que apos dois anderlines, a data do arquivo começa e ele deve ler até chegar em um numero com uma sequencia de 4 digitos que seria o ANO e então parar, isso dentro do nome do arquivo. esta seria a verificação, e adicionar tambem a verificação de tamanho do arquivo da sequinte maneira, pegar todos os arquivos, e fazer uma média, todos arquivos que tiver metade do tamanho da media sera selecionado para ter a letra z