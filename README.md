# TaskFlow

Gerenciador de tarefas feito com Streamlit, Pandas e SQLite.

## Funcionalidades

- Cadastro de tarefas com nome, status, prioridade, categoria, prazo e notas.
- Filtros por status, prioridade e busca por texto.
- Edicao de status, prioridade e notas.
- Exclusao de tarefas.
- Indicadores de total, pendentes, em progresso e concluidas.
- Graficos de analise por status, prioridade e categoria.
- Banco local SQLite em `tasks.db`.

## Requisitos

- Python 3.10 ou superior
- Streamlit
- Pandas

## Instalacao

Instale as dependencias com:

```bash
pip install streamlit pandas
```

## Como executar

Na pasta do projeto, rode:

```bash
streamlit run app.py
```

Depois acesse no navegador:

```text
http://localhost:8501
```

Se a porta `8501` ja estiver em uso, execute em outra porta:

```bash
streamlit run app.py --server.port 8502
```

## Estrutura

```text
.
+-- app.py      # Aplicacao principal em Streamlit
+-- tasks.db    # Banco de dados SQLite local
+-- README.md   # Documentacao do projeto
```

## Observacao

O arquivo `tasks.db` guarda as tarefas localmente. Se ele for removido, o app cria a estrutura novamente ao iniciar, mas os dados anteriores serao perdidos.
