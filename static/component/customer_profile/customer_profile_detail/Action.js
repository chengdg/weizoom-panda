/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:customer_profile.customer_profile_detail:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	changeAccountStatus: function(id,_method) {
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
			success: function() {
				Reactman.PageAction.showHint('success', '删除账号成功');
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
	filterAccounts: function(filterOptions) {
		console.log(filterOptions);
		Dispatcher.dispatch({
			actionType: Constant.MANAGER_ACCOUNT_FILTER_ACCOUNTS,
			data: filterOptions
		});
	},
	exportAccounts: function(){
		Dispatcher.dispatch({
			actionType: Constant.MANAGER_ACCOUNT_EXPORT,
			data: {}
		});
	}
};

module.exports = Action;