# TaskFlow ⚡

Gerenciador de tarefas moderno, seguro e multiusuário construído com **Streamlit**, **Pandas** e suporte híbrido a banco de dados (**Neon PostgreSQL** na nuvem e **SQLite** local).

---

## 🚀 Funcionalidades

- **Autenticação Segura:** Sistema de cadastro e login de usuários com senhas criptografadas via `scrypt` e proteção contra timing attacks.
- **Isolamento Multiusuário:** Cada usuário autenticado visualiza, cadastra, edita e remove apenas as suas próprias tarefas.
- **Banco de Dados Híbrido:**
  - **Nuvem (Produção):** Conexão permanente com **PostgreSQL no Neon**, garantindo que seus dados nunca se percam.
  - **Local (Desenvolvimento):** Fallback automático para SQLite local (`tasks.db`).
- **Gestão Completa de Tarefas:** Cadastro com nome, status, prioridade, categoria, prazo e notas.
- **Dashboard Analítico:** Indicadores de total, tarefas pendentes, em progresso e concluídas, além de gráficos interativos por status, prioridade e categoria.
- **Segurança Hardened:** Proteção contra Stored XSS com sanitização HTML, prevenção a ReDoS e integridade referencial com modo WAL no SQLite.

---

## 🛠️ Requisitos

- Python 3.10 ou superior
- Dependências listadas em `requirements.txt`:
  - `streamlit`
  - `pandas`
  - `psycopg2-binary`

---

## 📦 Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/alessandro185/Fluxos_Tarefas.git
   cd Fluxos_Tarefas
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

4. Acesse no navegador:
   ```text
   http://localhost:8501
   ```

---

## ☁️ Deploy no Streamlit Community Cloud

1. Conecte o repositório `alessandro185/Fluxos_Tarefas` no [Streamlit Community Cloud](https://share.streamlit.io/).
2. Nas configurações do App (**Settings > Secrets**), configure a variável de conexão com o banco Neon:
   ```toml
   DATABASE_URL = "postgresql://usuario:senha@ep-exemplo.neon.tech/neondb?sslmode=require"
   ```
3. O deploy é atualizado automaticamente a cada novo commit no GitHub.

---

## 📂 Estrutura do Projeto

```text
.
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação completa
├── tasks.db            # Banco SQLite local (fallback)
└── .gitignore          # Proteção de credenciais e caches
```
