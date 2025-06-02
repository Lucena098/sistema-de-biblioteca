class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.alugado_por = None

    def esta_disponivel(self):
        return self.alugado_por is None

    def __str__(self):
        if self.esta_disponivel():
            status = "Disponível"
        elif isinstance(self.alugado_por, Pessoa):
            status = f"Alugado por {self.alugado_por.nome}"
        else:
            status = "Alugado (erro de dados)"
        return f'"{self.titulo}" ({self.ano}) de {self.autor} - {status}'


class Pessoa:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.livros_alugados = []

    def alugar_livro(self, livro):
        if livro.esta_disponivel():
            livro.alugado_por = self
            self.livros_alugados.append(livro)
            return f'{self.nome} alugou o livro "{livro.titulo}".'
        else:
            return f"O livro {livro.titulo} já está alugado por {livro.alugado_por.nome}"

    def devolver_livro(self, livro):
        if livro in self.livros_alugados:
            livro.alugado_por = None
            self.livros_alugados.remove(livro)
            return f'{self.nome} devolveu o livro "{livro.titulo}".'
        else:
            return f'{self.nome} não possui o livro "{livro.titulo}".'


class Biblioteca:
    def __init__(self):
        self.livros = []
        self.pessoas = []

    def adicionar_livro(self, titulo, autor, ano):
        livro = Livro(titulo, autor, ano)
        self.livros.append(livro)
        return f'Livro "{titulo}" ({ano}) de {autor} adicionado à biblioteca.'

    def cadastrar_pessoa(self, nome, cpf, telefone):
        for p in self.pessoas:
            if p.cpf == cpf:
                return None
        pessoa = Pessoa(nome, cpf, telefone)
        self.pessoas.append(pessoa)
        return pessoa

    def listar_livros_disponiveis(self):
        return [livro for livro in self.livros if livro.esta_disponivel()]

    def listar_livros_alugados(self):
        return [livro for livro in self.livros if not livro.esta_disponivel()]

    def encontrar_pessoa(self, cpf):
        for pessoa in self.pessoas:
            if pessoa.cpf == cpf:
                return pessoa
        return None


def menu():
    biblioteca = Biblioteca()

    while True:
        print("\n=== MENU DA BIBLIOTECA ===")
        print("1. Adicionar livro")
        print("2. Cadastrar pessoa")
        print("3. Alugar livro")
        print("4. Devolver livro")
        print("5. Listar livros disponíveis")
        print("6. Listar livros alugados")
        print("7. Procurar pessoa cadastrada")
        print("8. Sair")

        opcao = input("Escolha uma opção (1-8): ")

        if opcao == "1":
            titulo = input("Título do livro: ")
            autor = input("Autor do livro: ")
            try:
                ano = int(input("Ano de lançamento: "))
            except ValueError:
                print("Ano inválido. Use apenas números.")
                continue
            print(biblioteca.adicionar_livro(titulo, autor, ano))

        elif opcao == "2":
            nome = input("Nome da pessoa: ")
            cpf = input("CPF: ")
            telefone = input("Telefone: ")
            pessoa = biblioteca.cadastrar_pessoa(nome, cpf, telefone)
            if pessoa:
                print(f'Pessoa "{pessoa.nome}" cadastrada com CPF {pessoa.cpf} e telefone {pessoa.telefone}.')
            else:
                print("CPF já cadastrado. Cadastro não realizado.")

        elif opcao == "3":
            cpf = input("CPF da pessoa: ")
            pessoa = biblioteca.encontrar_pessoa(cpf)
            if not pessoa:
                print("Pessoa não encontrada.")
                continue

            livros_disp = biblioteca.listar_livros_disponiveis()
            if not livros_disp:
                print("Nenhum livro disponível.")
                continue

            print("Livros disponíveis:")
            for i, livro in enumerate(livros_disp):
                print(f"{i + 1}. {livro}")

            escolha = input("Escolha o número do livro: ")
            if escolha.isdigit() and 0 < int(escolha) <= len(livros_disp):
                livro_escolhido = livros_disp[int(escolha) - 1]
                print(pessoa.alugar_livro(livro_escolhido))
            else:
                print("Escolha inválida.")

        elif opcao == "4":
            cpf = input("CPF da pessoa: ")
            pessoa = biblioteca.encontrar_pessoa(cpf)
            if not pessoa:
                print("Pessoa não encontrada.")
                continue

            if not pessoa.livros_alugados:
                print("Essa pessoa não tem livros alugados.")
                continue

            print("Livros alugados por essa pessoa:")
            for i, livro in enumerate(pessoa.livros_alugados):
                print(f"{i + 1}. {livro}")

            escolha = input("Escolha o número do livro para devolver: ")
            if escolha.isdigit() and 0 < int(escolha) <= len(pessoa.livros_alugados):
                livro_escolhido = pessoa.livros_alugados[int(escolha) - 1]
                print(pessoa.devolver_livro(livro_escolhido))
            else:
                print("Escolha inválida.")

        elif opcao == "5":
            livros = biblioteca.listar_livros_disponiveis()
            if livros:
                print("Livros disponíveis:")
                for livro in livros:
                    print("-", livro)
            else:
                print("Nenhum livro disponível.")

        elif opcao == "6":
            livros = biblioteca.listar_livros_alugados()
            if livros:
                print("Livros alugados:")
                for livro in livros:
                    print("-", livro)
            else:
                print("Nenhum livro alugado.")

        elif opcao == "7":
            cpf = input("Digite o CPF da pessoa para buscar: ")
            pessoa = biblioteca.encontrar_pessoa(cpf)
            if pessoa:
                print(f'Nome: {pessoa.nome}')
                print(f'CPF: {pessoa.cpf}')
                print(f'Telefone: {pessoa.telefone}')
                if pessoa.livros_alugados:
                    print("Livros alugados:")
                    for livro in pessoa.livros_alugados:
                        print(f"- {livro}")
                else:
                    print("Nenhum livro alugado por essa pessoa.")
            else:
                print("Pessoa não encontrada.")

        elif opcao == "8":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
