# 💼💳 Sistema Bancário - Desafio de POO(Programação orientada a objetos)

Este projeto é um sistema bancário desenvolvido em Python utilizando Programação Orientada a Objetos (POO). O sistema inclui classes para representar clientes, contas bancárias, transações e histórico.

## Funcionalidades 🛠️

### Cliente 👤

A classe `Cliente` representa os clientes do banco. Cada cliente possui um endereço e pode ter uma ou mais contas bancárias associadas.

### Pessoa Fisica 🧑

A classe `PessoaFisica` é uma subclasse de `Cliente`, que adiciona atributos específicos para representar pessoas físicas, como nome, data de nascimento e CPF.

### Conta 💰

A classe `Conta` representa uma conta bancária. Cada conta possui um número, uma agência, um saldo, um cliente associado e um histórico de transações. As contas podem ser de diferentes tipos, como conta corrente ou poupança.

### Conta Corrente 🏦

A classe `ContaCorrente` é uma subclasse de `Conta`, que adiciona atributos específicos para contas correntes, como limite de saldo e limite de saques.

### Transacao 🔄

A classe abstrata `Transacao` representa uma transação bancária. Possui métodos abstratos para realizar e registrar transações.

### Saque 💸 e Deposito 💳

As classes `Saque` e `Deposito` são subclasse de `Transacao`, que representam transações de saque e depósito, respectivamente. Elas implementam os métodos abstratos de `Transacao`.

## Uso 🚀

O programa principal está no arquivo `desafio_v2.py`. Basta executá-lo para interagir com o sistema bancário através de um menu interativo no terminal.

## Dependências 📦

Este projeto utiliza a biblioteca Colorama para adicionar cores ao terminal e a biblioteca Emoji para adicionar emojis às mensagens de saída.

Para instalar as dependências, execute o seguinte comando:
