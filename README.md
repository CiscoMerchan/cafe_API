# API with RESTful Routing
In this program can be use to create a website that contain a list of Coffee Shop
in the city. It is posible to display : All the Cafe, Randomn Cafe, Serach Cafe by location, Add a new Cafe to the database, Update price of Coffee, and Delete Cafe from
the db.

The database form take as inputs and display as output the follow information:

	id, name, map_url, img_url,location, seats, toilet, wifi, sockets, can_take_calls, coffee_price. 
	

This a /Flask API and 


This program is made with:
	-Python
	-Flask
	-sqlite
	-SQLALchemy
	-tested with Postman
		POSTMAN link: To visualize the APIs format via JSON link:
		https://www.getpostman.com/collections/149dd1a341b3e971d3c7

APIs
	GET Random Cafe	
		http://127.0.0.1:5000/random?random
		-This API give a random Cafe from the db.
	
	GET All Cafes
		http://127.0.0.1:5000/all?all=
		-This one is a HTTP GET All the cafes from the db. 		

	GET Search Cafes By Location
		http://127.0.0.1:5000/search?loc=locationname
		-The /search route will search the cafe database for a cafe that matches the location queried.
		Use the loc parameter to pass a location name

	POST Add a new cafe
		http://127.0.0.1:5000/add
		-/add: this API is a POST method. Is a Form to add a new Cafe to the db.

	PATCH Update coffe price
		http://127.0.0.1:5000/update-price/22?new_price=$4
		-Update price of a single shoot coffee is in the database.update-price/CafeID?new_price=updateprice

	DELETE Cafe
		http://127.0.0.1:5000/report-closed/22?api_key=TopSecretToken
		-Delete cafe by add a security feature by requiring an api-key . If the api-key "TopSecretAPIKey" then 
		allowed to make the delete request, otherwise, tell  no authorized to make that request. A 403 in HTTP .


	