import os
import re
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def extrair_data(nome_arquivo):
    # Regex para capturar a data no formato d_m_aaaa ou dd_mm_aaaa dentro do nome do arquivo
    match = re.search(r"(\d{1,2}_\d{1,2}_\d{4})", nome_arquivo)
    if match:
        return match.group(1)  # Retorna a data como string
    return None

def obter_mes_ano(data):
    # Extrai o mês e o ano da data no formato dd_mm_aaaa
    dia, mes, ano = data.split('_')
    return f"{mes}_{ano}"

def processar_pastas_por_dia(base_dir):
    total_arquivos = 0
    for root, dirs, files in os.walk(base_dir):
        total_arquivos += len(files)
    
    progresso["maximum"] = total_arquivos
    progresso["value"] = 0
    arquivos_processados = 0

    for root, dirs, files in os.walk(base_dir):
        arquivos_por_data = defaultdict(list)
        
        for file in files:
            try:
                print(f"Processando: {file}")
                if file.endswith(".zip"):
                    if "SW" in file:
                        caminho_completo = os.path.join(root, file)
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z_{file}"
                            os.rename(caminho_completo, os.path.join(root, novo_nome))
                            print(f"Arquivo renomeado (SW): {novo_nome}")
                        continue
                    
                    data = extrair_data(file)
                    if data:
                        caminho_completo = os.path.join(root, file)
                        tamanho = os.path.getsize(caminho_completo)
                        arquivos_por_data[data].append((file, tamanho, caminho_completo))
                    else:
                        print(f"Data não encontrada no nome do arquivo: {file}")
            except Exception as e:
                print(f"Erro ao processar o arquivo {file}: {e}")

            arquivos_processados += 1
            progresso["value"] = arquivos_processados
            app.update_idletasks()
        
        for data, arquivos in arquivos_por_data.items():
            if len(arquivos) > 1:
                arquivos.sort(key=lambda x: x[1], reverse=True)
                maior_arquivo = arquivos[0]
                print(f"Arquivo mantido: {maior_arquivo[0]}")

                for arquivo in arquivos[1:]:
                    try:
                        caminho_completo = arquivo[2]
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z_{arquivo[0]}"
                            os.rename(caminho_completo, os.path.join(root, novo_nome))
                            print(f"Arquivo renomeado: {novo_nome}")
                        else:
                            print(f"Arquivo não encontrado para renomeação: {arquivo[0]}")
                    except Exception as e:
                        print(f"Erro ao renomear o arquivo {arquivo[0]}: {e}")

def processar_pastas_por_mes(base_dir):
    total_arquivos = 0
    for root, dirs, files in os.walk(base_dir):
        total_arquivos += len(files)
    
    progresso["maximum"] = total_arquivos
    progresso["value"] = 0
    arquivos_processados = 0

    for root, dirs, files in os.walk(base_dir):
        arquivos_por_mes = defaultdict(list)
        
        for file in files:
            try:
                print(f"Processando: {file}")
                if file.endswith(".zip"):
                    if "SW" in file:
                        caminho_completo = os.path.join(root, file)
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z_{file}"
                            os.rename(caminho_completo, os.path.join(root, novo_nome))
                            print(f"Arquivo renomeado (SW): {novo_nome}")
                        continue
                    
                    data = extrair_data(file)
                    if data:
                        caminho_completo = os.path.join(root, file)
                        tamanho = os.path.getsize(caminho_completo)
                        mes_ano = obter_mes_ano(data)
                        arquivos_por_mes[mes_ano].append((data, file, tamanho, caminho_completo))
                    else:
                        print(f"Data não encontrada no nome do arquivo: {file}")
            except Exception as e:
                print(f"Erro ao processar o arquivo {file}: {e}")

            arquivos_processados += 1
            progresso["value"] = arquivos_processados
            app.update_idletasks()
        
        for mes_ano, arquivos in arquivos_por_mes.items():
            if len(arquivos) > 3:
                arquivos.sort(key=lambda x: x[0])  # Ordenar pelo dia
                
                arquivos_para_manter = [
                    min(arquivos, key=lambda x: abs(int(x[0].split('_')[0]) - 1)),   # Próximo do início do mês
                    min(arquivos, key=lambda x: abs(int(x[0].split('_')[0]) - 15)),  # Próximo do meio do mês
                    min(arquivos, key=lambda x: abs(int(x[0].split('_')[0]) - 30))   # Próximo do final do mês
                ]
                
                arquivos_para_manter_nomes = {arq[1] for arq in arquivos_para_manter}
                print(f"Arquivos mantidos para {mes_ano}: {arquivos_para_manter_nomes}")

                for arquivo in arquivos:
                    if arquivo[1] not in arquivos_para_manter_nomes:
                        try:
                            caminho_completo = arquivo[3]
                            if os.path.exists(caminho_completo):
                                novo_nome = f"Z_{arquivo[1]}"
                                os.rename(caminho_completo, os.path.join(root, novo_nome))
                                print(f"Arquivo renomeado: {novo_nome}")
                            else:
                                print(f"Arquivo não encontrado para renomeação: {arquivo[1]}")
                        except Exception as e:
                            print(f"Erro ao renomear o arquivo {arquivo[1]}: {e}")

def remover_prefixo_z(base_dir):
    total_arquivos = 0
    for root, dirs, files in os.walk(base_dir):
        total_arquivos += len(files)
    
    progresso["maximum"] = total_arquivos
    progresso["value"] = 0
    arquivos_processados = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            try:
                if file.startswith("Z_"):
                    caminho_completo = os.path.join(root, file)
                    novo_nome = file[2:]  # Remove "Z_" do início
                    os.rename(caminho_completo, os.path.join(root, novo_nome))
                    print(f"Prefixo 'Z_' removido: {novo_nome}")
            except Exception as e:
                print(f"Erro ao remover o prefixo do arquivo {file}: {e}")
            
            arquivos_processados += 1
            progresso["value"] = arquivos_processados
            app.update_idletasks()

def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        pasta_entry.delete(0, tk.END)
        pasta_entry.insert(0, pasta_selecionada)

def iniciar_automacao_por_dia():
    pasta = pasta_entry.get()
    if os.path.isdir(pasta):
        processar_pastas_por_dia(pasta)
        messagebox.showinfo("Concluído", "A automação por dia foi concluída com sucesso!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

def iniciar_automacao_por_mes():
    pasta = pasta_entry.get()
    if os.path.isdir(pasta):
        processar_pastas_por_mes(pasta)
        messagebox.showinfo("Concluído", "A automação por mês foi concluída com sucesso!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

def remover_z_dos_arquivos():
    pasta = pasta_entry.get()
    if os.path.isdir(pasta):
        remover_prefixo_z(pasta)
        messagebox.showinfo("Concluído", "Os arquivos foram renomeados para remover o prefixo 'Z_'!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

# Interface gráfica
app = tk.Tk()
app.title("CleanAutomate :D")
app.geometry("400x400")

# Label e Entry para a pasta
label = tk.Label(app, text="Selecione a pasta:")
label.pack(pady=10)

pasta_entry = tk.Entry(app, width=50)
pasta_entry.pack(pady=5)

# Botão para selecionar a pasta
botao_selecionar = tk.Button(app, text="Selecionar Pasta", command=selecionar_pasta)
botao_selecionar.pack(pady=5)

# Barra de progresso
progresso = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progresso.pack(pady=10)

# Botão para iniciar a automação por dia
botao_iniciar_dia = tk.Button(app, text="Iniciar Automação por Dia", command=iniciar_automacao_por_dia)
botao_iniciar_dia.pack(pady=5)

# Botão para iniciar a automação por mês
botao_iniciar_mes = tk.Button(app, text="Iniciar Automação por Mês", command=iniciar_automacao_por_mes)
botao_iniciar_mes.pack(pady=5)

# Botão para remover o prefixo "Z_"
botao_remover_z = tk.Button(app, text="Remover Prefixo 'Z' dos Arquivos", command=remover_z_dos_arquivos)
botao_remover_z.pack(pady=10)

# Executando a interface gráfica
app.mainloop()

