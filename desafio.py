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
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para realizar o depósito
def depositar(saldo, valor, extrato, /):
    # Permite cancelar o depósito digitando 'x'
    valor_str = input("Informe o valor do depósito ou digite 'x' e tecle Enter para cancelar: ")
    if valor_str.lower() == "x":
        print("Operação de depósito cancelada.")
        return saldo, extrato
    try:
        valor = float(valor_str)
    except ValueError:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato

    if valor > 0:
        saldo += valor
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora} Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

# Função para realizar o saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Permite cancelar o saque digitando 'x'
    valor_str = input("Informe o valor do saque ou digite 'x' e tecle Enter para cancelar: ")
    if valor_str.lower() == "x":
        print("Operação de saque cancelada.")
        return saldo, extrato
    try:
        valor = float(valor_str)
    except ValueError:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato

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
        saldo -= valor
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"[{data_hora}] Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

# Função para exibir o extrato da conta
def exibir_extrato(saldo, /, *, extrato):
    # Exibe as transações realizadas e o saldo atual
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    # Solicita os dados do usuário, permitindo cancelar a qualquer momento digitando 'x'
    cpf = input("Informe o CPF (somente número) ou digite 'x' e tecle Enter para cancelar: ")
    if cpf.lower() == "x":
        print("Operação de criação de usuário cancelada.")
        return False

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return False

    nome = input("Informe o nome completo ou digite 'x' e tecle Enter para cancelar: ")
    if nome.lower() == "x":
        print("Operação de criação de usuário cancelada.")
        return False

    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa) ou digite 'x' e tecle Enter para cancelar: ")
    if data_nascimento.lower() == "x":
        print("Operação de criação de usuário cancelada.")
        return False

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado) ou digite 'x' e tecle Enter para cancelar: ")
    if endereco.lower() == "x":
        print("Operação de criação de usuário cancelada.")
        return False

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")
    return True

# Função para buscar um usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    # Retorna o usuário correspondente ao CPF ou None se não encontrado
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta bancária
def criar_conta(agencia, numero_conta, usuarios):
    # Solicita o CPF do usuário e verifica se ele está cadastrado, permitindo cancelar com 'x'
    cpf = input("Informe o CPF do usuário ou digite 'x' e tecle Enter para cancelar: ")
    if cpf.lower() == "x":
        print("Operação de criação de conta cancelada.")
        return None

    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None

    print("\n=== Conta criada com sucesso! ===")
    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

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
        opcao = input('\nEscolha uma operação:\n[1] Novo usuário\n[2] Acessar Minha Conta\n=> ')
        if opcao in ["1", "2"]:
            return opcao
        else:
            print("Opção inválida. Por favor, escolha novamente.")

# Função para acessar uma conta existente
def acessar_conta(usuarios, contas):
    # Solicita o CPF e verifica se há uma conta associada, permitindo cancelar com 'x'
    cpf = input("Informe o CPF para acessar sua conta ou digite 'x' e tecle Enter para cancelar: ")
    if cpf.lower() == "x":
        print("Operação de acesso à conta cancelada.")
        return None

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
            # Fluxo para criar um novo usuário e abrir uma conta
            print('\n=== Fluxo para novo usuário ===\n//// Para cancelar digite "x"')
            usuario_criado = criar_usuario(usuarios)
            if not usuario_criado:
                continue  # Se cancelou, volta ao menu inicial
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                print("\nConta criada com sucesso! Você pode acessá-la agora.")
            else:
                print("\nNão foi possível criar a conta ou operação cancelada.")

        elif opcao_inicial == "2":
            # Fluxo para acessar uma conta existente
            print("\n=== Acessando conta existente ===")
            conta = acessar_conta(usuarios, contas)
            if not conta:
                continue  # Retorna ao início se não encontrar a conta

            while True:
                opcao = menu()

                if opcao == "d":
                    saldo, extrato = depositar(saldo, 0, extrato)  # valor será solicitado dentro da função

                elif opcao == "s":
                    saldo, extrato = sacar(
                        saldo=saldo,
                        valor=0,  # valor será solicitado dentro da função
                        extrato=extrato,
                        limite=limite,
                        numero_saques=numero_saques,
                        limite_saques=LIMITE_SAQUES,
                    )

                elif opcao == "e":
                    # Exibe o extrato
                    exibir_extrato(saldo, extrato=extrato)

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