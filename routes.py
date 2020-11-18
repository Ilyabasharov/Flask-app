from flask import (
	Flask,
	request,
	render_template
	)

from configs import get_configs

app = Flask(__name__)
configs = get_configs()

@app.route('/start', methods=['POST', 'GET'])
def start():
	if request.method == 'POST':
		print(request.form)

	return render_template('start.html', **configs)

@app.route('/')
@app.route('/dim')
def main():
	return render_template('dim.html', **configs)

@app.errorhandler(404)
def nonePage(error):
	return render_template('none.html', **configs)

if __name__ == '__main__':
	app.run(debug=True)