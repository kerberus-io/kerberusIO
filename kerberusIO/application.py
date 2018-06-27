from flask import Flask, render_template
import config


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)


@app.route('/')
def hello_world():
    return render_template("index.html")

