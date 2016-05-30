
from flask import *
import sqlite3
from flask import Flask, render_template, request


DATABASE = 'mojabaza.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'cookie'

@app.route('/')
def main():
    return render_template('index.html')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/tasks')
def tasks():
    g.db  = connect_db()
    cur = g.db.execute('select name, due_date, priority, task_id from mbaza where status=1')
    open_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()]
    cur = g.db.execute('select name, due_date, priority, task_id from mbaza where status=0')
    closed_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('tasks.html', open_tasks=open_tasks, closed_tasks=closed_tasks)

@app.route('/add', methods=['POST'])
def new_task():
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']
    if not name and not date and priority =='0':
        flash("You forgot the task name, date, and priority. Fill the missing fields.")
        return redirect(url_for('tasks'))
    elif not name and not date:
        flash("You forgot the task name and date. Fill the missing fields.")
        return redirect(url_for('tasks'))
    elif not date and priority=='0':
        flash("You forgot the task date and priority. Fill the missing fields.")
        return redirect(url_for('tasks'))
    elif not name and priority=='0':
        flash("You forgot the task name and priority. Fill the missing fields.")
        return redirect(url_for('tasks'))
    elif not name:
        flash("You forgot the task name. Fill the missing fields.")
        return redirect(url_for('tasks'))
    elif not date:
        flash("You forgot the task date. Fill the missing fields.")
        return redirect(url_for('tasks'))
    elif priority=='0':
        flash("You forgot the task priority. Fill the missing fields.")
        return redirect(url_for('tasks'))
    else:
        g.db.execute('insert into mbaza (name, due_date, priority, status) values (?, ?, ?, 1)',
             [request.form['name'], request.form['due_date'], request.form['priority']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>',)
def delete_entry(task_id):
    g.db  = connect_db()
    cur = g.db.execute('delete from mbaza where task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was deleted')
    return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>',)
def complete(task_id):
    g.db  = connect_db()
    cur = g.db.execute('update mbaza set status = 0 where task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was completed.')
    return redirect(url_for('tasks'))


@app.route('/taskss')
def taskss():
    return render_template('tasks.html')




if __name__ == "__main__":
    app.run(debug=True)