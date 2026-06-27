from flask import Flask, render_template, jsonify, request
from scipy import stats
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

# Metric description dictionary, to know where the scores come from
METRIC_DESCRIPTIONS = {
    'knowledge_score': 'Participants answered three questions about stream ecology — including criteria for ecological assessment, what bioindicators are, and what proportion of German streams are in good ecological condition.',
    'attitude':        'Participants rated how useful they personally find various stream protection measures (e.g. buying organic food, participating in group events). Scale: 1 (not useful) to 5 (very useful).',
    'awareness':       'Participants rated how threatening they consider various factors for river ecosystems (e.g. pesticide inputs, bank stabilisation). Scale: 1 (not threatening) to 5 (very threatening).',
    'skills':          'Participants self-rated their skills in ecology and stream monitoring, including their ability to collect standardised data and identify macroinvertebrates.',
    'personal_efficacy':   'Participants rated their agreement with statements about their personal ability to protect rivers and streams. Scale: 1 (strongly disagree) to 5 (strongly agree).',
    'collective_efficacy': 'Participants rated their belief that together with their community they can improve the ecological status of rivers and streams. Scale: 1 (strongly disagree) to 5 (strongly agree).',
    'behavioral_control':  'Participants rated how easy it is for them personally to take concrete actions to protect rivers and streams in everyday life. Scale: 1 (very difficult) to 5 (very easy).',
    'personal_norms':      'Participants rated their sense of personal responsibility and values regarding stream protection. Scale: 1 (strongly disagree) to 5 (strongly agree).',
    'nature_rel':          'Participants rated their connection to nature using the NR-6 scale (e.g. "My relationship to nature is an important part of who I am"). Scale: 1 (strongly disagree) to 5 (strongly agree).',
    'interest':            'Participants rated their interest in biology, ecological research, rivers and streams, freshwater protection, and environmental policy. Scale: 1 (not at all) to 5 (very strongly).',
    'past_behavior1':      'Participants reported how often they personally performed stream-protective behaviours (e.g. buying organic food, respecting protection rules). Scale: 1 (not at all) to 5 (very often).',
    'past_behavior2':      'Participants reported how often they engaged in collective stream-protective behaviours (e.g. attending events, contacting politicians). Scale: 1 (not at all) to 5 (very often).',
    'plan_behavior1':      'Participants reported whether they plan to personally protect rivers and streams in the coming weeks. Scale: 1 (does not apply) to 5 (applies completely).',
    'plan_behavior2':      'Participants reported whether they plan to engage collectively in stream protection in the coming weeks. Scale: 1 (does not apply) to 5 (applies completely).',
}

def get_significance(scores_a, scores_b):
    '''Compare two paired score lists using Wilcoxon signed-rank test.
    Returns a dict with the star symbol and p-value.'''
    # Need at least 10 pairs to run the test
    pairs_a = []
    pairs_b = []
    for a, b in zip(scores_a, scores_b):
        if a is not None and b is not None:
            pairs_a.append(a)
            pairs_b.append(b)

    if len(pairs_a) < 10:
        return {'star': 'ns', 'p': None}

    try:
        stat, p = stats.wilcoxon(pairs_a, pairs_b)
        if p <= 0.001:
            star = '***'
        elif p <= 0.01:
            star = '**'
        elif p <= 0.05:
            star = '*'
        else:
            star = 'ns'
        return {'star': star, 'p': round(float(p), 4)}
    except Exception:
        return {'star': 'ns', 'p': None}

# My Routes
# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Explore page
@app.route('/explore')
def explore():
    return render_template('explore.html', metrics=METRICS, descriptions=METRIC_DESCRIPTIONS)

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

        pre      = group_df[col_pre].dropna().tolist()
        post     = group_df[col_post].dropna().tolist()
        followup = group_df[col_followup].dropna().tolist()

        # Match paired scores for statistical tests
        paired_pre_post = group_df[[col_pre, col_post]].dropna()
        paired_pre_fu   = group_df[[col_pre, col_followup]].dropna()
        paired_post_fu  = group_df[[col_post, col_followup]].dropna()

        groups[code] = {
            'label':    label,
            'pre':      pre,
            'post':     post,
            'followup': followup,
            'stats': {
                'pre_vs_post':     get_significance(
                    paired_pre_post[col_pre].tolist(),
                    paired_pre_post[col_post].tolist()
                ),
                'pre_vs_followup': get_significance(
                    paired_pre_fu[col_pre].tolist(),
                    paired_pre_fu[col_followup].tolist()
                ),
                'post_vs_followup': get_significance(
                    paired_post_fu[col_post].tolist(),
                    paired_post_fu[col_followup].tolist()
                ),
            }
        }

    return jsonify({
        'metric':     metric,
        'label':      METRICS.get(metric, metric),
        'description': METRIC_DESCRIPTIONS.get(metric, ''),
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
