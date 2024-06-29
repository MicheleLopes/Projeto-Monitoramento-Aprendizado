# Projeto-Monitoramento-Aprendizado
Este foi um projeto realizado para a empresa [Comunidade DS](https://www.comunidadeds.com/), por meio de um vínculo por uma empresa Jr.
Ele foi elaborado inicialmente por uma equipe de 3 cientistas de dados e em alguns momentos também houve o contato com stakeholders do projeto e o analista de dados da empresa para conseguir acesso aos dados e também conseguir executar o projeto na nuvem da empresa.

O projeto possui duas entregas principais:
1- Construção do ETL que faz toda extração dos dados e carga para o GCP;
2- Painel para interação com o usuário na plataforma Streamlit.

Como o projeto contém alguns dados sigilosos da empresa, o projeto deste portfólio utiliza uma tabela fictícia para poder disponibilizar o painel criado para visualização pública.
Segue o link do painel: Ele possui acesso de segurança, você pode acessa-lo utilizando as credenciais usuário: e senha:

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
Essa coleta permite ter acesso as turmas que precisamos realizar o acompanhamento do progresso semanal

-Listar Progresso por Aluno e Produto - Retorna o progresso de um usuário em um determinado curso.
Essa coleta permiti extrair a informação de progresso necessária para o painel de acompanhamento do progresso

Ao extrair a API os dados são entregues na seguinte estrutura:

**Listar alunos por Tag:**

-Chamada da API: GET /usuario/lista_por_tag/{tag_id}

Resposta:

"usuario":[
            {
                "id":1051,
                "nome":"Joana C",
                "email":"teste@oculto.com.br",
                "doc": "123.123.123-12",
                "celular":null,
                "login_auto":"http://membros.dvp/auth/login?crstk=",
                "gratis": false,
                "criado_em":"2020-01-12 19:59:20",
                "ultimo_acesso_em":null
            }
            
**Listar Progresso por Aluno e Produto**

-Chamada da API: GET /usuario/progresso_por_produto/{usuario_email_id_doc}/{produto_id}

Resposta:

"progresso":{
            "total":"41.7%",
            "assistidas":7,
            "completas":5
            }

# 3. Estratégia de solução

# 4. Estrutura do ETL
Para reesolver o problema, foi necessário criar um ETL para empresa, modelando como funcionaria a extração dos dados, transformações necessárias e como funcionaria o armazenamento do banco de dados.

O fluxograma abaixo representa a estrutura final do nosso projeto, desde a extração dos dados até a interação com o usuário final.

<img width="739" alt="image" src="https://github.com/MicheleLopes/Projeto-Monitoramento-Aprendizado/assets/123608349/3d6a0eb3-f9f3-4c96-86f7-360eaffab5f1">

Segue abaixo um descritivo de como funcionam as interações do ETL:

1Inicialmente é feito a extração dos dados da plataforma da Cademi por meio de uma API. Para isso como entrada é necessário informar tags das turmas, onde a API irá retornar uma lista de alunos e informações de contato.

Com essa informação é realizado uma segunda solicitação via API, onde como entrada é fornecido a lista de alunos que a Cademi retornou e em conjunto uma tabela com os produtos que gostaríamos de extrair o progresso.
Esses dados do progresso são armazenados dentro do nosso banco de dados a fim de armazenar o histórico do progresso.

Para interação com o usuário, foi criado um dashboard no streamlit, que consulta o banco de dados do GCP e trás uma visualização dos dados de progresso de uma forma interativa com filtros.

Além disso o streamlit também possui uma tela onde o coordenador de ensino pode inserir novas tags para entrarem nas próximas coletas de turmas da API. Para isso funcionar sem a necessidade de alterações internas, o próprio streamlit consegue alimentar a tabela de lista de turmas dentro do GCP.

O APP do streamlit é disponível para acesso de forma web, hospedado em Cloud por meio do GCP. Como essa aplicação é de uso interno da empresa, para acesso seguro, existe uma tela de login onde os usuários precisam informar as credenciais fornecidas pela empresa.

# 5. Solução final
Explicar sobre o streamlit e suas páginas
Como produto final para empresa foi elaborado um painel na plataforma do streamlit.
Esse painel possui inicialmente uma tela de login, que garante o acesso apenas para os colaboradores internos da empresa.
Além disso possui uma página para Inserir novas Tags para acompanhamento da trilha

# 6. Resultados obtidos
Processo rodando de forma automática e independente de um profissional que entenda de código para subir eventuais atualizações
Se a pessoa cancelar deixa de pagar o ticket médio - entender valores se possíveis 
Tempo de cada tutor  - Pegar insights e depoimento com os tutores
Tempo de cada funcionário  - Pegar insights e depoimento com Meigarom e Nayara

# 7. Conclusões finais
O maior desafio deste projeto foi estruturar do zero como seria esse ETL da empresa e conseguir automatiza-lo de forma que atualizações futuras não dependam de um analista de dados, conseguem ser feitas por um usuário da área de negócio apenas por meio de uma interação com a interface

# 8. Próximos passos


# Sobre o repositório

# 1. Estrutura das pastas

# 2. Documentaçao e referência para consultas
[Documentação API Cademi](https://ajuda.cademi.com.br/configuracoes/api/usuario)

[Documentação Streamlit](https://docs.streamlit.io/)
