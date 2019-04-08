import flask
import json
import requests
import argparse


from student import Student, Group


app = flask.Flask("lazy_students")
app.group = Group()


# API methods
@app.route('/count', methods=['GET'])
def count():
    print(app.group)
    return json.dumps({"count": app.group.count()}) + "\n"


@app.route('/add', methods=['POST'])
def add():
    print(app.group)
    if 'name' in flask.request.args:
        app.group.add_student(flask.request.args['name'])
        return 'OK'
    else:
        flask.abort(400)


@app.route('/get_ideas', methods=['GET'])
def get_ideas():
    return json.dumps(app.group.get_ideas()) + "\n"


@app.route('/free', methods=['POST'])
def free():
    if 'id' in flask.request.args:
        try:
            app.group.free(int(flask.request.args['id']))
            return 'OK'
        except ValueError as err:
            flask.abort(400)
    else:
        flask.abort(400)


# Page handlers

@app.route('/group', methods=['GET'])
def show_group():
    count_response = requests.get('http://127.0.0.1:50002/count').json()

    return flask.render_template(
        'group.html',
        count=count_response['count']
    )


@app.route('/ideas', methods=['GET'])
def show_ideas():
    ideas = requests.get('http://127.0.0.1:50002/get_ideas').json()

    return flask.render_template(
        'ideas.html',
        ideas=ideas
    )


@app.route('/add_button', methods=['POST'])
def add_button():
    if 'name' in flask.request.form:
        print(type(flask.request.form['name']))
        print(flask.request.form['name'])
        requests.post("http://127.0.0.1:50002/add?name={}".format(flask.request.form['name']))

        return flask.redirect('http://127.0.0.1:50002/group')
    else:
        flask.abort(400)


@app.route('/free_button', methods=['POST'])
def free_button():
    if 'id' in flask.request.args:
        requests.post('http://127.0.0.1:50002/free?id={}'.format(
            flask.request.args['id']
        ))
        return flask.redirect('http://127.0.0.1:50002/group')
    else:
        flask.abort(400)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int)
    args = parser.parse_args()

    app.run('::', args.port, debug=True, threaded=True)

