# Prova Final - Tecnologias Web

## Iniciando o Projeto
Para verificar o projeto basta apenas rodar os comandos na pasta principal:
* source env/bin/activate
* python3 manage.py runserver

## Restrições Impostas pela Prova
* Os 3 passos devem ser repetidos para cada nova requisição, ou seja, um novo selo será gerado a cada vez que o usuário recarregar a página;
* As requisições devem ser feitas através do código (não utilizando alguma ferramenta externa como o Postman ou a própria ferramenta interativa disponível na documentação);
* Você deve implementar essa funcionalidade usando o seu Projeto 2 como base e o selo deve ser apresentado na página inicial. Ou seja, você não pode criar uma nova página separada para mostrar essa imagem.

## Verificação da Resolução (Código)

As alterações foram feitas nos arquivos:
* Index.html (Página principal de Login, que apresenta a imagem obtida pela API no centro da página)
* views.py (Dentro da função login (linha 23-35): Faz a requisição do token via GET, depois usa esse token para obter o link da imagem via POST, e por fim passa esse link para o render do Index.html via a variável "selo")

# Comprovação da Resolução

Conforme as restrições impostas pela prova, a funcionalidade faz requisições GET de token e POST para obter as imagens atualizadas a cada refresh da página principal, e é mostrado no centro dela.

Estas imagens validam a resolução do exercício, mostrando a imagem obtida pela API fornecida no exercício da Prova na home page do Projeto 2 - Aries.

<p align="center">
  <img src="https://user-images.githubusercontent.com/60860861/120318254-05148780-c2b6-11eb-8824-99cc640e3946.png" width="600" height="500"></img>
  <img src="https://user-images.githubusercontent.com/60860861/120318257-06de4b00-c2b6-11eb-93cc-5ae81e81505a.png" width="600" height="500"></img>
  <img src="https://user-images.githubusercontent.com/60860861/120318265-08a80e80-c2b6-11eb-9fe9-fe456e80bf89.png" width="600" height="500"></img>
</p>
