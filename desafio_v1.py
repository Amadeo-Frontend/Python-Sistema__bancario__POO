import textwrap
from colorama import Fore, Style  # Importando cores para o terminal
from datetime import datetime
from abc import ABC, abstractmethod  # Importando ABC e abstractmethod

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
            print(Fore.RED + "\n❌❌❌ Operação falhou! Você não tem saldo suficiente. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
        elif valor > 0:
            self._saldo -= valor
            print(Fore.GREEN + "\n✅✅✅ Saque realizado com sucesso! ✅✅✅")
            print(Style.RESET_ALL)  # Resetando a cor
            return True
        else:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(Fore.GREEN + "\n✅✅✅ Depósito realizado com sucesso! ✅✅✅")
            print(Style.RESET_ALL)  # Resetando a cor
        else:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor do saque excede o limite. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
        elif excedeu_saques:
            print(Fore.RED + "\n❌❌❌ Operação falhou! Número máximo de saques excedido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
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
