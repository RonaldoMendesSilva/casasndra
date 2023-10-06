from cassandra.cluster import Cluster
import uuid

# Configuração do Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect()

# Criação do keyspace e da tabela
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS task_manager
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
""")

session.execute("""
    USE task_manager;
""")

session.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id UUID PRIMARY KEY,
        title TEXT,
        description TEXT
    );
""")

# Função para adicionar tarefa
def add_task(title, description):
    task_id = uuid.uuid1()
    session.execute("""
        INSERT INTO tasks (id, title, description) VALUES (%s, %s, %s);
    """, (task_id, title, description))

# Função para listar tarefas
def list_tasks():
    rows = session.execute("SELECT id, title FROM tasks")
    for row in rows:
        print(f"ID: {row.id}, Title: {row.title}")

# Função para visualizar descrição da tarefa
def view_task_description(task_id):
    row = session.execute("SELECT description FROM tasks WHERE id = %s", (task_id,)).one()
    if row:
        print(f"Description: {row.description}")
    else:
        print("Tarefa não encontrada.")

# Função para remover tarefa
def remove_task(task_id):
    session.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

# Exemplo de uso
task_id = uuid.uuid1()  # Defina task_id antes de usar nas funções
add_task("Fazer Compras", "Comprar itens essenciais para casa")
add_task("Estudar Python", "Dedicar 1 hora diariamente ao estudo de Python")
list_tasks()
view_task_description(task_id)  # Substitua task_id pelo ID da tarefa desejada
remove_task(task_id)  # Substitua task_id pelo ID da tarefa a ser removida
