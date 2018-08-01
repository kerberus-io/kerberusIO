from flask import Flask, render_template, redirect, url_for, request
import config


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
