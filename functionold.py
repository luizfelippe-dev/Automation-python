import os
import re
from collections import defaultdict

def extrair_data(nome_arquivo):
    # Regex para capturar a data no formato dd_mm_aaaa dentro do nome do arquivo
    match = re.search(r"(\d{2}_\d{2}_\d{4})", nome_arquivo)
    if match:
        return match.group(1)  # Retorna a data como string
    return None

def processar_pastas(base_dir):
    for root, dirs, files in os.walk(base_dir):
        arquivos_por_mes = defaultdict(list)
        
        # Itera sobre os arquivos
        for file in files:
            print(f"Processando: {file}")  # Monitorando os arquivos processados
            if file.endswith(".zip"):
                # Ignorar arquivos com "SW" no nome
                if "SW" in file:
                    os.remove(os.path.join(root, file))  # Excluindo o arquivo
                    print(f"Arquivo excluído (SW): {file}")
                    continue
                
                # Extrair a data do nome do arquivo
                data = extrair_data(file)
                if data:
                    dia, mes, ano = data.split("_")  # Extraindo dia, mês e ano
                    caminho_completo = os.path.join(root, file)
                    arquivos_por_mes[(ano, mes)].append((int(dia), file, caminho_completo))
        
        # Para cada mês, manter apenas os arquivos do começo, meio e fim
        for (ano, mes), arquivos in arquivos_por_mes.items():
            if len(arquivos) > 0:
                # Ordenar os arquivos por dia
                arquivos.sort(key=lambda x: x[0])

                # Selecionar arquivos do começo, meio e fim
                arquivos_a_manter = []

                # Manter o arquivo do começo do mês
                arquivos_a_manter.append(arquivos[0])  # Primeiro arquivo (ou mais próximo do início)

                # Encontrar o arquivo do meio do mês (mais próximo do dia 15)
                meio = sorted(arquivos, key=lambda x: abs(x[0] - 15))
                arquivos_a_manter.append(meio[0])  # Mais próximo do dia 15

                # Manter o último arquivo do mês
                arquivos_a_manter.append(arquivos[-1])  # Último arquivo do mês

                # Excluir os demais
                arquivos_a_manter_set = set((dia, file, caminho) for dia, file, caminho in arquivos_a_manter)
                for arquivo in arquivos:
                    if (arquivo[0], arquivo[1], arquivo[2]) not in arquivos_a_manter_set:
                        os.remove(arquivo[2])  # Excluindo o arquivo
                        print(f"Arquivo excluído: {arquivo[1]}")
            else:
                print(f"Nenhum arquivo encontrado para o mês {mes}/{ano}.")

if __name__ == "__main__":
    # Caminho base onde estão as pastas das entidades
    base_dir = r"D:/testintegração2020/INTEGRACAO"  # Altere para o caminho desejado
    processar_pastas(base_dir)
