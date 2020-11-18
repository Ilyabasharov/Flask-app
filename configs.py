import yaml, os

def get_configs(path='configs') -> dict:
	result = dict()

	for config in os.listdir(path):
		item, end = os.path.splitext(config)

		if end == 'yaml':
			with open(os.path.join('configs', config), 'r') as f:
				result |= yaml.load(f)

	return result