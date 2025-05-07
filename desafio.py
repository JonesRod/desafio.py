import textwrap  # Import necessário para formatar o texto
from datetime import datetime  # Import necessário para registrar data e hora

# Função para exibir o menu de operações
def menu():
    # Exibe as opções disponíveis para o usuário
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para realizar o depósito
def depositar(saldo, valor, extrato, /):
    # Verifica se o valor do depósito é válido
    if valor > 0:
        saldo += valor  # Atualiza o saldo
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Registra a data e hora
        extrato += f"{data_hora} Depósito:\tR$ {valor:.2f}\n"  # Adiciona ao extrato
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato  # Retorna o saldo atualizado e o extrato

# Função para realizar o saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Verifica se o saque respeita as condições
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor  # Atualiza o saldo
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Registra a data e hora
        extrato += f"[{data_hora}] Saque:\t\tR$ {valor:.2f}\n"  # Adiciona ao extrato
        numero_saques += 1  # Incrementa o número de saques
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato  # Retorna o saldo atualizado e o extrato

# Função para exibir o extrato da conta
def exibir_extrato(saldo, /, *, extrato):
    # Exibe as transações realizadas e o saldo atual
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    # Solicita os dados do usuário
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adiciona o novo usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

# Função para buscar um usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    # Retorna o usuário correspondente ao CPF ou None se não encontrado
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta bancária
def criar_conta(agencia, numero_conta, usuarios):
    # Solicita o CPF do usuário e verifica se ele está cadastrado
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

# Função para listar todas as contas cadastradas
def listar_contas(contas):
    # Exibe as informações de cada conta
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# Função para iniciar o programa
def iniciar_programa():
    # Exibe a tela inicial e solicita a escolha do usuário
    print("Bem-vindo ao sistema bancário!")
    while True:
        opcao = input("\nEscolha uma operação:\n[1] Abrir uma conta\n[2] Acessar minha conta\n=> ")
        if opcao in ["1", "2"]:
            return opcao
        else:
            print("Opção inválida. Por favor, escolha novamente.")

# Função para acessar uma conta existente
def acessar_conta(usuarios, contas):
    # Solicita o CPF e verifica se há uma conta associada
    cpf = input("Informe o CPF para acessar sua conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado! Certifique-se de que o CPF está correto ou crie uma conta. @@@")
        return None

    conta_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
    if not conta_usuario:
        print("\n@@@ Nenhuma conta encontrada para este CPF. @@@")
        return None

    print("\n=== Conta acessada com sucesso! ===")
    return conta_usuario[0]

# Função principal que gerencia o fluxo do programa
def main():
    # Define os limites e inicializa as variáveis
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    # Loop principal do programa
    while True:
        opcao_inicial = iniciar_programa()

        if opcao_inicial == "1":
            # Fluxo para abrir uma nova conta
            print("\n=== Fluxo de abertura de conta ===")
            criar_usuario(usuarios)
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                print("\nConta criada com sucesso! Você pode acessá-la agora.")
            else:
                print("\nNão foi possível criar a conta. Reinicie o programa para tentar novamente.")

        elif opcao_inicial == "2":
            # Fluxo para acessar uma conta existente
            print("\n=== Acessando conta existente ===")
            conta = acessar_conta(usuarios, contas)
            if not conta:
                continue  # Retorna ao início se não encontrar a conta

            while True:
                opcao = menu()

                if opcao == "d":
                    # Realiza um depósito
                    valor = float(input("Informe o valor do depósito: "))
                    saldo, extrato = depositar(saldo, valor, extrato)

                elif opcao == "s":
                    # Realiza um saque
                    valor = float(input("Informe o valor do saque: "))
                    saldo, extrato = sacar(
                        saldo=saldo,
                        valor=valor,
                        extrato=extrato,
                        limite=limite,
                        numero_saques=numero_saques,
                        limite_saques=LIMITE_SAQUES,
                    )

                elif opcao == "e":
                    # Exibe o extrato
                    exibir_extrato(saldo, extrato=extrato)

                elif opcao == "nu":
                    # Cria um novo usuário
                    criar_usuario(usuarios)

                elif opcao == "nc":
                    # Cria uma nova conta
                    numero_conta = len(contas) + 1
                    conta = criar_conta(AGENCIA, numero_conta, usuarios)
                    if conta:
                        contas.append(conta)

                elif opcao == "lc":
                    # Lista todas as contas
                    listar_contas(contas)

                elif opcao == "q":
                    # Sai do menu e retorna à escolha inicial
                    print("\nVoltando para a escolha inicial de operação...")
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")

# Inicia o programa
main()