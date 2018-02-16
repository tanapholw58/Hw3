import pymongo, json, time
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

url = "mongodb://jamesza:12345@localhost:27017/admin"
client = pymongo.MongoClient(url)

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('information')

db = client.admin.cpe_company_limited

class Register(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		if set(("id", "firstname", "lastname", "password")) <= set(data):
			db.insert({"id":data['id'], "firstname":data['firstname'], "lastname":data['lastname'], "password":data['password']})
			return {"id":data['id'], "firstname":data['firstname'], "lastname":data['lastname'], "password":data['password']}
		else:
			return {"status":"need more argument id,firstname,lastname,password"}

class Sign(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		u = db.find_one({"id":data['id']})
		print data['password']
		if not u:
			return {"status":"Don't have this ID"}
		else:
			if u['password'] == data['password']:
				dtstamp = time.strftime("%Y-%m-%d %H:%M:%S")
				db.update_one({'id':data['id']},{ '$push':{'list_work':{'datetime':dtstamp}}},upsert=False)
				return {"status":"Login complete","datetime":dtstamp}
			else:
				return {"status":"password is wrong"}

class Record(Resource):
        def post(self):
                args = parser.parse_args()
                data = json.loads(args['information'])
		n = db.find_one({"id":data['id']})
		if not n:
                        return {'id':"no id"}
		else:
			if 'list_work' not in n:
                                return {'id':n['id'],'list_work':"no data"}
                        else:
                                return {'id':n['id'],'list_work':n['list_work']} 

api.add_resource(Register,'/api/regis')
api.add_resource(Sign,'/api/Sign')
api.add_resource(Record,'/api/Record')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5100)
