import json
from flask import Flask, render_template, request

with open('candidates.json', 'r', encoding='utf8') as candidates_js:
    candidates = json.load(candidates_js)

with open('settings.json', 'r', encoding='utf8') as settings_js:
    settings = json.load(settings_js)

app = Flask(__name__)


@app.route('/')
def main():
    if settings['online']:
        return '<h2><b>Приложение работает</b></h2>' \
               '<p><a href="/list/">Список кандидатов</a></p></br>' \
               '<form action="/search_n/">' \
               '<label for="c_name">Поиск по кандидатам<br></label>' \
               '<input type="text" size="30" id="c_name" name="name" placeholder="Введите имя">' \
               '<button>искать</button>' \
               '</form></br>' \
               '<form action="/search_s/">' \
               '<label for="c_skill">Поиск по навыкам<br></label>' \
               '<input type="text" size="30" id="c_skill" name="skill" placeholder="Введите навык">' \
               '<button>искать</button>' \
               '</form>'

    else:
        return '<h2><b>Приложение не работает</b></h2>'


@app.route('/list/')
def candidates_list():
    return render_template('candidates_list.html', candidates=candidates)


@app.route('/candidate/<id_>/')
def candidate_page(id_):
    return render_template('candidate_page.html', candidates=candidates, id_=int(id_))


@app.route('/search_n/')
def search_candidates():
    search_name = request.args['name']
    search_name_result = []
    for cand in candidates:
        if settings['case-sensitive']:
            if search_name in cand['name']:
                search_name_result.append(cand)
        else:
            if search_name.lower() in cand['name'].lower():
                search_name_result.append(cand)
    return render_template('search_name.html', search_name_result=search_name_result,
                           num_of_res=len(search_name_result))


@app.route('/search_s/')
def search_skills():
    search_skill = request.args['skill']
    search_skill_result = []
    for cand in candidates:
        if search_skill.lower() in cand['skills'].lower():
            search_skill_result.append(cand)
    return render_template('search_skill.html', skill=search_skill,
                           search_skill_result=search_skill_result[0:settings['limit']],
                           num_of_res=len(search_skill_result))


if __name__ == "__main__":
    app.run()


