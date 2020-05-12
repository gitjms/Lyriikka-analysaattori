from flask import Flask, render_template
app = Flask(__name__)


class Item:
	def __init__(self, name):
		self.name = name

@app.route("/")
def lyrfreq():
	return render_template("index.html")

if __name__ == "__main__":
	#app.run()
	app.run(debug=True)
