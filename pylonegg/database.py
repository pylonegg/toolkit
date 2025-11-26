import pyodbc
from pylonegg.config import load_config
from datetime import datetime

# Connection string
config      = load_config()
DATABASE    = config["db_database"]
SERVER      = config["db_server"]


CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)




def init_db():
    """
    Initialize SQL Server database with tables:
    - tasks
    - approvals
    - ai_suggestions
    """
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        print("[INFO] Connected to SQL Server successfully.")

        # Tasks table
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tasks' AND xtype='U')
        CREATE TABLE tasks (
            id NVARCHAR(255) PRIMARY KEY,
            source NVARCHAR(100),
            title NVARCHAR(255),
            description NVARCHAR(MAX),
            object_ref NVARCHAR(255),
            url NVARCHAR(255),
            created_at DATETIME
        )
        """)

        # Approvals table
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='approvals' AND xtype='U')
        CREATE TABLE approvals (
            task_id NVARCHAR(255) PRIMARY KEY,
            status NVARCHAR(50),
            edited_text NVARCHAR(MAX),
            approved_at DATETIME
        )
        """)

        # AI Suggestions table
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ai_suggestions' AND xtype='U')
        CREATE TABLE ai_suggestions (
            task_id NVARCHAR(255) PRIMARY KEY,
            suggestion NVARCHAR(MAX),
            created_at DATETIME
        )
        """)

        conn.commit()
        print("[INFO] Tables created/verified successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
    finally:
        conn.close()



# -----------------------------
# Database Utility Functions
# -----------------------------

def save_task(task):
    """Insert a new task into the tasks table, ignore if it exists."""
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM tasks WHERE id = ?)
            INSERT INTO tasks (id, source, title, description, object_ref, url, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            task["id"],
            task["id"],
            task.get("source"),
            task.get("title"),
            task.get("description"),
            str(task.get("object_ref")),
            task.get("url",""),
            datetime.now()
        ))
        conn.commit()
        print(f"[INFO] Task {task['id']} saved successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to save task {task['id']}: {e}")
    finally:
        conn.close()


def save_ai_suggestion(task_id, suggestion):
    """Insert or update AI suggestion for a task."""
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("""
            IF EXISTS (SELECT 1 FROM ai_suggestions WHERE task_id = ?)
                UPDATE ai_suggestions
                SET suggestion = ?, created_at = ?
                WHERE task_id = ?
            ELSE
                INSERT INTO ai_suggestions (task_id, suggestion, created_at)
                VALUES (?, ?, ?)
        """, (
            task_id, suggestion, datetime.now(), task_id,
            task_id, suggestion, datetime.now()
        ))
        conn.commit()
        print(f"[INFO] AI suggestion saved for task {task_id}.")
    except Exception as e:
        print(f"[ERROR] Failed to save AI suggestion for task {task_id}: {e}")
    finally:
        conn.close()


def save_approval(task_id, status, edited_text=None):
    """Insert or update approval for a task."""
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("""
            IF EXISTS (SELECT 1 FROM approvals WHERE task_id = ?)
                UPDATE approvals
                SET status = ?, edited_text = ?, approved_at = ?
                WHERE task_id = ?
            ELSE
                INSERT INTO approvals (task_id, status, edited_text, approved_at)
                VALUES (?, ?, ?, ?)
        """, (
            task_id, status, edited_text, datetime.now(), task_id,
            task_id, status, edited_text, datetime.now()
        ))
        conn.commit()
        print(f"[INFO] Approval saved for task {task_id}.")
    except Exception as e:
        print(f"[ERROR] Failed to save approval for task {task_id}: {e}")
    finally:
        conn.close()


def get_unprocessed_tasks():
    """Retrieve tasks that have not yet been approved."""
    tasks = []
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.source, t.title, t.description, t.object_ref, t.url
            FROM tasks t
            LEFT JOIN approvals a ON t.id = a.task_id
            WHERE a.status IS NULL
        """)
        rows = cursor.fetchall()
        for row in rows:
            tasks.append({
                "id": row[0],
                "source": row[1],
                "title": row[2],
                "description": row[3],
                "object_ref": row[4],
                "url": row[5]
            })
        print(f"[INFO] Retrieved {len(tasks)} unprocessed tasks.")
    except Exception as e:
        print(f"[ERROR] Failed to fetch unprocessed tasks: {e}")
    finally:
        conn.close()
    return tasks
