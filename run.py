from application import app
from flask import Flask


if __name__ == "__main__":
	#app.run()
	#app.run(debug=True)
	app.run(debug=Flask.debug)
