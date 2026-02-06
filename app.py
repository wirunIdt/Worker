from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Data file path
DATA_FILE = 'tasks.json'
USERS_FILE = 'users.json'

# Initialize data files
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'admin': 'admin123'}, f, ensure_ascii=False)

# Helper functions
def read_tasks():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def write_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def read_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'admin': 'admin123'}

def write_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Decorator for admin-only routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes

@app.route('/')
def index():
    """Public order form page"""
    return render_template('order_form.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    """Handle public order submission"""
    tasks = read_tasks()
    
    new_task = {
        'id': str(int(datetime.now().timestamp() * 1000)),
        'customer': {
            'name': request.form.get('customer_name', ''),
            'phone': request.form.get('customer_phone', ''),
            'email': request.form.get('customer_email', '')
        },
        'title': request.form.get('task_title', ''),
        'description': request.form.get('task_description', ''),
        'priority': request.form.get('priority', 'medium'),
        'deadline': request.form.get('deadline', ''),
        'status': 'pending',
        'createdBy': 'ลูกค้า',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    
    tasks.insert(0, new_task)
    write_tasks(tasks)
    
    return render_template('order_form.html', success=True)

@app.route('/tracking')
def tracking():
    """Public order tracking page"""
    return render_template('tracking.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle order search"""
    tasks = read_tasks()
    search_name = request.form.get('search_name', '').lower()
    search_date = request.form.get('search_date', '')
    
    results = tasks
    
    if search_name:
        results = [task for task in results 
                   if search_name in task['customer']['name'].lower()]
    
    if search_date:
        results = [task for task in results 
                   if task.get('deadline', '').startswith(search_date)]
    
    return render_template('tracking.html', results=results, 
                           searched=True, search_name=search_name, 
                           search_date=search_date)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    users = read_users()
    first_time = len(users) == 0
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if first_time:
            # Create first admin account
            users[username] = password
            write_users(users)
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            # Normal login
            if username in users and users[username] == password:
                session['username'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('login.html', error='ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', first_time=first_time)
    
    return render_template('login.html', first_time=first_time)

@app.route('/logout')
def logout():
    """Logout"""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard page"""
    tasks = read_tasks()
    username = session.get('username', '')
    
    # Calculate statistics
    stats = {
        'total': len(tasks),
        'pending': len([t for t in tasks if t['status'] == 'pending']),
        'inprogress': len([t for t in tasks if t['status'] == 'inprogress']),
        'completed': len([t for t in tasks if t['status'] == 'completed'])
    }
    
    return render_template('admin_dashboard.html', tasks=tasks, stats=stats, username=username)

@app.route('/admin/update_status', methods=['POST'])
@admin_required
def update_status():
    """Update task status"""
    task_id = request.form.get('task_id')
    tasks = read_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            statuses = ['pending', 'inprogress', 'completed', 'cancelled']
            current_index = statuses.index(task['status'])
            next_index = (current_index + 1) % len(statuses)
            
            task['status'] = statuses[next_index]
            task['updatedAt'] = datetime.now().isoformat()
            task['updatedBy'] = session.get('username', '')
            break
    
    write_tasks(tasks)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete', methods=['POST'])
@admin_required
def delete_task():
    """Delete task"""
    task_id = request.form.get('task_id')
    tasks = read_tasks()
    
    tasks = [task for task in tasks if task['id'] != task_id]
    write_tasks(tasks)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/filter/<status>')
@admin_required
def filter_tasks(status):
    """Filter tasks by status"""
    tasks = read_tasks()
    username = session.get('username', '')
    
    if status != 'all':
        tasks = [task for task in tasks if task['status'] == status]
    
    # Calculate statistics
    all_tasks = read_tasks()
    stats = {
        'total': len(all_tasks),
        'pending': len([t for t in all_tasks if t['status'] == 'pending']),
        'inprogress': len([t for t in all_tasks if t['status'] == 'inprogress']),
        'completed': len([t for t in all_tasks if t['status'] == 'completed'])
    }
    
    return render_template('admin_dashboard.html', tasks=tasks, stats=stats, 
                           username=username, current_filter=status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
