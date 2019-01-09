from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/datacosts")
def datacosts():
    costs= [1,2,3,4]
    return render_template('datacosts.html', costs=costs)

if __name__ == "__main__":
    app.run()
