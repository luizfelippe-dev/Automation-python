import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import customtkinter as ctk

def extrair_data(nome_arquivo):
    # Regex para capturar várias formas de datas como dd_mm_aaaa, d_mm_aaaa, dd_mm_aa ou dd_mm_aaaa_hh_mm_ss
    match = re.search(r"(\d{1,2}_\d{1,2}_\d{2,4})", nome_arquivo)
    if match:
        return match.group(1)  # Retorna a data como string
    return None

def obter_mes_ano(data):
    # Extrai o mês e o ano da data no formato dd_mm_aaaa ou dd_mm_aa
    partes_data = data.split('_')
    if len(partes_data[2]) == 2:  # Se o ano for de dois dígitos, adiciona '20' para completar o formato
        ano = f"20{partes_data[2]}"
    else:
        ano = partes_data[2]
    mes = partes_data[1]
    return f"{mes}_{ano}"

def ajustar_data_se_necessario(data_arquivo, timestamp_modificacao):
    """Se o arquivo foi modificado entre 23h e 4h, ajusta a data para o dia anterior."""
    data_modificacao = datetime.fromtimestamp(timestamp_modificacao)
    hora_modificacao = data_modificacao.hour
    
    # Se o horário de modificação for entre 23h e 4h, considera como do dia anterior
    if 23 <= hora_modificacao or hora_modificacao < 5:
        data_modificada = data_modificacao - timedelta(days=1)
        nova_data = data_modificada.strftime("%d_%m_%Y")
        print(f"Ajustando data de {data_arquivo} para {nova_data} devido ao horário {hora_modificacao}.")
        return nova_data
    return data_arquivo

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
                if file.endswith((".zip", ".rar")):  # Reconhece arquivos .zip e .rar
                    if "SW" in file:
                        caminho_completo = os.path.join(root, file)
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z{file}"
                            os.rename(caminho_completo, os.path.join(root, novo_nome))
                            print(f"Arquivo renomeado (SW): {novo_nome}")
                        continue
                    
                    data = extrair_data(file)
                    if data:
                        caminho_completo = os.path.join(root, file)
                        timestamp_modificacao = os.path.getmtime(caminho_completo)
                        data = ajustar_data_se_necessario(data, timestamp_modificacao)
                        
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
                            novo_nome = f"Z{arquivo[0]}"
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
                if file.endswith((".zip", ".rar")):  # Reconhece arquivos .zip e .rar
                    if "SW" in file:
                        caminho_completo = os.path.join(root, file)
                        if os.path.exists(caminho_completo):
                            novo_nome = f"Z{file}"
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
                                novo_nome = f"Z{arquivo[1]}"
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
                if file.startswith("Z"):
                    caminho_completo = os.path.join(root, file)
                    novo_nome = file[1:]  # Remove "Z" do início
                    os.rename(caminho_completo, os.path.join(root, novo_nome))
                    print(f"Prefixo 'Z' removido: {novo_nome}")
            except Exception as e:
                print(f"Erro ao remover o prefixo do arquivo {file}: {e}")
            
            arquivos_processados += 1
            progresso["value"] = arquivos_processados
            app.update_idletasks()

def excluir_arquivos_com_z(base_dir):
    total_arquivos = 0
    for root, dirs, files in os.walk(base_dir):
        total_arquivos += len(files)

    progresso["maximum"] = total_arquivos
    progresso["value"] = 0
    arquivos_processados = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            try:
                if file.startswith("Z"):
                    caminho_completo = os.path.join(root, file)
                    os.remove(caminho_completo)
                    print(f"Arquivo excluído: {file}")
            except Exception as e:
                print(f"Erro ao excluir o arquivo {file}: {e}")

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
        messagebox.showinfo("Concluído", "Os arquivos foram renomeados para remover o prefixo 'Z'!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

def excluir_arquivos_com_z_button():
    pasta = pasta_entry.get()
    if os.path.isdir(pasta):
        excluir_arquivos_com_z(pasta)
        messagebox.showinfo("Concluído", "Os arquivos com prefixo 'Z' foram excluídos!")
    else:
        messagebox.showerror("Erro", "Selecione uma pasta válida.")

# Configurando a aparência da interface com customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Interface gráfica
app = ctk.CTk()
app.title("CleanAutomate")
app.geometry("400x500")

# Label e Entry para a pasta
label = ctk.CTkLabel(app, text="Selecione a pasta:")
label.pack(pady=10)

pasta_entry = ctk.CTkEntry(app, width=300)
pasta_entry.pack(pady=5)

# Botão para selecionar a pasta
botao_selecionar = ctk.CTkButton(app, text="Selecionar Pasta", command=selecionar_pasta)
botao_selecionar.pack(pady=5)

# Barra de progresso
progresso = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progresso.pack(pady=10)

# Botão para iniciar a automação por dia
botao_iniciar_dia = ctk.CTkButton(app, text="Iniciar Automação por Dia", command=iniciar_automacao_por_dia)
botao_iniciar_dia.pack(pady=5)

# Botão para iniciar a automação por mês
botao_iniciar_mes = ctk.CTkButton(app, text="Iniciar Automação por Mês", command=iniciar_automacao_por_mes)
botao_iniciar_mes.pack(pady=5)

# Botão para remover o prefixo "Z_"
botao_remover_z = ctk.CTkButton(app, text="Remover Prefixo 'Z' dos Arquivos", command=remover_z_dos_arquivos)
botao_remover_z.pack(pady=5)

# Botão para excluir arquivos com "Z_"
botao_excluir_z = ctk.CTkButton(app, text="Excluir Arquivos com 'Z'", command=excluir_arquivos_com_z_button)
botao_excluir_z.pack(pady=5)

# Executando a interface gráfica
app.mainloop()
