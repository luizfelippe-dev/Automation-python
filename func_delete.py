import os
import re
from src.model import session,Arquivos,ArquivosExcluidos,engine,text 
from pathlib import Path
from multiprocessing import Process
from datetime import datetime
import asyncio 

class ProcessDelete():
    def __init__(self) -> None:
    
        
        pass
    
    def return_files(self):
        output = []
        with engine.connect() as connection:
            result = connection.execute(text("SELECT ID, EXCLUIR, NAME_ARQUIVO, ANO,CAMINHO_COMPLETO FROM ARQUIVOS WHERE EXCLUIR = 'S'"))
            for row in result:
                output.append(row)
        connection.close()
        yield output    

        pass


class DeleteFile():
    def __init__(self) -> None:
        pass
      
    def _get_db(self, id:int = 0, ):
        output = []
        
        if id > 0:
            with engine.connect() as connection:
                result = connection.execute(text(f"SELECT * FROM ARQUIVOS WHERE ID IN ({id}) "))
                for row in result:
                    output.append(row)
            connection.close()
            return output
 
        else:    
            with engine.connect() as connection:
                result = connection.execute(text("SELECT * FROM ARQUIVOS WHERE EXCLUIR='S' "))
                for row in result:
                    output.append(row)
            connection.close()
            return output

    def _delete_db(self, id: int = 0):
        if id > 0:
            with engine.connect() as connection:
                connection.execute(text(f"DELETE FROM ARQUIVOS WHERE ID IN ({id})"))
                connection.commit()  # Mova o commit para dentro do bloco with
        
    
    
    
    def _save_db_delete(self,name,tipo,city,year,sistema:str=None,caminho:str=None,date_creat:str=None,date_modify=None,size_file:str=None, date_name_file:str=None, version_firebird:str=None,exclude = 'S'):
        self.new_info = ArquivosExcluidos(
            name_arquivo = name,
            tipo = tipo,
            cidade = city,
            ano=year,
            sistema = sistema,
            caminho_completo = caminho,
            #data_criacao = date_creat,
            #data_modificacao = date_modify,
            tamanho_arquivo = size_file,
            #data_arquivo = date_name_file, 
            firebird = version_firebird, 
            excluir = exclude
        )
        session.add(self.new_info)
        session.commit()
    
    
    def _delete_file(self,id:int = 0):
        query = self._get_db(id=id)
        if len(query) > 0:
            for i in query:
                save_log = self._save_db_delete(name=i[1],tipo=i[2],city=i[3],year=i[4],sistema=i[5],caminho=i[6],size_file=i[9])
                if os.path.exists(i[6]):
                    delete = os.remove(i[6])
                    delete_db = self._delete_db(i[0])
                    return f"Arquivo {i[6]} removido"
                    #
                else: 
                    delete_db = self._delete_db(i[0])
                    return f"Erro ao remover, arquivo inexistente {i[6]}"
                       
                
                # print('name'+i[1])
                # print('caminho' +' '+ i[6])
                # print('tamanho' + i[9])

        
    
    def _start_process_delete(self):
        files_to_exclude = self._get_db()
        for i in files_to_exclude:
            delete = self._delete_file(i[0])
            yield delete


if __name__ == "__main__":

    app =DeleteFile()._start_process_delete()
    # #app._start_process_delete()
    # for l in app:
    #     print(l)