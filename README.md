# Citizen Science Visualizer

A Flask web app that visualizes how citizen science participation 
affects participants' knowledge, attitudes, and behaviour. Built around publicly available survey data from the **FLOW Citizen Science Project Survey (Zenodo, 2024)** https://zenodo.org/records/13268341


## Video Demo
[paste your YouTube URL here after recording]

## What it does

Citizen Science Visualizer lets users interactively explore 
survey data collected before, during and after participation 
in a citizen science project. 

Users can select from 14 metrics, including knowledge scores, environmental attitudes, and planned behaviour to see how scores changed across three timepoints (pretest, posttest and follow-up) for three participant groups: Citizen Scientists, Waiting Control, and Panel Control.

Each chart shows:
- Individual data points (box plots with all points visible)
- Statistical significance markers (* p≤0.05, ** p≤0.01, *** p≤0.001)
- Metric descriptions explaining what each score measures
- Interactive hover tooltips showing exact values and p-values
- Option to download as PNG

## How to run it

```bash
git clone https://github.com/YOUR-USERNAME/citizen-science-visualizer.git
cd citizen-science-visualizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 fetch_data.py
python3 app.py
```
Then open http://127.0.0.1:5000 in Safari or Firefox.
Note: fetch_data.py must be run once before app.py. It downloads and cleans the raw dataset from data/raw/ and saves it as data/flow_clean.csv, which the app reads at startup.
Note: This app was developed and tested on Mac. Windows users may need to use python instead of python3 and venv\Scripts\activate instead of source venv/bin/activate.

## Data source

Participant survey data from the citizen science project FLOW, 2021
Dataset DOI: https://doi.org/10.5281/zenodo.13268341
Licence: CC-BY

von Gönner, J., Masson, T., Köhler, S., Fritsche, I., Bonn, A. (2024).
Citizen science promotes knowledge, skills and collective action 
to monitor and protect freshwater streams. People and Nature.



## Design decisions

**Flask over Django** — Flask is lightweight and sufficient for 
a single-dataset read-only app. No database needed since data 
is served from a pre-cleaned CSV loaded at startup.

**Plotly.js over Chart.js** — Plotly natively supports box plots 
with individual points (beeswarm-style), which is scientifically 
more honest than bar charts showing only means.

**API-first data layer** — chart data is served via a /api/data 
endpoint rather than embedded in the HTML. This separates data 
logic from presentation and makes the app extensible.

**Short codes in data, readable labels in presentation** — 
group codes (treat, ctr1, ctr2) are used in the CSV while 
human-readable labels are defined once in app.py and passed 
to all templates. This follows separation of concerns.

**Wilcoxon signed-rank test** — chosen over t-test because 
the score distributions are not guaranteed to be normal, 
and the data is paired (same participants at each timepoint).

## Future features

- Support for additional citizen science datasets (drop-in CSV)
- Demographics tab: filter by age group and gender
- Change score chart: visualize pre→post difference per group


## Inspired by

This project was built as the CS50x final project by Romana Yáñez, 
who is interested in the intersection of citizen science, 
data visualization and science communication.

