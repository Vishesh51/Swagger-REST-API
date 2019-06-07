from flask import Flask, request
from flask_restplus import Api, Resource, fields
from random import randint

flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "Phone Number Assignment", 
		  description = "Application for assigning new numbers to users")
name_space = app.namespace('phone', description='Manages Numbers')

model = app.model('Data Model', 
				  {'name': fields.String(required = True, 
    					  				 description="Name of the person", 
    					  				 help="Name cannot be blank."),
					'request-number (leave 0 for no special request)':fields.Integer(required= False,
										description="Number of the person",
										minimum=1111111111,
										maximum=9999999999,
										help="Please enter a valid number")
										})

number=randint(1111111111,9999999999)
list_of_names = {}
list_of_numbers={}

@name_space.route("/<int:id>")
class MainClass(Resource):

	@app.doc(responses={ 200: 'OK', 400: 'Incorrect URL request', 500: 'Internal Error' }, 
			 params={ 'id': 'Enter the id of the person'})
	def get(self, id):
		try:
			name = list_of_names[id]
			no=list_of_numbers[id]
			return {
				"status": "Number retrieved",
				"name" : list_of_names[id],
				"Number requested": list_of_numbers[id]
			}
		except KeyError as e:
			name_space.abort(500, e.__doc__, status = "Internal Error", statusCode = "500")
		except Exception as e:
			name_space.abort(400, e.__doc__, status = "Incorrect URL request", statusCode = "400")

	@app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Specify the Id associated with the person' })
	@app.expect(model)		
	def post(self, id):
		try:
			num=request.json['request-number (leave 0 for no special request)']
			list_of_names[id] = request.json['name']
			if num!=0 and (num<1111111111 or num>9999999999):
				return {
					"status": "Invalid Number"
					}
			if num!=0:
				if num not in list_of_numbers.values():
					list_of_numbers[id]=num
					return {
					"status": "New contact number assigned",
					"name": list_of_names[id],
					"request-number": list_of_numbers[id]
					}
				else:
					return {
					"status": "Number already taken"
					}
			while num==0:
				number=randint(1111111111,9999999999)
				if number in list_of_numbers:
					continue
				else:
					list_of_numbers[id]=number
					break
			return {
					"status": "New contact number assigned",
					"name": list_of_names[id],
					"request-number": list_of_numbers[id],
					
				}
		except KeyError as e:
			name_space.abort(500, e.__doc__, status = "Internal Error", statusCode = "500")
		except Exception as e:
			name_space.abort(400, e.__doc__, status = "Incorrect URL request", statusCode = "400")