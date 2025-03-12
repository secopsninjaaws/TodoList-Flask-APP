from flask import Flask, request, redirect, url_for, render_template_string
import json
import os

DATA_FILE = "tasks.json"
app = Flask(__name__)

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

HTML_TEMPLATE = """
<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <title>Todo List</title>
</head>
<body>
    <h1>Todo List</h1>
    <ul>
    {% for idx, task in enumerate(tasks, start=1) %}
        <li>
            {{ idx }}. {{ task['title'] }} - {{ 'Feito' if task.get('done', False) else 'Pendente' }}
            {% if not task.get('done', False) %}
            <a href="{{ url_for('mark_done', task_id=idx-1) }}">Marcar como feita</a>
            {% endif %}
            <a href="{{ url_for('delete_task', task_id=idx-1) }}">Remover</a>
        </li>
    {% endfor %}
    </ul>
    <h2>Adicionar Tarefa</h2>
    <form action="{{ url_for('add_task') }}" method="post">
        <input type="text" name="title" placeholder="Título da tarefa" required>
        <input type="submit" value="Adicionar">
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/done/<int:task_id>")
def mark_done(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)