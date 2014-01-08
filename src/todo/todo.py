from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sqlite3 import dbapi2 as sqlite3

from todo.database import db_session

## SETTINGS
app = Flask(__name__)
app.config.update({
    DATABASE='/tmp/todo.db',
    DEBUG=True,
    SECRET_KEY='ad75feSDau',
    USERNAME='admin',
    PASSWORD='default'
})
app.config.from_envvar('TODO_SETTINGS', silent=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

## API
@app.route('/todo/api/v1.0/todos', methods = ['GET'])
@auth.login_required
def get_todos():
    cur = g.db.execute('select id, title, text from todos order by id desc')
    todos = cur.fetchall()
    return jsonify({'todos' : todos})
 
@app.route('/todo/api/v1.0/todos/<int:todo_id>', methods = ['GET'])
@auth.login_required
def get_todo(todo_id):
    cur = g.db.execute('select id, title, text from todos where id ={}'.format(todo_id))
    todos = cur.fetchall()
    if len(todos) ==0:
        abort(404)
    return jsonify({'todos' : todos}) 
 
@app.route('/todo/api/v1.0/todos', methods = ['POST'])
@auth.login_required
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'id': todos[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    ## DB INSERT TODO HERE
    return jsonify( { 'todo': make_public_todo(todo) } ), 201
 
@app.route('/todo/api/v1.0/todos/<int:todo_id>', methods = ['PUT'])
@auth.login_required
def update_todo(todo_id):

    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    todo = filter(lambda t: t['id'] == todo_id, todos)
    if len(todo) == 0:
        abort(404)

    ## UPDATE TODO IN DB HERE

    todo[0]['title'] = request.json.get('title', todo[0]['title'])
    todo[0]['description'] = request.json.get('description', todo[0]['description'])
    todo[0]['done'] = request.json.get('done', todo[0]['done'])
    return jsonify( { 'todo': make_public_todo(todo[0]) } )
    
@app.route('/todo/api/v1.0/todos/<int:todo_id>', methods = ['DELETE'])
@auth.login_required
def delete_todo(todo_id):
    todo = filter(lambda t: t['id'] == todo_id, todos)
    if len(todo) == 0:
        abort(404)
    g.db.execute('delete from todos where id={}'.format(todo_id))
    return jsonify( { 'result': True } )

@app.route("/todos")
def show_todos():
    todos = Todo.get()
    return render_template('todos.html', todos=todos)

##VIEWS
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

if __name__ == '__main__':
    app.run()
