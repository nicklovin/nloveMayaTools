import commentjson
import os
import sys


def _format_json_data(data):
	editable_data = str(data)
	quote_data = editable_data.replace('\'', '\"')
	dict_data = eval(editable_data)
	formatted_data = format_json(dict_data)
	return str(formatted_data)


def save_to_json(data, filepath):
	with open(filepath, 'w') as f:
		f.write(_format_json_data(data))


# For safety re-writes: knows the incoming data is clean
def save_backup_to_json(data, filepath):
	with open(filepath, 'w') as f:
		f.write(str(data))


def load_from_json(filepath):
	with open(filepath) as f:
		# Should return as dict, check
		return commentjson.load(f)


def format_json(data):
	return commentjson.dumps(
		data,
		sort_keys=True,
		indent=4,
		default=repr,
		separators=(', ', ': ')).replace('    ', '\t')

