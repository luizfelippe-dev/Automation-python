#Automação de Limpeza de Backups
"""BrainStorm: Nome, Data, Tamanho, Copia

Verificar Nome, Data Do Backup, Tamanho do arquivo sempre maior que o anterior.
 Validar se já possui copias do arquivo
 Sempre mantes 1 SW mais atual
 ==3 arquivos por mes nos anos de 2020 a 2022
 ==1 arquivo por dia nos anos de 2023 a 2024
 verificação de funcionamento do banco, descompactando
 
 Validações: Duplicata com mesmo nome 
 - verificar data mantendo apenas um banco por dia (Se o ano for ==2023 && ==2024)
 - verificar horario mais perto do fim do dia 
 - verificar tamanho do arquivo priorizando sempre o maior
 - no caso dos arquivos serem absolutamente iguais excluir duplicatas e manter apenas 1 arquivo 
 
 - Testar a automação inserindo a letra "Z" no começo ou final do nome do arquivo
 - No caso de funcionar apenas trocar a função para que exclua os arquivos

 ----------------------------------------------------------------------------------
automação teste para adicionar "Z" dentro do nome dos backups e outra para retirar oq foi inserido.
 ----------------------------------------------------------------------------------
 - possibilidade de criar uma automação de inserção de caracteres predefinidos nos backups
   e outra automação apenas para validar e excluir arquivos com os caracteres."""