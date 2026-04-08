# ========================================================
# SISTEMA DE GESTÃO DE PEDIDOS
# Autor: PAULO
# Tecnologias: Python + SQLite
# Sistema CRUD com cadastro de produtos, 
# realização de pedidos e relatório de vendas (ETL
# ========================================================



from colorama import Fore, Style, init

#Inicializa conexão com banco de dados SQLite
import sqlite3

conn = sqlite3.connect("sqlid.db")
cursor = conn.cursor()


# Exibe menu principal do sistema
init()
pedidos = []
print(Fore.BLACK + "--- CRUD ATUALIZADO ---" + Style.RESET_ALL)
print(Fore.LIGHTGREEN_EX + "1 - CADASTRAR PRODUTO")
print("2 - LISTAR PRODUTO")
print("3 - FAZER PEDIDOS")
print("4 - LISTAR PEDIDOS")
print("5 - VER FATURAMENTO TOTAL")
print("7 - RELATÓRIO TOTAL")
print("6 - SAIR" + Style.RESET_ALL)

op_cadastro = 1
op_listarproduto = 2
op_fazerpedidos = 3
op_listarpedidos = 4
op_fatur = 5
sair = 6
op_relat = 7
rodando = True

# LOOP principal do sistema (execução continua)
while rodando: 

  try:          #EVITAR QUEBRA
    opcao = int(input("Escolha A OPÇÃO: "))
  except ValueError:
    print(Fore.RED + "Digite um número válido!" + Style.RESET_ALL) 
    continue

# Cadastro de novo produto no banco de dados
  if opcao == op_cadastro:
    nome = input(Fore.BLUE + "Digite o NOME DO PRODUTO: " + Style.RESET_ALL)
    preco = int(input(Fore.BLUE + "Digite o PREÇO: " + Style.RESET_ALL))
    cursor.execute(         #EXECUTANDO COMANDO SQL
      "INSERT INTO usuarios (nome, preco) VALUES (?, ?)", 
      (nome, preco)
    )
    conn.commit()
    produto = {
      "nome": nome,
      "preco": preco
    }
  
  # Consultar exibição de todos os produtos cadastrado
  elif opcao == op_listarproduto:
    cursor.execute( "SELECT * FROM usuarios") #SELECIONA TABELA DE USUARIOS/PRODUTOS NO SQL E PEGA RESULTADO COM FETCHALL
    dados = cursor.fetchall()
    
    for produto in dados:
      print(f"{produto[0]} - {produto[1]} | R$ {produto[2]}")

  # Seleção de produto e criação de pedido com cálculo de valor total
  elif opcao == op_fazerpedidos:
    escolher = int(input("ESCOLHA O ID DO PRODUTO: "))
    produto_escolhido = None
    for produto in dados:
      if produto[0] == escolher:
        produto_escolhido = produto
        break
    if produto_escolhido is None:
      print("Produto não encontrado.")
      continue
    
    try:        
     quantidade = int(input("DIGITE QUANTIDADE: "))
    except:
      print("Digite um número válido!")
      continue
    total = produto_escolhido[2] * quantidade
    print(Fore.LIGHTGREEN_EX + f"✔ PRODUTO: {produto[1]} | TOTAL: R$ {total:.2f}" + Style.RESET_ALL)

  
     # Inserir Pedidos no SQL / Persistência do pedido no banco de dados
    print(Fore.RED + "\n--- LISTA DE PEDIDOS ---" + Style.RESET_ALL)
    cursor.execute(
       "INSERT INTO pedidos (nome_produto, quantidade, total ) VALUES (?, ?, ?)",
       (produto_escolhido[1], quantidade, total) 
    )
    conn.commit()
  
    # Consultar exibição de todos os pedidos realizados
  elif opcao == op_listarpedidos:
     cursor.execute("SELECT * FROM pedidos") 
     dados = cursor.fetchall()

     for pedido in dados: 
      print(f"ID: {pedido[0]} - {pedido[1]} | QNT: {pedido[2]} - R$ {pedido[3]}")


    # Cálculo do faturamento total com base nos pedidos registrados
  elif opcao == op_fatur:
    cursor.execute("SELECT * FROM pedidos")
    dados = cursor.fetchall()

    if not dados:
      print(Fore.RED + "NENHUM PEDIDO AINDA " + Style.RESET_ALL)
    else:
      total_geral = 0
    for pedido in dados:
      total_geral += pedido[3]
      print(Fore.LIGHTGREEN_EX + f"FATURAMENTO TOTAL: {total_geral}" + Style.RESET_ALL)


    # Geração de relatório consolidade (ETL SIMPLIFICADO)
    # Extração: SELECT no banco
    # Transformação: soma e contagem
    # Carga: exibição no terminal
  elif opcao == op_relat:  
    cursor.execute("SELECT * FROM pedidos")
    dados = cursor.fetchall()
    total_geral = 0
    contador_pedidos = 0 
  for pedido in dados: 
     total_geral += pedido[3]
     contador_pedidos += 1
  print(Fore.LIGHTRED_EX + "\n ---- RELATÓRIO ----" + Style.RESET_ALL)
  print(Fore.LIGHTGREEN_EX + f"Faturamento Total: R${total_geral:.2f}" + Style.RESET_ALL)
  print(Fore.LIGHTYELLOW_EX + f"Total de Pedidos: {contador_pedidos}" + Style.RESET_ALL)


 