
# CleanAutomate

## Descrição
CleanAutomate é uma aplicação de automação de arquivos desenvolvida com a biblioteca Tkinter e customtkinter do Python. A aplicação facilita a organização e o gerenciamento de arquivos dentro de pastas baseando-se em datas incorporadas nos nomes dos arquivos. Ele fornece funcionalidades para renomear, reorganizar e excluir arquivos com base em regras pré-definidas.

## Intuito
O objetivo do CleanAutomate é processar arquivos dentro de uma estrutura de diretórios selecionada pelo usuário, organizando-os por data de modificação e outros critérios especificados. Ele suporta a automação de tarefas repetitivas como:
- Renomear arquivos para incluir ou remover prefixos.
- Organizar arquivos em subpastas com base em sua data.
- Excluir arquivos redundantes ou temporários.
- Facilitar a limpeza e manutenção de diretórios grandes.

## Funcionalidades
1. **Selecionar Pasta:** Permite ao usuário escolher a pasta que deseja automatizar.
2. **Automação por Dia:** Processa os arquivos por dia, agrupando-os por data e renomeando arquivos duplicados ou menos relevantes.
3. **Automação por Mês:** Agrupa os arquivos em um nível mais alto, por mês e ano, e executa operações similares, mas em um escopo temporal mais amplo.
4. **Remover Prefixo 'Z':** Remove o prefixo 'Z' de arquivos previamente marcados.
5. **Excluir Arquivos com 'Z':** Exclui arquivos que começam com o prefixo 'Z', que são geralmente arquivos temporários ou marcados para exclusão.

## Verificações
- **Validação de Pasta:** Verifica se o diretório selecionado é válido e acessível.
- **Validação de Nome de Arquivo:** Extrai e valida datas dos nomes dos arquivos utilizando expressões regulares para formatos de data comuns.
- **Verificação de Modificação de Arquivos:** Ajusta datas de arquivos modificados entre 23h e 4h para refletir a data correta de criação ou modificação.
- **Tratamento de Exceções:** Gerencia erros durante o processo de renomeação ou exclusão de arquivos para manter a estabilidade da aplicação.

## Requisitos
- **Python 3.x**
- **Bibliotecas:**
  - `tkinter`
  - `customtkinter`
  - `os`
  - `re`
  - `collections`
  - `datetime`
- **Sistema Operacional Compatível:** Windows, macOS ou Linux com suporte para Tkinter.

## Instalação
Para usar o CleanAutomate, certifique-se de ter o Python e as bibliotecas necessárias instaladas. Você pode instalar as bibliotecas adicionais usando pip:
```bash
pip install customtkinter
```
# Execução

Para iniciar a aplicação, execute o script Python no terminal ou através de um ambiente de desenvolvimento que suporte execução de scripts Python com interface gráfica:
```bash
python CleanAutomate.py
```

## Autores

- [@JuliSales](https://github.com/Locked666)
- [@LuizFelipe](https://github.com/luizfelippe-dev/)


