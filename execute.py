import os 
import re
from src.model import session,Arquivos,ArquivosExcluidos 
from pathlib import Path
from multiprocessing import Process
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



class VerifyFile():
    def __init__(self,directorio:str):
        self.diretorio = directorio


    def _save_db_info(self,name,tipo,sistema:str=None,caminho:str=None,date_creat:str=None,date_modify=None,size_file:str=None, date_name_file:str=None, version_firebird:str=None,exclude = 'N'):
        self.new_info = Arquivos(
            name_arquivo = name,
            tipo = tipo,
            sistema = sistema,
            caminho_completo = caminho,
            data_criacao = date_creat,
            data_modificacao = date_modify,
            tamanho_arquivo = size_file,
            data_arquivo = date_name_file, 
            firebird = version_firebird, 
            excluir = exclude
        )
        session.add(self.new_info)
        session.commit()
        # print(date_modify)
    # Verifica a existencia de subdiretorios.
    def _extrair_informacoes(self,nome_arquivo):
        # Verifica se nome_arquivo é uma string
        
        if not isinstance(nome_arquivo, str):
            raise ValueError("nome_arquivo deve ser uma string")

        # Define o padrão regex para os nomes de arquivos
        padrao = r"(FB[234])(_SW)?_(\w+)_([0-9]{1,2})_([0-9]{1,2})_([0-9]{4})__(\d{1,2})_(\d{1,2})_(\d{1,2})_FBK"
        
        # Faz a correspondência com o padrão
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

    def _veriy_subdiretorio(self,diretorio:str = os.getcwd()):
        lista_diretorio = []

        # lista =  os.listdir(diretorio)
        # for i in lista:
        #     if os.path.isdir(i):
        #         lista_diretorio.append(fr"{Path(i).resolve()}")
        # for a in lista_diretorio:
        #     sub =  os.listdir(a)
        #     for b in a :
        #         if os.path.isdir(b):
        #             lista_diretorio.append(fr"{Path(b).resolve()}")

        for path in Path(diretorio).rglob('*'):
            if path.is_dir():
                lista_diretorio.append(path)


        return lista_diretorio                

    def _list_files(self,diretorio = None):
        lista_files_diretorio =[]
        lista_files_diretorio_temp = []
        if diretorio == None:
            lista_files_diretorio_temp = os.listdir()
        else :
            lista_files_diretorio_temp = os.listdir(diretorio)    

        for i in lista_files_diretorio_temp:
            if i.endswith('.zip'):
                lista_files_diretorio.append(Path(i).resolve())

        return lista_files_diretorio

    async def obter_informacoes_arquivo(self,name_arquivo,caminho):
        ext = self._extrair_informacoes(str(name_arquivo))
        # Obtém o caminho completo do arquivo
        caminho_completo = Path(caminho).resolve()
        # Obtém a data de criação (somente no Windows)
        data_criacao = datetime.fromtimestamp(os.path.getctime(caminho))

        # Obtém a data de modificação
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho))
        # dt = data_modificacao.strftime("%Y-%m-%d %H:%M:%S")

        # Obtém o tamanho do arquivo em bytes
        tamanho_arquivo = os.path.getsize(caminho)

        # Retorna as informações
        data_hora_str = f"{ext['ano']}-{ext['mes']}-{ext['dia']} {ext['hora']}:{ext['minuto']}:{ext['segundo']}"
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')

        info = self._save_db_info(
            name=name_arquivo,
            tipo=ext['sw'],
            sistema=ext['sistema'],
            caminho=caminho_completo.as_posix(),
            date_creat=data_criacao,
            date_modify=data_modificacao,
            size_file=tamanho_arquivo,
            date_name_file=data_hora_obj,
            version_firebird=ext['tipo_firebird']
        )

        return {
            "nome_arquivo": name_arquivo,
            "tipo":ext['sw'] , 
            "caminho_completo": caminho_completo.as_posix(),
            "data_criacao": data_criacao,
            "data_modificacao": data_modificacao,
            "tamanho_arquivo": tamanho_arquivo,
            "data_arquivo": f"{ext['dia']}-{ext['mes']}-{ext['ano']}",
            "hora_arquivo": f"{ext['hora']}:{ext['minuto']}:{ext["segundo"]}",
            "Firebird": ext['tipo_firebird']
        }

    def _start_process(self):
        # lista_diretorio = self._veriy_subdiretorio(self.diretorio)
        # listar_files = []
        # for i in lista_diretorio:
        #     # print(i)
        #     listar = self._list_files(i)
        #     if len(listar) > 0:
        #         for r in listar:
        #          listar_files.append(Path(r).resolve())
        #         #  listar_files.append(r)
        #          #l = self.obter_informacoes_arquivo(r,Path(r).resolve())
        #          #print((r,Path(r).resolve()))
 
        # print(listar_files)
        file_manager = FileManager(self.diretorio)
        todos_files = file_manager.listar_todos_os_arquivos()
        for i in todos_files:
           asyncio.run(self.obter_informacoes_arquivo(Path(i).name,i))
        
            
            
        

        pass

if __name__=='__main__':
    a = VerifyFile(os.getcwd())._start_process()
    print(a)
