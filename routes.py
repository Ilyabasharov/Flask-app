from flask import (
	Flask,
	request,
	render_template
	)

from configs import get_configs

app = Flask(__name__)
configs = get_configs()

@app.route('/start')
def start():
	return render_template('start.html', **configs)

@app.route('/')
@app.route('/dim')
def main():
	return render_template('dim.html', **configs)

if __name__ == '__main__':
	app.run(debug=True)