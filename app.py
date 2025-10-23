from flask import Flask, render_template, request, redirect, url_for, flash
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# In-memory "database" with unique IDs
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['task'].strip()
    if task_content:
        task_id = str(uuid.uuid4())
        tasks.append({
            'id': task_id,
            'content': task_content,
            'completed': False
        })
        flash('Task added successfully!', 'success')
    else:
        flash('Please enter a task!', 'error')
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle/<task_id>')
def toggle_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            if task['completed']:
                flash('Task completed!', 'success')
            else:
                flash('Task marked as not completed.', 'success') # For the 'Undo' button
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)