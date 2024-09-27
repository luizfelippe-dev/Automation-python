import os
import re
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox

def extrair_data(nome_arquivo):
    # Regex para capturar a data no formato d_m_aaaa ou dd_mm_aaaa dentro do nome do arquivo
    match = re.search(r"(\d{1,2}_\d{1,2}_\d{4})", nome_arquivo)
    if match:
        return match.group(1)  # Retorna a data como string
    return None

def processar_pastas(base_dir):
    for root, dirs, files in os.walk(base_dir):
        arquivos_por_data = defaultdict(list)
        
        # Itera sobre os arquivos
        for file in files:
            try:
                print(f"Processando: {file}")  # Monitorando os arquivos processados
                if file.endswith(".zip"):
                    # Ignorar arquivos com "SW" no nome
                    if "SW" in file:
                        caminho_completo = os.path.join(root, file)
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z{file}"
                            os.rename(caminho_completo, os.path.join(root, novo_nome))
                            print(f"Arquivo renomeado (SW): {novo_nome}")
                        continue
                    
                    # Extrair a data do nome do arquivo
                    data = extrair_data(file)
                    if data:
                        caminho_completo = os.path.join(root, file)
                        tamanho = os.path.getsize(caminho_completo)
                        arquivos_por_data[data].append((file, tamanho, caminho_completo))
                    else:
                        print(f"Data não encontrada no nome do arquivo: {file}")
            except Exception as e:
                print(f"Erro ao processar o arquivo {file}: {e}")
        
        # Para cada data, manter apenas o maior arquivo
        for data, arquivos in arquivos_por_data.items():
            if len(arquivos) > 1:
                # Ordenar pelo tamanho e manter o maior
                arquivos.sort(key=lambda x: x[1], reverse=True)
                maior_arquivo = arquivos[0]
                print(f"Arquivo mantido: {maior_arquivo[0]}")

                # Renomear os demais com "Z" no início
                for arquivo in arquivos[1:]:
                    try:
                        caminho_completo = arquivo[2]
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z{arquivo[0]}"
                            os.rename(caminho_completo, os.path.join(root, novo_nome))
                            print(f"Arquivo renomeado: {novo_nome}")
                        else:
                            print(f"Arquivo não encontrado para renomeação: {arquivo[0]}")
                    except Exception as e:
                        print(f"Erro ao renomear o arquivo {arquivo[0]}: {e}")

def remover_prefixo_z(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            try:
                # Verificar se o arquivo começa com "Z"
                if file.startswith("Z"):
                    caminho_completo = os.path.join(root, file)
                    novo_nome = file[1:]  # Remove "Z" do início
                    os.rename(caminho_completo, os.path.join(root, novo_nome))
                    print(f"Prefixo 'Z' removido: {novo_nome}")
            except Exception as e:
                print(f"Erro ao remover o prefixo do arquivo {file}: {e}")

def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        pasta_entry.delete(0, tk.END)
        pasta_entry.insert(0, pasta_selecionada)

def iniciar_automacao():
    pasta = pasta_entry.get()
    if os.path.isdir(pasta):
        processar_pastas(pasta)
        messagebox.showinfo("Concluído", "A automação foi concluída com sucesso!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

def remover_z_dos_arquivos():
    pasta = pasta_entry.get()
    if os.path.isdir(pasta):
        remover_prefixo_z(pasta)
        messagebox.showinfo("Concluído", "Os arquivos foram renomeados para remover o prefixo 'Z'!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

# Interface gráfica
root = tk.Tk()
root.title("Automação de Backup")
root.geometry("400x200")

# Label e Entry para a pasta
label = tk.Label(root, text="Selecione a pasta:")
label.pack(pady=10)

pasta_entry = tk.Entry(root, width=50)
pasta_entry.pack(pady=5)

# Botão para selecionar a pasta
botao_selecionar = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
botao_selecionar.pack(pady=5)

# Botão para iniciar a automação
botao_iniciar = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
botao_iniciar.pack(pady=5)

# Botão para remover o prefixo "Z_"
botao_remover_z = tk.Button(root, text="Remover Prefixo 'Z' dos Arquivos", command=remover_z_dos_arquivos)
botao_remover_z.pack(pady=10)

root.mainloop()
