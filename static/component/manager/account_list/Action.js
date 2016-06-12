/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.account_list:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	changeAccountStatus: function(id,_method) {
		console.log('changeAccountStatus');
		console.log(id,_method);
		Resource.post({
			resource: 'manager.account',
			data: {
				id: id,
				method: _method
			},
			success: function() {
				Reactman.PageAction.showHint('success', '修改状态成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.MANAGER_ACCOUNT_UPDATE_ACCOUNT,
						data: {}
					});
				},1000);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	},

	deleteAccount: function(id) {
		Resource.delete({
			resource: 'manager.account',
			data: {
				id: id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.MANAGER_ACCOUNT_UPDATE_ACCOUNT
			}
		});
	},
	filterAccounts: function(filterOptions) {
		console.log(filterOptions);
		Dispatcher.dispatch({
			actionType: Constant.MANAGER_ACCOUNT_FILTER_ACCOUNTS,
			data: filterOptions
		});
	}
};

module.exports = Action;