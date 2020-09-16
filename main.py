from config import app
@app.route("/")
def home():
    return "<h1>Hello from Prason </h1>"

if(__name__)=='__main__':
    app.run(debug=True,host='0.0.0.0')