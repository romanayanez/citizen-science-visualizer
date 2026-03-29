from flask import Flask, render_template
import pandas as pd

# Flask app setup
app = Flask(__name__)

# Load cleaned data once, when app starts
df = pd.read_csv('data/flow_clean.csv')

# Make labels more readable for display
GROUP_LABELS = {
    'treat': 'Citizen Scientists',
    'ctr1': 'Waiting Control',
    'ctr2': 'Panel Control'
}

GENDER_LABELS = {
    'male': 'Male',
    'female': 'Female',
}

# Routes

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Explore page
@app.route('/explore')
def explore():
    return render_template('explore.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)