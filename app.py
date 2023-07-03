from flask import Flask, render_template
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

print("sneed")

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 8080, True)