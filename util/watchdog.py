# -*- coding: utf-8 -*-
"""@package util.watchdog
"""
__author__ = 'bert'

from django.conf import settings

from eaglet.core import watchdog as eaglet_watchdog


def watchdog_debug(message, log_type="WEB"):
	eaglet_watchdog.debug(message, log_type=log_type, server_name=settings.SERVICE_NAME) 

def watchdog_info(message, log_type="WEB"):
	eaglet_watchdog.info(message, log_type=log_type, server_name=settings.SERVICE_NAME)  

def watchdog_warning(message, log_type="WEB"):
	eaglet_watchdog.warning(message, log_type=log_type, server_name=settings.SERVICE_NAME)  

def watchdog_error(message, log_type="WEB"):
	eaglet_watchdog.error(message, log_type=log_type, server_name=settings.SERVICE_NAME)  

def watchdog_alert(message, log_type="WEB"):
	eaglet_watchdog.alert(message, log_type=log_type, server_name=settings.SERVICE_NAME)  