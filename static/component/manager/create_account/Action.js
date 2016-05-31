/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.create_account:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateAccount: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.NEW_ACCOUNT_UPDATE_ACCOUNT,
			data: {
				property: property,
				value: value
			}
		});
	},
	saveAccount: function(data) {
		var account_info = {
			name: data['name'],
			username: data['username'],
			password: data['password'],
			account_type: parseInt(data['account_type']),
			note: data['note']
		};

		if (data.id === -1) {
			Resource.put({
				resource: 'manager.account_create',
				data: account_info,
				success: function() {
					Reactman.PageAction.showHint('success', '创建账号成功');
					setTimeout(function(){
						Dispatcher.dispatch({
							actionType: Constant.NEW_ACCOUNT_CREATE,
							data: data
						});
					},1000);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				}
			});
		} else {
			account_info['id'] = data.id;
			Resource.post({
				resource: 'manager.account_create',
				data: account_info,
				success: function() {
					Reactman.PageAction.showHint('success', '编辑账号成功');
					setTimeout(function(){
						Dispatcher.dispatch({
							actionType: Constant.NEW_ACCOUNT_CREATE,
							data: data
						});
					},1000);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				}
			});
		}
	}
};

module.exports = Action;