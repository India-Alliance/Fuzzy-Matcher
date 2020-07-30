from flask import *
import standardise

app=Flask(__name__)

@app.route("/")
def upload():
	return render_template("home.html")

@app.route("/uploadSuccess", methods=["POST"])
def	uploadSuccess():
	print("reached")
	f=request.files['file']
	f.save(f.filename)
	standardised_name = standardise.standardiseList(f.filename)
	print(standardised_name)
	return render_template("success.html", tables=[standardised_name.to_html(classes='data', header="true")]) 	

@app.route("/success", methods=["POST"])
def show_disambiguated_name():
	entered_name = request.form['name-entry-field']
	standardised_name = standardise.standardiseName(entered_name)
	return render_template("success.html", tables=[standardised_name.to_html(classes='data', header="true")]) 	

@app.route("/download")
def download():
	filename = f.filename.split('.')[0] + "-standardised.pdf"
	return send_file(filename, as_attachment=True)

if __name__ == "__main__":
	app.run(debug=True)

