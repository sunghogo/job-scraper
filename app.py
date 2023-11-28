from Flask import Flask, render_template
from scraper.scraper import scrape

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
