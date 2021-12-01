import json
from flask import Flask, render_template

with open('candidates.json', 'r', encoding='utf8') as candidates_js:
    candidates = json.load(candidates_js)

with open('settings.json', 'r', encoding='utf8') as settings_js:
    settings = json.load(settings_js)



