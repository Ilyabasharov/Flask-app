import redis, os, flask, numpy
import configs

def_conf = configs.get_configs('configs/base')
app_conf = configs.get_configs('configs')

app = configs.create_app(app_conf['SECRET_KEY'])
data = redis.StrictRedis(host='localhost')

@app.route('/')
@app.route('/dim', methods=['POST'])
def dim():
	global app_conf, def_conf

	if flask.request.method == 'POST':
		if configs.checkCorrectness(**flask.request.form):
			return flask.redirect(flask.url_for('start', **flask.request.form))
		else:
			flask.flash(app_conf['ERROR'], category='error')

	return flask.render_template('dim.html', **def_conf)

@app.route('/compute/height<height>width<width>', methods=['POST'])
def compute(height: str, width: str):
	global app_conf, def_conf, data

	data.set('map', configs.matrixFromDict(
		height=int(height),
		width=int(width),
		form=flask.request.form.to_dict()
		).tobytes())

	return flask.render_template('dim.html', **def_conf)

@app.route('/start/height<height>width<width>')
def start(height: str, width: str):
	global def_conf

	return flask.render_template('start.html',
		height=int(height), width=int(width), **def_conf)

@app.errorhandler(404)
def nonePage(error):
	global def_conf

	return flask.render_template('none.html', **def_conf)

if __name__ == '__main__':
	app.run(debug=True)