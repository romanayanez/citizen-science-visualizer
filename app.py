from flask import Flask, render_template, jsonify, request
import pandas as pd

# my Flask app
app = Flask(__name__)

# Load my clean data
df = pd.read_csv('data/flow_clean.csv')

# Name dictionaries: data to presentation 
GROUP_LABELS = {
    'treat': 'Citizen Scientists',
    'ctr1': 'Waiting Control',
    'ctr2': 'Panel Control'
}

TIMEPOINT_COLORS = {
    'pre':      "#f3ba47",   # yellow
    'post':     "#0088ff",   # blue
    'followup': "#04c18e"    # dark green
}

GENDER_LABELS = {
    'male': 'Male',
    'female': 'Female'
}

# Metrics user can choose to visualize
METRICS = {
    'knowledge_score':     'Knowledge Score',
    'attitude':            'Attitude Toward Environment',
    'awareness':           'Awareness of Threats',
    'skills':              'Skills',
    'personal_efficacy':   'Personal Efficacy',
    'collective_efficacy': 'Collective Efficacy',
    'behavioral_control':  'Behavioral Control',
    'personal_norms':      'Personal Norms',
    'nature_rel':          'Nature Relatedness',
    'interest':            'Interest in the Environment',
    'past_behavior1':      'Past Personal Behaviour',
    'past_behavior2':      'Past Collective Behaviour',
    'plan_behavior1':      'Planned Personal Behaviour',
    'plan_behavior2':      'Planned Collective Behaviour',
}

# My Routes
# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Explore page
@app.route('/explore')
def explore():
    return render_template('explore.html', metrics=METRICS)

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# API route to return data for a given metric as JSON
@app.route('/api/data')
def get_data():
    # Get the metric from the URL e.g. /api/data?metric=knowledge_score
    metric = request.args.get('metric', 'knowledge_score')

    # Column names for 3 time-points
    col_pre      = f'{metric}.1'
    col_post     = f'{metric}.2'
    col_followup = f'{metric}.3'

    groups = {}
    for code, label in GROUP_LABELS.items():
        group_df = df[df['group'] == code]

        groups[code] = {
            'label':    label,
            'pre':      group_df[col_pre].dropna().tolist(),
            'post':     group_df[col_post].dropna().tolist(),
            'followup': group_df[col_followup].dropna().tolist(),
        }

    return jsonify({
        'metric':     metric,
        'label':      METRICS.get(metric, metric),
        'timepoints': ['Pre', 'Post', 'Follow-up'],
        'groups':     groups,
        'colors': {
            'pre':      TIMEPOINT_COLORS['pre'],
            'post':     TIMEPOINT_COLORS['post'],
            'followup': TIMEPOINT_COLORS['followup'],
        }
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
