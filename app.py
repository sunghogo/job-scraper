from flask import Flask, render_template
from scraper.scraper import scrape_search

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    scrape_search(search_position = "Frontend Internship", search_location = "United States")
    scrape_search(search_position = "Full Stack Internship", search_location = "New York")
    scrape_search(search_position = "Software Engineer Internship", search_location = "New York")
    scrape_search(search_position="Software Engineer",
                  search_location="New York", experience_level = "ENTRY_LEVEL")
    # scrape_search(search_position="Software Engineer",
    #               search_location="United States", experience_level = "ENTRY_LEVEL")
    return render_template('index.html')


if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
