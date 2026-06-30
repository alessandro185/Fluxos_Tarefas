import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, datetime

# ─── CONFIG ──────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="TaskFlow",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0d0d0f;
    color: #e8e6e1;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111114 !important;
    border-right: 1px solid #222228;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif;
    color: #e8e6e1;
}

/* ── Titles ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800;
    letter-spacing: -0.03em;
}

h1 { font-size: 2.4rem !important; }
h2 { font-size: 1.5rem !important; color: #a09f9a !important; }

/* ── Inputs ── */
input, textarea, [data-baseweb="select"] {
    background: #1a1a1f !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 8px !important;
    color: #e8e6e1 !important;
}

input:focus, textarea:focus {
    border-color: #5b5bf6 !important;
    box-shadow: 0 0 0 3px rgba(91, 91, 246, 0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    background: #5b5bf6;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.3rem;
    transition: all 0.2s ease;
    width: 100%;
}

.stButton > button:hover {
    background: #4444e0;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(91, 91, 246, 0.35);
}

.stButton > button[kind="secondary"] {
    background: transparent;
    border: 1px solid #2a2a32 !important;
    color: #a09f9a;
}

.stButton > button[kind="secondary"]:hover {
    border-color: #e05c5c !important;
    color: #e05c5c;
    box-shadow: 0 4px 12px rgba(224, 92, 92, 0.2);
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #111114;
    border: 1px solid #222228;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
}

[data-testid="stMetricLabel"] {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b6a65 !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem !important;
    font-weight: 800;
    color: #e8e6e1 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #222228;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Badges (status) ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}
.badge-pendente   { background: #2a1f0e; color: #f0a030; border: 1px solid #3d2e12; }
.badge-progresso  { background: #0e1e2a; color: #30a0f0; border: 1px solid #122030; }
.badge-concluido  { background: #0e2a14; color: #30d060; border: 1px solid #124018; }

/* ── Task cards ── */
.task-card {
    background: #111114;
    border: 1px solid #222228;
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.2s ease;
}
.task-card:hover { border-color: #5b5bf6; }
.task-name { font-weight: 500; font-size: 0.95rem; }
.task-date { font-size: 0.78rem; color: #6b6a65; margin-top: 3px; }

/* ── Divider ── */
hr { border-color: #222228; }

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: #1a1a1f !important;
    border-color: #2a2a32 !important;
}

/* ── Priority tag ── */
.priority-alta   { color: #e05c5c; font-size: 0.72rem; font-weight: 700; }
.priority-media  { color: #f0a030; font-size: 0.72rem; font-weight: 700; }
.priority-baixa  { color: #6b6a65; font-size: 0.72rem; font-weight: 700; }

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: baseline;
    gap: 0.8rem;
    margin-bottom: 0.2rem;
}
.page-header span {
    font-size: 0.85rem;
    color: #6b6a65;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d0d0f; }
::-webkit-scrollbar-thumb { background: #2a2a32; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─── DATABASE ────────────────────────────────────────────────────────────────

DB = "tasks.db"

def get_conn():
    return sqlite3.connect(DB)

def init_db():
    with get_conn() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT    NOT NULL,
                status    TEXT    NOT NULL DEFAULT 'Pendente',
                priority  TEXT    NOT NULL DEFAULT 'Média',
                category  TEXT             DEFAULT '',
                due_date  TEXT,
                notes     TEXT             DEFAULT '',
                created_at TEXT   DEFAULT (datetime('now'))
            )
        ''')
        # migrate: add columns if missing (for existing DBs)
        for col, definition in [
            ("priority",   "TEXT NOT NULL DEFAULT 'Média'"),
            ("category",   "TEXT DEFAULT ''"),
            ("notes",      "TEXT DEFAULT ''"),
            ("created_at", "TEXT DEFAULT (datetime('now'))"),
        ]:
            try:
                conn.execute(f"ALTER TABLE tasks ADD COLUMN {col} {definition}")
            except Exception:
                pass

@st.cache_data(ttl=0)
def get_tasks() -> pd.DataFrame:
    with get_conn() as conn:
        df = pd.read_sql_query(
            "SELECT id, task_name, status, priority, category, due_date, notes, created_at FROM tasks ORDER BY id DESC",
            conn
        )
    return df

def add_task(name: str, status: str, priority: str, category: str, due_date: str, notes: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO tasks (task_name, status, priority, category, due_date, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (name, status, priority, category, due_date, notes)
        )
    get_tasks.clear()

def delete_task(task_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    get_tasks.clear()

def update_task(task_id: int, status: str, priority: str, notes: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET status = ?, priority = ?, notes = ? WHERE id = ?",
            (status, priority, notes, task_id)
        )
    get_tasks.clear()

# ─── HELPERS ─────────────────────────────────────────────────────────────────

STATUSES    = ["Pendente", "Em Progresso", "Concluído"]
PRIORITIES  = ["Alta", "Média", "Baixa"]
CATEGORIES  = ["", "Trabalho", "Pessoal", "Estudos", "Saúde", "Financeiro", "Outro"]

STATUS_EMOJI    = {"Pendente": "⏳", "Em Progresso": "🔄", "Concluído": "✅"}
PRIORITY_COLOR  = {"Alta": "priority-alta", "Média": "priority-media", "Baixa": "priority-baixa"}
STATUS_CLASS    = {"Pendente": "badge-pendente", "Em Progresso": "badge-progresso", "Concluído": "badge-concluido"}

def badge(text: str, css_class: str) -> str:
    return f'<span class="badge {css_class}">{text}</span>'

def days_until(due_date_str: str) -> str:
    if not due_date_str:
        return ""
    try:
        d = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        diff = (d - date.today()).days
        if diff < 0:
            return f"🔴 {abs(diff)}d atrasado"
        if diff == 0:
            return "🟡 Vence hoje"
        return f"🟢 {diff}d restantes"
    except Exception:
        return ""

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚡ TaskFlow")
        st.markdown("---")
        st.markdown("### Adicionar Tarefa")

        task_name = st.text_input("Nome", placeholder="Ex: Revisar relatório")
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox("Status", STATUSES)
        with col2:
            priority = st.selectbox("Prioridade", PRIORITIES)

        category = st.selectbox("Categoria", CATEGORIES)
        due_date = st.date_input("Data de Entrega", min_value=date.today())
        notes    = st.text_area("Notas", placeholder="Observações opcionais...", height=80)

        if st.button("💾 Salvar Tarefa"):
            if task_name.strip():
                add_task(task_name.strip(), status, priority, category, str(due_date), notes)
                st.success("Tarefa adicionada!")
                st.rerun()
            else:
                st.error("Digite um nome para a tarefa.")

        st.markdown("---")
        st.markdown("### Filtros")
        filter_status   = st.multiselect("Status", STATUSES, default=STATUSES)
        filter_priority = st.multiselect("Prioridade", PRIORITIES, default=PRIORITIES)
        search_term     = st.text_input("🔍 Buscar", placeholder="Nome ou categoria...")

    return filter_status, filter_priority, search_term

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    init_db()

    filter_status, filter_priority, search_term = render_sidebar()

    # Header
    st.markdown("""
        <div class="page-header">
            <h1>Minhas Tarefas</h1>
            <span>TASKFLOW</span>
        </div>
    """, unsafe_allow_html=True)

    df = get_tasks()

    # ── Metrics ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total",        len(df))
    c2.metric("⏳ Pendentes",  len(df[df["status"] == "Pendente"]))
    c3.metric("🔄 Em Progresso", len(df[df["status"] == "Em Progresso"]))
    c4.metric("✅ Concluídas", len(df[df["status"] == "Concluído"]))

    st.markdown("---")

    if df.empty:
        st.info("📭 Nenhuma tarefa ainda. Use o menu lateral para adicionar!")
        return

    # ── Filters ──────────────────────────────────────────────────────────────
    df_view = df.copy()
    if filter_status:
        df_view = df_view[df_view["status"].isin(filter_status)]
    if filter_priority:
        df_view = df_view[df_view["priority"].isin(filter_priority)]
    if search_term:
        mask = (
            df_view["task_name"].str.contains(search_term, case=False, na=False) |
            df_view["category"].str.contains(search_term, case=False, na=False)
        )
        df_view = df_view[mask]

    # ── Task List ─────────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📋 Lista de Tarefas", "📊 Análise"])

    with tab1:
        if df_view.empty:
            st.warning("Nenhuma tarefa corresponde aos filtros selecionados.")
        else:
            for _, row in df_view.iterrows():
                with st.container():
                    col_info, col_actions = st.columns([5, 1])
                    with col_info:
                        status_badge   = badge(f"{STATUS_EMOJI.get(row['status'], '')} {row['status']}", STATUS_CLASS.get(row['status'], ''))
                        priority_class = PRIORITY_COLOR.get(row['priority'], '')
                        cat_text       = f" · {row['category']}" if row['category'] else ""
                        deadline_text  = days_until(row['due_date'])
                        deadline_disp  = f" · {deadline_text}" if deadline_text else ""

                        st.markdown(f"""
                        <div class="task-card">
                            <div>
                                <div class="task-name">{row['task_name']}</div>
                                <div class="task-date">
                                    <span class="{priority_class}">▲ {row['priority']}</span>
                                    {cat_text}{deadline_disp}
                                </div>
                            </div>
                            <div>{status_badge}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_actions:
                        with st.expander("✏️"):
                            new_status   = st.selectbox("Status",    STATUSES,   index=STATUSES.index(row['status']),   key=f"s_{row['id']}")
                            new_priority = st.selectbox("Prioridade", PRIORITIES, index=PRIORITIES.index(row['priority']), key=f"p_{row['id']}")
                            new_notes    = st.text_area("Notas", value=row['notes'] or "", key=f"n_{row['id']}", height=60)
                            if st.button("Salvar", key=f"upd_{row['id']}"):
                                update_task(row['id'], new_status, new_priority, new_notes)
                                st.success("Atualizado!")
                                st.rerun()
                            if st.button("🗑️ Deletar", key=f"del_{row['id']}"):
                                delete_task(row['id'])
                                st.rerun()

    with tab2:
        if df.empty:
            st.info("Sem dados para analisar.")
        else:
            col_a, col_b = st.columns(2)

            with col_a:
                st.subheader("Por Status")
                status_data = df["status"].value_counts().rename_axis("Status").reset_index(name="Qtd")
                st.bar_chart(status_data.set_index("Status"))

            with col_b:
                st.subheader("Por Prioridade")
                prio_data = df["priority"].value_counts().rename_axis("Prioridade").reset_index(name="Qtd")
                st.bar_chart(prio_data.set_index("Prioridade"))

            st.subheader("Por Categoria")
            cat_data = df[df["category"] != ""]["category"].value_counts().rename_axis("Categoria").reset_index(name="Qtd")
            if not cat_data.empty:
                st.bar_chart(cat_data.set_index("Categoria"))
            else:
                st.info("Nenhuma categoria atribuída ainda.")

            # Overdue count
            overdue = 0
            for _, row in df[df["status"] != "Concluído"].iterrows():
                if row["due_date"]:
                    try:
                        d = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
                        if d < date.today():
                            overdue += 1
                    except Exception:
                        pass
            if overdue:
                st.error(f"⚠️ {overdue} tarefa(s) com prazo vencido!")
            else:
                st.success("✅ Nenhuma tarefa atrasada!")


if __name__ == "__main__":
    main()