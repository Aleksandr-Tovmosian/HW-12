import json
from flask import Flask, render_template, request

with open('candidates.json', 'r', encoding='utf8') as candidates_js:    # импортируем список кандидатов
    candidates = json.load(candidates_js)

with open('settings.json', 'r', encoding='utf8') as settings_js:    # импортируем настройки
    settings = json.load(settings_js)

app = Flask(__name__)


@app.route('/')     # сделал главную страницу без файла html, т.к. тут не требовались циклы
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


@app.route('/list/')        # роут для списка кандидатов
def candidates_list():
    return render_template('candidates_list.html', candidates=candidates)


@app.route('/candidate/<id_>/')     # роут для страницы кандидата
def candidate_page(id_):
    return render_template('candidate_page.html', candidates=candidates, id_=int(id_))


@app.route('/search_n/')    # роут для страницы поиска кандидата по имени
def search_candidates():
    search_name = request.args['name']      # получаем данные, введённые пользователем
    search_name_result = []     # пустой список найденных результатов
    for cand in candidates:     # запускаем цикл по списку кандидатов
        if settings['case-sensitive']:      # проверяем настройку на учёт регистра
            if search_name in cand['name']:     # если запрос пользователя есть в имени очередного кандидата,
                # то добавляем его в список совпадений
                search_name_result.append(cand)
        else:
            if search_name.lower() in cand['name'].lower():
                search_name_result.append(cand)
    return render_template('search_name.html', search_name_result=search_name_result,
                           num_of_res=len(search_name_result))
    # передаем в файл search_name список результатов поиска и длину списка


@app.route('/search_s/')    # почти тоже самое, что и выше
def search_skills():
    search_skill = request.args['skill']
    search_skill_result = []
    for cand in candidates:
        if search_skill.lower() in cand['skills'].lower():
            search_skill_result.append(cand)
    return render_template('search_skill.html', skill=search_skill,
                           search_skill_result=search_skill_result[0:settings['limit']],
                           num_of_res=len(search_skill_result))
    # передаем срез списка кандидатов в зависимости от настроек и какой запрос был отправлен


if __name__ == "__main__":
    app.run()


