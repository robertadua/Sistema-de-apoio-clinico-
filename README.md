# Sistema-de-apoio-clínico (Clínio)

# 1) Tema do Projeto

O projeto tem como tema o desenvolvimento de uma plataforma de apoio clínico baseada em banco de dados NoSQL, voltada para a organização, integração e análise de informações médicas.

A proposta consiste na criação de um sistema que centraliza o histórico completo dos pacientes em uma estrutura flexível e escalável, permitindo o armazenamento de dados como consultas, sintomas, diagnósticos, prescrições e exames em um único ambiente.

Além da gestão de dados, o sistema incorpora uma interface interativa que atua como intermediária entre o médico e a base de dados, facilitando o acesso às informações e tornando o uso do prontuário mais eficiente no contexto da consulta.

O projeto se insere no contexto da transformação digital na saúde, buscando melhorar a qualidade do atendimento por meio do uso estruturado e inteligente dos dados clínicos.

# 2) Descrição da funcionalidade que mais entrega valor

A principal funcionalidade do sistema é a geração automática de um resumo clínico estruturado do paciente (briefing), a partir do seu histórico armazenado.

Ao acessar um paciente, o sistema consolida todas as informações relevantes registradas ao longo das consultas, como sintomas recorrentes, diagnósticos anteriores, prescrições realizadas e resultados de exames, apresentando esses dados de forma organizada e objetiva para o médico.

Essa funcionalidade reduz significativamente o tempo gasto na busca por informações, elimina a dependência da memória do profissional e garante que decisões clínicas sejam tomadas com base em um histórico completo e confiável.

Além disso, o sistema permite identificar padrões no histórico do paciente, como recorrência de sintomas ou possíveis indícios de condições crônicas, oferecendo sugestões que auxiliam na análise do caso.

O valor dessa funcionalidade se torna ainda mais evidente em contextos com alta rotatividade de profissionais, onde o acesso rápido e estruturado ao histórico do paciente é essencial para garantir a continuidade e a qualidade do atendimento.

# Importante: O sistema não substitui o diagnóstico médico, atuando exclusivamente como ferramenta de apoio baseada em dados históricos.


# Diagrama Modelo Relacional

<img width="7061" height="5263" alt="Image" src="https://github.com/user-attachments/assets/4e8ad776-d77e-4c49-9aed-0155cd8c33be" />

# Modelagem Baseada em Agregação

## Visão Geral

A modelagem do sistema foi construída com base no conceito de agregação, utilizado em bancos de dados NoSQL, onde os dados são organizados em conjuntos que fazem sentido serem acessados juntos.
Diferente do modelo relacional, que separa bastante as informações para evitar redundância, aqui a ideia foi justamente o contrário: agrupar os dados pensando em como o sistema vai ser usado na prática.
No caso desse sistema, o principal uso acontece durante a consulta médica, quando o profissional precisa acessar rapidamente o histórico do paciente. Por isso, a modelagem foi pensada priorizando leitura rápida e acesso direto às informações mais relevantes.


## Agregação Principal

A agregação principal definida foi o paciente.
Nesse contexto, o paciente atua como o aggregate root do sistema, sendo responsável por concentrar todas as informações relacionadas ao seu histórico clínico.
Ele funciona como o ponto central do sistema, reunindo tanto os dados cadastrais quanto todo o histórico clínico. Essa escolha faz sentido porque, na prática, o fluxo sempre começa pelo paciente, e a partir dele o médico precisa entender todo o contexto.


## Consultas como Sub-agregação

Dentro do paciente, as consultas foram organizadas como uma sub-agregação.
As consultas funcionam como uma sub-agregação dentro do paciente, representando os eventos clínicos que compõem o seu histórico.
Cada consulta representa um momento específico de atendimento e reúne todas as informações relacionadas àquele evento. Isso permite acompanhar a evolução do paciente ao longo do tempo de forma mais natural e organizada.


## Informações dentro da Consulta

Dentro de cada consulta, foram agrupados os dados que só fazem sentido naquele contexto específico.
Sintomas
Os sintomas representam o que o paciente relatou naquele momento. Eles foram colocados dentro da consulta porque não fazem sentido isoladamente, sem o contexto do atendimento.


## Diagnósticos
Os diagnósticos seguem a mesma lógica. Eles estão diretamente ligados à análise feita naquela consulta, então faz mais sentido mantê-los junto desse registro.


## Prescrições

As prescrições representam o que foi indicado como tratamento. Como dependem da consulta em que foram definidas, também foram incluídas dentro desse mesmo agrupamento.


## Exames

Os exames armazenam tanto informações quanto resultados relacionados ao atendimento. Ao mantê-los dentro da consulta, fica mais fácil analisar o caso de forma completa, sem precisar buscar dados em diferentes lugares.


## Médico associado à consulta
O médico foi relacionado à consulta para garantir que seja possível identificar quem realizou cada atendimento.
Isso é importante tanto para organização quanto para possíveis análises futuras.


## Justificativa da Modelagem

A principal decisão da modelagem foi organizar os dados pensando no uso real do sistema.
Como o objetivo é acessar rapidamente o histórico completo do paciente durante a consulta, faz sentido manter essas informações agrupadas. Isso evita múltiplas buscas no banco e torna o sistema mais eficiente.

Além disso, essa estrutura se aproxima mais da forma como o próprio médico pensa o atendimento: paciente → histórico → consulta → análise.

