import yaml, os

def get_configs(path='configs') -> dict:
	result = dict()

	for config in os.listdir(path):
		if config.endswith('yaml'):
			with open(os.path.join('configs', config), 'r') as f:
				tmp = yaml.load(f, Loader=yaml.FullLoader)
				
				if tmp is not None:
					result |= tmp

	return result