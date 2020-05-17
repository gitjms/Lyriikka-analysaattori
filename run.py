from application import app
from flask import Flask

app.add_url_rule('/images/<path:filename>', ...)

if __name__ == "__main__":
	#app.run()
	app.run(debug=True)
