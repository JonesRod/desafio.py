''' 
Para ler e escrever dados em Python, utilizamos as seguintes funções: 
- input: lê UMA linha com dado(s) de Entrada do usuário;
- print: imprime um texto de Saída (Output), pulando linha.  
'''

class ContaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular   # Nome do titular da conta
        self.saldo = saldo       # Saldo inicial da conta

class SistemaBancario:
    def __init__(self):
        self.contas = []  # Inicializa a lista que irá armazenar todas as contas

    def criar_conta(self, titular, saldo):
        conta = ContaBancaria(titular, saldo)  # Cria uma nova instância de ContaBancaria
        self.contas.append(conta)              # Adiciona a conta à lista de contas

    def listar_contas(self):
        # Gera uma lista de strings no formato "Titular: R$ Saldo"
        lista_formatada = [f"{conta.titular}: R$ {conta.saldo}" for conta in self.contas]
        # Junta os elementos com vírgula e espaço, e imprime
        print(", ".join(lista_formatada))
  

# Cria uma instância do sistema bancário
sistema = SistemaBancario()

# Loop para ler entradas até que o comando "FIM" seja digitado
while True:
    entrada = input().strip()
    if entrada.upper() == "FIM":
        break  # Encerra o loop se o usuário digitar "FIM"
    
    # Divide a entrada no formato "Titular, Saldo"
    titular, saldo = entrada.split(", ")
    sistema.criar_conta(titular, int(saldo))  # Cria a conta com nome e saldo convertidos

# Após o fim das entradas, lista todas as contas cadastradas
sistema.listar_contas()
