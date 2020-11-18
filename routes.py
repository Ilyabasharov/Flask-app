import redis, flask
import configs

app = configs.create_app()
data = redis.Redis(host='127.0.0.1', port=5001, db=0)
defaults = configs.get_configs('configs/base')

@app.route('/start', methods=['POST', 'GET'])
def start():
	return flask.render_template('start.html', **defaults)

@app.route('/')
@app.route('/dim', methods=['POST'])
def main():
	if flask.request.method == 'POST':
		if configs.checkCorrectness(**flask.request.form):
			flask.redirect(flask.url_for('/start'))
		else:
			flask.flash('Oooops! Check your input.', category='error')

	return flask.render_template('dim.html', **defaults)

@app.errorhandler(404)
def nonePage(error):
	return flask.render_template('none.html', **defaults)

if __name__ == '__main__':
	app.run(debug=True)