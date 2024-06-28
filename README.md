# Projeto-Monitoramento-Aprendizado
Este foi um projeto realizado para a empresa [Comunidade DS](https://www.comunidadeds.com/), por meio de um vínculo por uma empresa Jr.
Ele foi elaborado inicialmente por uma equipe de 3 cientistas de dados e em alguns momentos também houve o contato com stakeholders do projeto e o analista de dados da empresa para conseguir acesso aos dados e também conseguir executar o projeto na nuvem da empresa.

Como o projeto contém alguns dados sigilosos da empresa, o projeto deste portfólio utiliza uma tabela fictícia para poder disponibilizar o painel criado para visualização pública.
Segue o link do painel: Ele possui acesso de segurança, você pode acessa-lo utilizando como usuário: e senha:

O projeto do início ao fim, foi feito com uma colaboração entre os cientistas da dados Michele Lopes e Daniel Salvatori

# 1. Problema de Negócio

A escola Comunidade DS utiliza a plataforma da [Cademi](https://cademi.com.br/), para disponibilizar os cursos para os alunos. 
Hoje o coordenador de ensino não consegue visualizar o progresso dos alunos ao longo das disciplinas, ainda existem tutores que acompanham o progresso dos alunos novos, para garantir engajamento e evitar cancelamentos de assinatura, mas isso ocorre de forma manual, consultando um por um o progresso dentro da plataforma.

Desta forma a principal a principal dor é poder visualizar o progresso dos alunos em uma frequência semanal, para facilitar a agilidade da equipe de tutores que garante o engajamento e gerar Insights para as reuniões de acompanhamento de métricas.
Os alunos são dividido em turmas, onde todo mês abre uma turma nova para acompanhamento e existem alguns parâmetros de avanço esperado, o que serve como guia para o tutor entender se o aluno está com o progresso previsto. Além da entrada de alunos novos mensalmente, que precisam ser inclusos nesse acompanhamento, eventualmente os alunos trocam de turma, ou acabam desistindo do curso e essas turmas precisam ser atualizadas.

A escola deseja um painel que deve ser atualizado semanalmente e o histórico deve ser mantido, mostrando o progresso dos alunos. No final do mês deseja-se poder analisar o histórico e entender como é o progresso dos alunos.


# 2. Descrição dos dados
Hoje a Cademi disponibiliza uma API onde é possível ter acesso as informações necessárias para execução do projeto.
Foi coletado via API duas estruturas de dados:

-Listar Alunos por Tag - Retorna uma lista de usuários à partir da ID de uma determinada TAG.
Essa coleta permite ter acesso as turmas o qual é necessário realizar o acompanhamento do progresso semanal

-Listar Progresso por Aluno e Produto - Retorna o progresso de um usuário em um determinado curso.
Essa coleta permiti extrair a informação de progresso necessária para o painel de acompanhamento do progresso

Ao extrair a API os dados são entregues na seguinte estrutura:


# 3. Estratégia de solução

# 4. Estrutura do ETL
 Montar uma figura com o esquema do ETL
 
# 5. Solução final
Explicar sobre o streamlit e suas páginas

# 6. Resultados obtidos
Processo rodando de forma automática e independente de um profissional que entenda de código para subir eventuais atualizações
Se a pessoa cancelar deixa de pagar o ticket médio - entender valores se possíveis 
Tempo de cada tutor  - Pegar insights e depoimento com os tutores
Tempo de cada funcionário  - Pegar insights e depoimento com Meigarom e Nayara

# 7. Conclusões finais

# 8. Próximos passos


# Sobre o repositório

# 1. Estrutura das pastas

# 2. Documentaçao e referência para consultas
[Documentação API Cademi](https://ajuda.cademi.com.br/configuracoes/api/usuario)

[Documentação Streamlit](https://docs.streamlit.io/)
