''' 
Para ler e escrever dados em Python, utilizamos as seguintes funções: 
- input: lê UMA linha com dado(s) de Entrada do usuário;
- print: imprime um texto de Saída (Output), pulando linha.  
'''

class ContaBancaria:
    # Método construtor para inicializar a conta com nome do titular, saldo 0 e lista de operações
    def __init__(self, titular):
        self.titular = titular         # Nome do dono da conta
        self.saldo = 0                 # Saldo inicial da conta
        self.operacoes = []           # Lista para registrar as operações realizadas

    # Método para depositar um valor na conta
    def depositar(self, valor):
        self.saldo += valor                            # Adiciona o valor ao saldo
        self.operacoes.append(f"+{valor}")             # Registra a operação como depósito

    # Método para realizar um saque
    def sacar(self, valor):
        # Verifica se há saldo suficiente para o saque (valor é negativo)
        if self.saldo + valor >= 0:
            self.saldo += valor                        # Subtrai o valor do saldo (valor negativo)
            self.operacoes.append(str(valor))          # Registra a operação como saque
        else:
            self.operacoes.append("Saque não permitido")  # Registra que o saque foi negado

    # Método para exibir o extrato das operações e o saldo final
    def extrato(self):
        operacoes_str = ", ".join(self.operacoes)      # Junta as operações separadas por vírgula
        print(f"Operações: {operacoes_str}; Saldo: {self.saldo}")  # Imprime o resultado final

# Lê o nome do titular da conta
nome_titular = input().strip()

# Cria uma nova conta bancária com o nome do titular
conta = ContaBancaria(nome_titular)

# Lê a linha com os valores das transações e divide por vírgula
entrada_transacoes = input().strip()
transacoes = [int(valor) for valor in entrada_transacoes.split(",")]

# Processa cada valor da lista de transações
for valor in transacoes:
    if valor > 0:
        conta.depositar(valor)    # Se for positivo, é um depósito
    else:
        conta.sacar(valor)        # Se for negativo ou zero, tenta sacar

# Exibe o extrato final da conta
conta.extrato()