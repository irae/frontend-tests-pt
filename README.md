Automatizando testes de Javascript no front-end
===============================================

## Iraê Carvalho

Nos últimos anos a internet deixou de ser só conteúdo – hoje usamos aplicações complexas que facilmente chegam a 5mil linhas de código Javascript. Como garantir uma aplicação sem bugs? Como garantir que novas funcionalidades não criem bugs em códigos antigos? Como fazer isso de forma automática? Para responder essas perguntas veremos ferramentas de testes unitários, validadores de sintaxe, cobertura, compactação, testes de integração, scripts de automação, e finalmente integração contínua.



----------------------------------------------------------------------

## Repositório de exemplos

Este repositório contém os slides e as ferramentas e códigos open source que serão/foram apresentados na palestra. Tudo que está aqui é por motivo didático e qualquer uso comercial deve atentar as licenças de cada software incluso.

A versão atual foi/será apresentada no BH.js em Belo Horizonte, MG, Brasil em 21 de Janeiro de 2012.

## Slides da palestra

Os slides em formato texto incluindo comentários que fiz para me guiar durante a palestra estão disponíveis:

* Visualizar slides: [http://irae.github.com/frontend-tests-pt/](http://irae.github.com/frontend-tests-pt/)
* Slides em formato texto: [slides.md](https://github.com/irae/frontend-tests-pt/blob/master/slides.md)

## Usando esse repositório:

Para usar tudo que está no repositório siga os passos:

* Instale o VirtualEnv e o VituralEnvWrapper (no google é fácil de achar tutoriais dessa instalação)
* Rode os comandos abaixo pra baixar o repositório, criar um virtualenv e baixar os arquivos extras:

```sh
# vá para a pasta que vc quer baixar o projeto
git clone git://github.com/irae/frontend-tests-pt.git
cd frontend-tests-pt
mkvirtualenv fe-tests
make downloads
make
```

Após isso você pode ler os slides, ou usar os outros comandos do makefile pra fazer as demais tarefas. Se tiver dúvidas, poste nos [issues](https://github.com/irae/frontend-tests-pt/issues) do projeto.
