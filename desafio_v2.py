import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from colorama import Fore, Style


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M")
        tipo_transacao = transacao.__class__.__name__
        valor_transacao = transacao.valor

        registro_transacao = f"{Fore.CYAN}Tipo: {tipo_transacao} | Valor: R$ {valor_transacao:.2f} | Data e Hora: {data_hora}{Style.RESET_ALL}"
        self._transacoes.append(
            {
                "tipo": tipo_transacao,
                "valor": valor_transacao,
                "data": data_hora,
                "registro": registro_transacao,
            }
        )


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(
                Fore.RED
                + "\n❌❌❌ Operação falhou! Você não tem saldo suficiente. ❌❌❌"
            )
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        elif valor <= 0:
            print(
                Fore.RED
                + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌"
            )
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo -= valor
        print(
            Fore.GREEN
            + f"\n✅✅✅ Saque realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M')} ✅✅✅"
        )
        print(Style.RESET_ALL)  # Resetando a cor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print(
                Fore.RED
                + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌"
            )
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo += valor
        print(
            Fore.GREEN
            + f"\n✅✅✅ Depósito realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M')} ✅✅✅"
        )
        print(Style.RESET_ALL)  # Resetando a cor
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = sum(
            1
            for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(
                Fore.RED
                + "\n❌❌❌ Operação falhou! O valor do saque excede o limite. ❌❌❌"
            )
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        elif excedeu_saques:
            print(
                Fore.RED
                + "\n❌❌❌ Operação falhou! Número máximo de saques excedido. ❌❌❌"
            )
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""{Fore.CYAN}
    ========== CONTA CORRENTE ==========
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
    {Style.RESET_ALL}"""


def menu():
    menu_text = f"""{Fore.CYAN + Style.BRIGHT}
    ================ MENU ================
    [d]💰\tDepositar
    [s]💸\tSacar
    [e]📊\tExtrato
    [nc]📋\tNova conta
    [nu]👤\tNovo usuário
    [lc]📄\tListar contas
    [q]🚪\tSair
    => {Style.RESET_ALL}"""
    return input(textwrap.dedent(menu_text))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(Fore.YELLOW + "\n❗❗❗ Cliente não possui conta! ❗❗❗")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print(Fore.CYAN + "\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            tipo_transacao = transacao["tipo"]
            texto_formatado = f"\n{Fore.YELLOW}{tipo_transacao} ({transacao['data']}):\n\tR$ {transacao['valor']:.2f}{Style.RESET_ALL}"
            # Verificar se a transação é um saque e alterar a cor do texto para vermelho
            if tipo_transacao == "Saque":
                texto_formatado = f"{Fore.RED}{texto_formatado}{Style.RESET_ALL}"

            extrato += texto_formatado

    print(extrato)
    print(f"\n{Fore.CYAN}Saldo:\n\tR$ {conta.saldo:.2f}{Style.RESET_ALL}")
    print(Fore.CYAN + "==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    print(
        Fore.GREEN
        + f"\n✅✅✅ Cliente criado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M')} ✅✅✅"
    )
    print(Style.RESET_ALL)  # Resetando a cor


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(
            Fore.RED
            + "\n❌❌❌ Cliente não encontrado, fluxo de criação de conta encerrado! ❌❌❌"
        )
        print(Style.RESET_ALL)  # Resetando a cor
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(
        Fore.GREEN
        + f"\n✅✅✅ Conta criada com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M')} ✅✅✅"
    )
    print(Style.RESET_ALL)  # Resetando a cor


def listar_contas(contas):
    for conta in contas:
        print(Fore.CYAN + "=" * 100)
        print(Fore.YELLOW + str(conta) + Style.RESET_ALL)


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print(
                Fore.RED
                + "\n❌❌❌ Operação inválida, por favor selecione novamente a operação desejada. ❌❌❌"
            )
            print(Style.RESET_ALL)  # Resetando a cor


if __name__ == "__main__":
    main()
