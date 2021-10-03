import peewee
import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property
import flask
import datetime

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

werkzeug.cached_property = cached_property

from flask import Flask, request, jsonify
from peewee import *
from flask_marshmallow import Marshmallow
from flask_restplus import Api, fields, Resource

"""
Столкнулся с проблемой: cannot import name 'cached_property' from 'werkzeug'
Пришлось использовать костыль сверху
"""

app = Flask(__name__)
db = SqliteDatabase('data3.db')
ma = Marshmallow(app)
api = Api()
api.init_app(app)


# Таблицы

class BaseModel(Model):
    class Meta:
        database = db
        order_by = ('created_at',)

class Task(BaseModel):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=100)
    content = TextField(null=False)

    created_at = DateTimeField(default=datetime.datetime.now())

class UserSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content', 'created_at')

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('title', 'created_at')


model = api.model('Taskmodel', {
    'title': fields.String('Enter title'),
    'content': fields.String('Enter content')
})

task_schema = UserSchema()
tasks_schema = UsersSchema(many=True)

# Программа

@api.route('/api/task/get/<int:id>')
class getdata(Resource):
    def get(self, id):
        return jsonify(task_schema.dump(Task.get(id)))


@api.route('/api/task/post', methods=['POST', 'GET'])
class postdata(Resource):
    @api.expect(model)
    def post(self, request, *args, **kwargs):
        task_add = Task(title=request.json['title'], content=request.json['content'])
        task_add.save()
        return {'message': 'data added to database'}


@api.route('/api/task/put/<int:id>')
class putdata(Resource):
    @api.expect(model)
    def put(self, id):
        task_upd = Task.get(id)
        task_upd.title = request.json['title']
        task_upd.content = request.json['content']
        task_upd.save()
        return {'message': 'data updated'}


@api.route('/api/task/delete/<int:id>')
class deletedata(Resource):
    def delete(self, id):
        task_delete = Task.get(id)
        task_delete.delete_instance()
        task_delete.save()
        return {'message': 'data deleted successfully'}


@api.route('/api/task/get_all')
class getdata1(Resource):
    def get(self):
        return jsonify(tasks_schema.dump(Task.select()))


if __name__ == '__main__':
    try:
        db.connect()
        Task.create_table()
    except peewee.InternalError as px:
        print(str(px))
    app.run(debug=True)