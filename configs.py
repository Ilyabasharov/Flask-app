import yaml, os, flask

def get_configs(path='configs') -> dict:
    result = dict()
    
    for config in os.listdir(path):
        if config.endswith('yaml'):
            with open(os.path.join(path, config), 'r') as f:
                tmp = yaml.load(f, Loader=yaml.FullLoader)
                if tmp is not None:
                    result |= tmp

    return result

def create_app(key: str) -> flask.Flask:
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = key

    return app