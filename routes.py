import redis, os, flask, numpy
import planning, configs

def_conf = configs.get_configs('configs/base')
app_conf = configs.get_configs('configs')

app = configs.create_app(app_conf['SECRET_KEY'])
#data = redis.Redis(host='redis', port=6379)
data = redis.Redis(host='localhost', port=6379)

@app.route('/dim')
@app.route('/')
def dim():
	global app_conf, def_conf

	return flask.render_template('dim.html', **def_conf)

@app.route('/last')
def last():
	global def_conf, data

	request = data.hgetall('compute')

	if not request:
		return flask.render_template(
			'last.html',
			height=None,
			**def_conf)

	return flask.render_template(
		'last.html',
		height=int(request[b'height']),
		width=int(request[b'width']),
		path=numpy.frombuffer(request[b'path'], numpy.int).reshape(-1, 2).tolist(),
		obstacles=numpy.frombuffer(request[b'obstacles'], numpy.int).reshape(-1, 2).tolist(),
		**def_conf)


@app.route('/compute/height<height>width<width>', methods=['POST'])
def compute(height: str, width: str):
	global app_conf, def_conf, data

	matrix, obstacles = planning.matrixFromDict(
		height=int(height),
		width=int(width),
		form=flask.request.form.to_dict())

	path = numpy.array(planning.astar(
		matrix.reshape(int(height), int(width)).tolist(),
		start=(0, 0),
		end = (int(width) - 1, int(height) - 1)))

	data.hmset('compute', {
		'path': path.tobytes(),
		'obstacles': obstacles.tobytes(),
		'height': height,
		'width': width})

	if None in path:
		flask.flash(app_conf['ERROR'], category='error')

	return flask.render_template(
		'compute.html',
		height=int(height),
		width=int(width),
		path=path.tolist(),
		obstacles=obstacles.tolist(),
		**def_conf)

@app.route('/start', methods=['POST'])
def start():
	global def_conf

	form = flask.request.form.to_dict()

	return flask.render_template(
		'start.html',
		height=int(form['height']), 
		width=int(form['width']), 
		**def_conf)

@app.errorhandler(404)
def nonePage(error):
	global def_conf

	return flask.render_template('none.html', **def_conf)

if __name__ == '__main__':
	app.run()
