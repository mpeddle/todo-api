from flask import Flask, request, session, redirect, abort, \
     render_template, jsonify
from flask.views import MethodView

from todoapi.database import db_session
from todoapi.models import Todo

from jinja2 import Environment, PackageLoader

## SETTINGS
app = Flask(__name__)

jinja_env = Environment(loader=PackageLoader('todoapi', 'templates'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

## API

class TodoApi(MethodView):

    def get(self, todo_id):
        todo = Todo.query.filter(Todo.id==todo_id).all()
        return jsonify({'todos' : [t.api_dict() for t in todo]}) 

    def post(self):
        title, text = request.form.get('title',''), request.form.get('text','')
        if title == '':
            return jsonify({'error':'Todos require a title'})
        todo = Todo(title=title,text=text)
        db_session.add(todo)
        db_session.commit()
        return 'OK'

    def delete(self,todo_id):
        todo = Todo.query.filter(Todo.id==todo_id)
        if not todo:
            return jsonify({'error':'Todo not found'})
        todo.delete()
        db_session.commit()
        return jsonify({'result': True})

    def put(self, todo_id):
        title, text = request.form.get('title',''), request.form.get('text','')
        if 'title' =='':
            return jsonify({'error':'Todos require a title'})
        todo = Todo.query.filter(Todo.id==todo_id).first()
        if todo:
            todo.title = title
            todo.text = text
            db_session.add(todo)
            db_session.commit()
            return jsonify({'result': True})
        else:
            return jsonify({'error':'Todo not found'})
 
class Todos(MethodView):
    def get(self):
        todos = Todo.query.all()
        print todos
        return jsonify({'todos': [t.api_dict() for t in todos]})

## VIEWS

@app.route("/")
def index():
    todos = Todo.query.all()
    template = jinja_env.get_template('todo.html')
    return template.render(todos=todos)

app.add_url_rule('/todos', view_func=Todos.as_view('todos_view'), methods=['GET',])
app.add_url_rule('/todo', view_func=TodoApi.as_view('todo_view_put'), methods=['POST'])
app.add_url_rule('/todo/<int:todo_id>', view_func=TodoApi.as_view('todo_view'), methods=['GET','PUT','DELETE']) 

if __name__ == '__main__':
    app.run(debug=True)
