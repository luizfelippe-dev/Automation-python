#Automação de Limpeza de Backups
"""BrainStorm:

Caminho das Pastas: \\10.1.2.35\backup\clientes\2023\1\ARH\C_AGUACLARA

 ==3 arquivos por mes nos anos de 2020 a 2022
 ==1 arquivo por dia nos anos de 2023 a 2024

 Entrar na pasta (Filho), fazer o processo. Ao Finalizar, retornar para pasta anterior(Pai) e acessar a pasta seguinte(Filho2).
 
 Validações:

 - na verificação de tamanho do arquivo, fazer média de todos os arquivos, os arquivos que tiver metade do tamanho da media dos arquivos devem ser deletados
 - Verificar se à dois arquivos com a mesma data, Se sim ir para proxima validação, se não ir para proximo arquivo.zip
 - verificar qual tem o horario mais perto do fim do dia, Horario mais perto de 23:59:59 Ter Prioridade e ir para proxima validação 
 - verificar tamanho do arquivo priorizando sempre o maior, se for mesmo tamanho ir Excluir o mais antigo.
 - Verificar nome do arquivo que possui SW no nome, se passar pelas validações anteriores (Data/horario e tamanho) então manter o arquivo SW como prioridade, e excluir os outros com mesma data e tamanho ou tamanho menores, caso contrario ir para proxima validação.
 - no caso dos arquivos serem absolutamente iguais excluir duplicatas e manter apenas 1 arquivo
 
 - Testar a automação inserindo a letra "Z" no começo ou final do nome do arquivo
 - No caso de funcionar apenas trocar a função para que exclua os arquivos

 ----------------------------------------------------------------------------------
automação teste para adicionar "Z" dentro do nome dos backups e outra para retirar oq foi inserido.
 ----------------------------------------------------------------------------------
 - possibilidade de criar uma automação de inserção de caracteres predefinidos nos arquivos
   e outra automação apenas para validar e excluir arquivos com os caracteres."""