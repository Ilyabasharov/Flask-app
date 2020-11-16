from flask import (
	Flask,
	render_template)

app = Flask(__name__)

@app.route('/start')
def start():
	return render_template('start.html', title='hello')

@app.route('/')
@app.route('/main')
def main():
	return render_template('main.html')

if __name__ == '__main__':
	app.run(debug=True)