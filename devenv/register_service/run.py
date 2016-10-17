# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import json
import subprocess
import socket
import etcd
import json

parser = OptionParser()
parser.add_option("--port", dest="port", help="service's port")

options = None

def get_local_ip():
	try:
		csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		csock.connect(('8.8.8.8', 80))
		(addr, port) = csock.getsockname()
		csock.close()
		return addr
	except socket.error:
		return "127.0.0.1"

def invoke(command):
	print '***** start output for `%s` *****' % command
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while True:
		line = p.stdout.readline()
		if not line:
			break
		print '\t', line
	print '***** finish output for %s *****' % command

def do_register_bak():
	if os.name == 'posix':
		template = './linux.tmpl'
	else:
		template = './windows.tmpl'

	with open(template) as f:
		commands_tmpl = f.read()

	commands = commands_tmpl % {"port": options.port}
	with open('./register_service.sh', 'wb') as f:
		f.write(commands)

	invoke('bash ./register_service.sh')
	print 'success'

def load_config_from_json_file():
	"""
	load config from json file
	"""
	with open('./config.json', 'rb') as f:
		content = f.read()

	base_dir = os.path.join('.', '../..')
	config = json.loads(content)
	locations = []
	for location in config['locations']:
		root = os.path.abspath(os.path.join(base_dir, location['root']))
		locations.append("location %s { root %s; }" % (location['path'], root))

	config['locations'] = locations

	return config

def load_config(client, key):
	"""
	load config from etcd if etcd has the key
	otherwise, load config from config.json
	"""
	try:
		content = client.get(key)
		print '[register] use existed config from etcd'
		return json.loads(content.value)
	except:
		print '[register] use new config from config.json'
		return load_config_from_json_file()

def load_service_name():
	"""
	load service_name from service.json
	"""
	service_json_path = '../../service.json'
	with open(service_json_path, 'rb') as f:
		content = f.read()
		return json.loads(content)['name']

def do_register():
	client = etcd.Client(host='etcd.weizoom.com')
	service_name = load_service_name()
	key = "/service/%s" % service_name
	config = load_config(client, key)
	host = '%s:%s' % (get_local_ip(), options.port)

	if not host in config['hosts']:
		config['hosts'].append(host)
	client.set(key, json.dumps(config))
	print '[register] register to %s' % key

def register():
	do_register()
	#if '_IS_WEIZOOM_DEV_VM' in os.environ:
	#	do_register()
	#else:
	#	print 'not in weizoom dev vm, do nothing'

if __name__ == '__main__':
	options, args = parser.parse_args()
	register()