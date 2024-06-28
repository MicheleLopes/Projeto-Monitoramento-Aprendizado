# Projeto-Monitoramento-Aprendizado
Este foi um projeto realizado para a empresa [Comunidade DS](https://www.comunidadeds.com/), por meio de um vínculo por uma empresa Jr.
Ele foi elaborado por equipe de 3 cientistas de dados e em alguns momentos também houve o contato com stakeholders do projeto e o analista de dados da empresa para conseguir acesso aos dados e também conseguir executar o projeto na nuvem da empresa.

Como o projeto contém alguns dados sigilosos da empresa, o projeto deste portfólio utiliza uma tabela fictícia para poder disponibilizar o painel criado para visualização pública.
Segue o link do painel: Ele possui acesso de segurança, você pode acessa-lo utilizando como usuário: e senha:

O projeto do início ao fim, foi feito com uma colação entre a profissional Michele Lopes e Daniel Salvatori

# 1. Problema de Negócio

Hoje a escola Comunidade DS utiliza a plataforma da [Cademi](https://cademi.com.br/)
Como Coordenador de Ensino, eu gostaria de visualizar semanalmente o progresso de cada aluno, ao longo das disciplinas.

Os alunos devem ser agrupados por turmas, a partir da Turma 1 - Analista de Dados que começou em Novembro de 2023 até a turma 6 - Analista de Dados que começou em Abril de 2024.

O painel pode ser feito no Streamlit e sua estrutura pode ser vista abaixo.

Explicando o painel:
Colunas: Informações do Aluno + O nome das disciplinas na sequência que os alunos precisam terminar da Formação Profissional em Análise de Dados.

Por exemplo:
Nome | email | Telefone | LinkedIn | Portfólio de Projetos | SQL | Métricas de Negócio | Excel | ...

Linhas: Contém as informações do aluno + O progresso do aluno fornecido via API da Cademí.

Esse painel deve ser atualizado semanalmente e o histórico deve ser mantido. Em outras palavras, a cada mês, 4 fotos são tiradas da Cademí, mostrando o progresso dos alunos. No final do mês, podemos analisar o histórico ( as 4 fotos semanais ) e entender como é o progresso dos alunos.


# 2. Descrição dos dados

# 3. Estratégia de solução
