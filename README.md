# 💼💳 Sistema Bancário - Desafio de POO(Programação orientada a objetos)

Este projeto é um sistema bancário desenvolvido em Python utilizando Programação Orientada a Objetos (POO). O sistema inclui classes para representar clientes, contas bancárias, transações e histórico.

## ▶ Demonstração





https://github.com/Amadeo-Frontend/Python-Sistema__bancario__POO/assets/104178969/83289e81-5f0d-4b43-b4c9-34e8a9f44afe





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

### Data e Hora 🕐

O projeto utiliza uma implementação robusta de data e hora, que não apenas registra transações com precisão, mas também apresenta essas informações de forma clara e organizada, permitindo aos usuários uma compreensão instantânea das atividades em suas contas

### Implementação do Log e do log.txt 💾

O projeto inclui uma funcionalidade de log para registrar eventos importantes, como a criação de novos clientes e contas. O log é feito utilizando o módulo logging do Python e é armazenado no arquivo log.txt. Cada registro no arquivo de log contém informações detalhadas, incluindo o tipo de operação realizada, o nome do cliente, o número da conta e a data e hora em que a operação ocorreu. Isso oferece uma forma organizada e fácil de rastrear as atividades dentro do sistema bancário, proporcionando transparência e controle sobre as operações realizadas.

## Uso 🚀

O programa principal está no arquivo `desafio_v2.py`. Basta executá-lo para interagir com o sistema bancário através de um menu interativo no terminal.

## Dependências 🔧

Este projeto utiliza a biblioteca `colorama` para adicionar cores ao terminal. Para instalar essa biblioteca, execute o seguinte comando no terminal:

```
pip install colorama
```

## Contribuição 🧾

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para
sugestões, reportar bugs ou propor melhorias. Se deseja contribuir diretamente,
faça um fork do repositório, crie uma branch para suas modificações e abra um
pull request.

## Suporte 💻

Se você encontrar algum problema ou tiver dúvidas sobre o uso deste projeto, por
favor, abra um issue para discussão.

Feito com ❤️ por Amadeo Bon para contribuir com a comunidade de desenvolvimento
Python. Boa codificação!
