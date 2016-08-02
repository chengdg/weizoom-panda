/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:business.detail:Action');
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
			company_name: data['company_name'],
			company_type: JSON.stringify(data['company_type']),
			purchase_method: data['purchase_method'],
			points: data['points'],
			contacter: data['contacter'],
			phone: data['phone'],
			valid_time_from: data['valid_time_from'],
			valid_time_to: data['valid_time_to'],
			username: data['username'],
			password: data['password'],
			account_type: parseInt(data['account_type']),
			note: data['note']
		};
		account_info['id'] = data.id;
		// Resource.post({
		// 	resource: 'manager.account_create',
		// 	data: account_info,
		// 	success: function() {
		// 		Reactman.PageAction.showHint('success', '编辑客户信息成功');
		// 		setTimeout(function(){
		// 			Dispatcher.dispatch({
		// 				actionType: Constant.NEW_ACCOUNT_CREATE,
		// 				data: data
		// 			});
		// 		},1000);
		// 	},
		// 	error: function(data) {
		// 		Reactman.PageAction.showHint('error', data.errMsg);
		// 	}
		// });
	}
};

module.exports = Action;