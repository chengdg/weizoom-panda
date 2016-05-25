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
		var account = {
			name: data['name'],
			username: data['username'],
			password: data['password'],
			account_type: data['account_type']
		};

		//if (data.id === -1) {
		Resource.put({
			resource: 'manager.account_create',
			data: account,
			success: function() {
				Dispatcher.dispatch({
					actionType: Constant.NEW_ACCOUNT_CREATE,
					data: data
				});
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMg);
			}
		});
		//} else {
		//	account['id'] = data.id;
		//	Resource.post({
		//		resource: 'manager.account_create',
		//		data: account,
		//		dispatch: {
		//			dispatcher: Dispatcher,
		//			actionType: Constant.NEW_ACCOUNT_CREATE
		//		}
		//	});
		//}
	}
};

module.exports = Action;