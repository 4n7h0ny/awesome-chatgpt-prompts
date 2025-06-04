from flask import Flask, render_template, request, jsonify, url_for
import csv
import os

app = Flask(__name__)

PROMPTS = []

# Load prompts from repository CSV on startup
csv_path = os.path.join(os.path.dirname(__file__), '..', 'prompts.csv')
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        PROMPTS.append(row)

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    dev_only = request.args.get('dev') == '1'

    results = []
    for p in PROMPTS:
        if dev_only and p['for_devs'].upper() != 'TRUE':
            continue
        if query in p['act'].lower() or query in p['prompt'].lower() or not query:
            results.append(p)

    return render_template('index.html', prompts=results, query=query, dev_only=dev_only)

@app.route('/api/prompts')
def api_prompts():
    return jsonify(PROMPTS)

if __name__ == '__main__':
    app.run(debug=True)
