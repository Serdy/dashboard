from docker import Client
import signal
import requests


def docker_urls():
	with open('cluster') as f:
		docker_urls = []
		for x in f.readlines():
			if x[-1:] == "\n":
				docker_urls.append(x[:-1])
			else:
				docker_urls.append(x)
		return docker_urls
			

def docker_name_up(*args):
	docker_name = []
	for docker_url in docker_urls():
		try:
		    cli = Client(base_url='tcp://' + docker_url + ':2375', timeout=5)
		    for x in cli.containers(all=True):
				id = (x['Id'][:12])
				status =  (x['Status'])
				name = (x['Names'][0][1:])
				ip = (x['NetworkSettings']['Networks']['bridge']['IPAddress'])
				dockers = { 'Id': id, 'Status': status, 'Name': name, 'ip': ip, 'Docker_host_ip': docker_url }
				docker_name.append(dockers)
		except requests.ConnectionError:
		    pass
	return docker_name


def search_docker(docker_name_up, search):
	docker_name = []
	for resuts_search in (x for x in docker_name_up if search in x['Name']):
		docker_name.append(resuts_search)
	return docker_name


def docker_logs(docker_url, containet_id):
	cli = Client(base_url='tcp://' + docker_url + ':2375')
	logs = cli.logs(containet_id, stdout=True, stderr=True, stream=False, tail=100, timestamps=True)
	return logs

def docker_top(docker_url, containet_id):
	cli = Client(base_url='tcp://' + docker_url + ':2375')
	top = cli.top(containet_id, 'aux')
	return top 

def docker_intro(docker_url, containet_id):
	cli = Client(base_url='tcp://' + docker_url + ':2375')
	docker = cli.inspect_container(containet_id)
	id = (docker['Id'][:12])
	status =  (docker['State']['Status'])
	name = (docker['Name'][1:])
	ip = (docker['NetworkSettings']['Networks']['bridge']['IPAddress'])
	image = (docker['Config']['Image'])
	hostname = (docker['Config']['Hostname'])
	entrypoint = (docker['Config']['Entrypoint'])
	mount_point = (docker['HostConfig']['Binds']) 
	intro = { 'Id': id, 'Status': status, 'Name': name, 'ip': ip, 'Docker_host_ip': docker_url, 'Image': image, 'Hostname': hostname, 'Entrypoint': entrypoint, 'Mount': mount_point }
	return intro
	