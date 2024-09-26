import os 
import re
from src.model import session, Arquivos, ArquivosExcluidos 
from pathlib import Path
from datetime import datetime
import asyncio

class FileManager:
    def __init__(self, diretorio):
        self.diretorio = diretorio

    def _veriy_subdiretorio(self, dir_path):
        # Retorna todos os subdiretórios de forma recursiva
        return [p for p in Path(dir_path).rglob('*') if p.is_dir()]

    def _list_files(self, dir_path):
        # Retorna todos os arquivos no diretório especificado
        return [p for p in Path(dir_path).iterdir() if p.is_file()]

    def listar_todos_os_arquivos(self):
        lista_diretorio = self._veriy_subdiretorio(self.diretorio)
        listar_files = []
        for i in lista_diretorio:
            listar = self._list_files(i)
            if listar:  # Verifica se a lista não está vazia
                for r in listar:
                    if Path(r).name.endswith('.zip'):
                        listar_files.append(r.resolve())
        return listar_files

class VerifyFile:
    def __init__(self, directorio: str):
        self.diretorio = directorio

    def _save_db_info(self, name, tipo, sistema: str = None, caminho: str = None, date_creat: str = None, date_modify = None, size_file: str = None, date_name_file: str = None, version_firebird: str = None, exclude = 'N'):
        self.new_info = Arquivos(
            name_arquivo=name,
            tipo=tipo,
            sistema=sistema,
            caminho_completo=caminho,
            data_criacao=date_creat,
            data_modificacao=date_modify,
            tamanho_arquivo=size_file,
            data_arquivo=date_name_file, 
            firebird=version_firebird, 
            excluir=exclude
        )
        session.add(self.new_info)
        session.commit()

    def _extrair_informacoes(self, nome_arquivo):
        if not isinstance(nome_arquivo, str):
            raise ValueError("nome_arquivo deve ser uma string")

        padrao = r"(FB[234])(_SW)?_(\w+)_([0-9]{1,2})_([0-9]{1,2})_([0-9]{4})__(\d{1,2})_(\d{1,2})_(\d{1,2})_FBK"
        correspondencia = re.match(padrao, nome_arquivo)
        
        if correspondencia:
            tipo_firebird = correspondencia.group(1)
            sw = correspondencia.group(2)
            sistema = correspondencia.group(3)
            dia = correspondencia.group(4)
            mes = correspondencia.group(5)
            ano = correspondencia.group(6)
            hora = correspondencia.group(7)
            minuto = correspondencia.group(8)
            segundo = correspondencia.group(9)
            
            return {
                "tipo_firebird": tipo_firebird,
                "sw": sw,
                "sistema": sistema,
                "dia": dia,
                "mes": mes,
                "ano": ano,
                "hora": hora,
                "minuto": minuto,
                "segundo": segundo
            }
        else:
            raise ValueError("O nome do arquivo não corresponde ao padrão esperado")

    async def _start_process(self):
        file_manager = FileManager(self.diretorio)
        arquivos = file_manager.listar_todos_os_arquivos()
        for arquivo in arquivos:
            info = self._extrair_informacoes(arquivo.name)
            self._save_db_info(
                name=arquivo.name,
                tipo=info["tipo_firebird"],
                sistema=info["sistema"],
                caminho=str(arquivo),
                date_creat=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                date_modify=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                size_file=str(arquivo.stat().st_size),
                date_name_file=f"{info['ano']}-{info['mes']}-{info['dia']}",
                version_firebird=info["tipo_firebird"]
            )
            yield {
                "nome_arquivo": arquivo.name,
                "caminho_completo": str(arquivo),
                "data_arquivo": f"{info['ano']}-{info['mes']}-{info['dia']}",
                "hora_arquivo": f"{info['hora']}:{info['minuto']}:{info['segundo']}"
            }
            await asyncio.sleep(0.1)  # Simula uma pequena pausa para manter a interface responsiva
