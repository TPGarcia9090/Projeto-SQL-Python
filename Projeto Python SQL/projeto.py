from classes import *

cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    quantidade INTEGER,
                    preco REAL
                  )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Vendas (
                    id_venda INTEGER PRIMARY KEY,
                    id_produto INTEGER,
                    quantidade INTEGER,
                    data_venda TEXT,
                    FOREIGN KEY(id_produto) REFERENCES Produtos(id)
                  )''')

conn.commit()

def menu():
    print("\n--- Sistema de Gerenciamento de Estoque ---")
    print("1. Adicionar Produto")
    print("2. Atualizar Estoque")
    print("3. Visualizar Estoque")
    print("4. Registrar Venda")
    print("5. Gerar Relatório de Estoque")
    print("6. Gerar Relatório de Vendas")
    print("7. Sair")

def iniciar_sistema():
    estoque = GerenciadorEstoque()

    while True:
        menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome do produto: ")
            descricao = input("Descrição do produto: ")
            quantidade = int(input("Quantidade disponível: "))
            preco = float(input("Preço: "))
            produto = Produto(nome, descricao, quantidade, preco)
            estoque.adicionar_produto(produto)
            print("Produto adicionado com sucesso!")

        elif escolha == '2':
            produto_id = int(input("ID do produto a ser atualizado: "))
            nova_quantidade = int(input("Nova quantidade: "))
            estoque.atualizar_estoque(produto_id, nova_quantidade)
            print("Estoque atualizado!")

        elif escolha == '3':
            estoque.visualizar_estoque()

        elif escolha == '4':
            id_produto = int(input("ID do produto vendido: "))
            quantidade = int(input("Quantidade vendida: "))
            data_venda = input("Data da venda (Ano-Mês-Data): ")
            estoque.registrar_venda(id_produto, quantidade, data_venda)

        elif escolha == '5':
            estoque.gerar_relatorio_estoque()

        elif escolha == '6':
            estoque.gerar_relatorio_vendas()

        elif escolha == '7':
            print("Saindo do sistema.")
            estoque.fechar_conexao()
            break

        else:
            print("Opção inválida, tente novamente.")

iniciar_sistema()