from flask import *
import standardise

app=Flask(__name__)

@app.route("/")
def upload():
	return render_template("home.html")

@app.route("/success", methods=["POST"])
def show_disambiguated_name():
	entered_name = request.form['name-entry-field']
	print(entered_name)
	standardised_name = standardise.standardise(entered_name)
	print(standardised_name)
	return render_template("success.html", tables=[standardised_name.to_html(classes='data', header="true")]) 	

if __name__ == "__main__":
	app.run(debug=True)

