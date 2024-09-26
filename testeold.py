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
                    novo_nome = f"Z_{file}"
                    os.rename(os.path.join(root, file), os.path.join(root, novo_nome))
                    print(f"Arquivo renomeado (SW): {novo_nome}")
                    continue
                
                # Extrair a data do nome do arquivo
                data = extrair_data(file)
                if data:
                    ano, mes = data.split("_")[2], data.split("_")[1]  # Extraindo ano e mês
                    caminho_completo = os.path.join(root, file)
                    arquivos_por_mes[(ano, mes)].append((file, caminho_completo))
        
        # Para cada mês, manter apenas os arquivos do começo, meio e fim
        for (ano, mes), arquivos in arquivos_por_mes.items():
            if len(arquivos) > 0:
                # Ordenar os arquivos por data
                arquivos.sort(key=lambda x: extrair_data(x[0]))

                # Manter apenas o primeiro, o 15º e o último
                arquivos_a_manter = []
                if len(arquivos) >= 1:
                    arquivos_a_manter.append(arquivos[0])  # Primeiro arquivo
                if len(arquivos) >= 15:
                    arquivos_a_manter.append(arquivos[14])  # 15º arquivo
                arquivos_a_manter.append(arquivos[-1])  # Último arquivo

                # Renomear os demais com "Z" no início
                for arquivo in arquivos:
                    if arquivo not in arquivos_a_manter:
                        novo_nome = f"Z_{arquivo[0]}"
                        os.rename(arquivo[1], os.path.join(root, novo_nome))
                        print(f"Arquivo renomeado: {novo_nome}")
            else:
                print(f"Nenhum arquivo encontrado para o mês {mes}/{ano}.")

if __name__ == "__main__":
    # Caminho base onde estão as pastas das entidades
    base_dir = r"D:/testintegração2020/INTEGRACAO"  # Altere para o caminho desejado
    processar_pastas(base_dir)
