import sqlite3

class Produto:
    def __init__(self, nome, descricao, quantidade, preco):
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco

    def salvar_no_banco(self, cursor, conn):
        cursor.execute("INSERT INTO Produtos (nome, descricao, quantidade, preco) VALUES (?, ?, ?, ?)",
                       (self.nome, self.descricao, self.quantidade, self.preco))
        conn.commit()
    
class Venda:
    def __init__(self, id_produto, quantidade, data_venda):
            self.id_produto = id_produto
            self.quantidade = quantidade
            self.data_venda = data_venda

    def salvar_no_banco(self, cursor, conn):
        cursor.execute("INSERT INTO Vendas (id_produto, quantidade, data_venda) VALUES (?, ?, ?)",
                       (self.id_produto, self.quantidade, self.data_venda))
        cursor.execute("UPDATE Produtos SET quantidade = quantidade - ? WHERE id = ?",
                       (self.quantidade, self.id_produto))
        conn.commit()

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

class GerenciadorEstoque:
    def __init__(self):
        self.conn = sqlite3.connect('estoque.db')
        self.cursor = self.conn.cursor()

    def adicionar_produto(self, produto):
        produto.salvar_no_banco(self.cursor, self.conn)

    def atualizar_estoque(self, produto_id, quantidade):
        self.cursor.execute("UPDATE Produtos SET quantidade = ? WHERE id = ?", (quantidade, produto_id))
        self.conn.commit()

    def visualizar_estoque(self):
        self.cursor.execute("SELECT * FROM Produtos")
        produtos = self.cursor.fetchall()
        for produto in produtos:
            print(produto)
    
    def fechar_conexao(self):
        self.conn.close()

    def registrar_venda(self, id_produto, quantidade, data_venda):
        self.cursor.execute("SELECT quantidade FROM Produtos WHERE id = ?", (id_produto,))
        estoque_disponivel = self.cursor.fetchone()[0]
    
        if estoque_disponivel >= quantidade:
            venda = Venda(id_produto, quantidade, data_venda)
            venda.salvar_no_banco(self.cursor, self.conn)
            print("Venda registrada com sucesso!")
        else:
            print("Quantidade insuficiente no estoque!")

    def gerar_relatorio_estoque(self):
        self.cursor.execute("SELECT nome, descricao, quantidade, preco FROM Produtos")
        produtos = self.cursor.fetchall()
        print("\n--- Relatório de Estoque ---")
        
        for produto in produtos:
            print(f"Nome: {produto[0]}, Descrição: {produto[1]}, Quantidade: {produto[2]}, Preço: {produto[3]}")
    
    def gerar_relatorio_vendas(self):
        self.cursor.execute('''SELECT Vendas.id_venda, Produtos.nome, Vendas.quantidade, Vendas.data_venda 
                           FROM Vendas 
                           JOIN Produtos ON Vendas.id_produto = Produtos.id''')
        vendas = self.cursor.fetchall()
        print("\n--- Relatório de Vendas ---")
        
        for venda in vendas:
            print(f"ID Venda: {venda[0]}, Produto: {venda[1]}, Quantidade: {venda[2]}, Data: {venda[3]}")