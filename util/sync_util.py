# -*- coding: utf-8 -*-

from eaglet.utils.resource_client import Resource

from panda.settings import EAGLET_CLIENT_ZEUS_HOST, ZEUS_SERVICE_NAME


def sync_zeus(params, resource, method='get'):

	if method == 'get':
		return __sync_zeus_get(params, resource)
	elif method == 'put':

		return __sync_zeus_put(params, resource)
	elif method == 'post':
		return __sync_zeus_post(params, resource)
	else:
		return __sync_zeus_delete(params, resource)

def __sync_zeus_put(params, resource):
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
		'resource': resource,
		'data': params
	})
	if resp and resp.get('code') == 200:
		return True, resp.get('data')
	else:
		return False, None

def __sync_zeus_delete(params, resource):
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete({
		'resource': resource,
		'data': params
	})
	if resp and resp.get('code') == 200:
		return True, resp.get('data')
	else:
		return False, None

def __sync_zeus_post(params, resource):
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
		'resource': resource,
		'data': params
	})
	if resp and resp.get('code') == 200:
		return True, resp.get('data')
	else:
		return False, None

def __sync_zeus_get(params, resource):
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).get({
		'resource': resource,
		'data': params
	})
	if resp and resp.get('code') == 200:
		return True, resp.get('data')
	else:
		return False, None