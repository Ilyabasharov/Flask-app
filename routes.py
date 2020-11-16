from flask import Flask
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
env = Environment(loader = FileSystemLoader('templates'))

@app.route('/')
def main():
	return env.get_template('base.html').render(title = 'hello')

if __name__ == '__main__':
	app.run(debug=True)