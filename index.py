from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
tasks = []

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>To-Do List App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 300px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
            }
            .task-input {
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }
            .task-input input {
                flex: 1;
                padding: 5px;
                margin-right: 5px;
            }
            .task-input button {
                padding: 5px 10px;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            ul li {
                padding: 10px;
                background-color: #f4f4f4;
                margin-bottom: 5px;
                cursor: pointer;
            }
            .buttons {
                display: flex;
                justify-content: space-between;
            }
            .buttons button {
                padding: 5px;
            }
        </style>
    </head>
    <body>

    <div class="container">
        <h1>To-Do List App</h1>
        <div class="task-input">
            <input type="text" id="task" placeholder="Enter task...">
            <button onclick="addTask()">Add Task</button>
        </div>
        <ul id="task-list"></ul>
        <div class="buttons">
            <button onclick="removeTask()">Remove Task</button>
            <button onclick="editTask()">Edit Task</button>
            <button onclick="saveTasks()">Save Tasks</button>
            <button onclick="loadTasks()">Load Tasks</button>
        </div>
    </div>

    <script>
        let taskList = [];

        document.addEventListener("DOMContentLoaded", () => {
            loadTasks();
        });

        function addTask() {
            const taskInput = document.getElementById('task');
            const task = taskInput.value.trim();
            if (task) {
                taskList.push(task);
                taskInput.value = '';
                renderTasks();
            }
        }

        function removeTask() {
            const taskInput = document.getElementById('task');
            const task = taskInput.value.trim();
            if (task) {
                taskList = taskList.filter(t => t !== task);
                taskInput.value = '';
                renderTasks();
            }
        }

        function editTask() {
            const taskInput = document.getElementById('task');
            const task = taskInput.value.trim();
            if (task) {
                const newTask = prompt('Edit task:', task);
                if (newTask) {
                    const taskIndex = taskList.indexOf(task);
                    if (taskIndex > -1) {
                        taskList[taskIndex] = newTask.trim();
                        renderTasks();
                    }
                }
            }
        }

        function saveTasks() {
            fetch('/save_tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ tasks: taskList }),
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        }

        function loadTasks() {
            fetch('/load_tasks')
                .then(response => response.json())
                .then(data => {
                    taskList = data.tasks;
                    renderTasks();
                })
                .catch(error => console.error('Error:', error));
        }

        function renderTasks() {
            const taskListElement = document.getElementById('task-list');
            taskListElement.innerHTML = '';
            taskList.forEach(task => {
                const li = document.createElement('li');
                li.textContent = task;
                li.onclick = () => document.getElementById('task').value = task;
                taskListElement.appendChild(li);
            });
        }
    </script>
    </body>
    </html>
    ''')

@app.route('/save_tasks', methods=['POST'])
def save_tasks():
    global tasks
    data = request.get_json()
    tasks = data.get('tasks', [])
    return jsonify({'message': 'Tasks saved successfully!'})

@app.route('/load_tasks', methods=['GET'])
def load_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
