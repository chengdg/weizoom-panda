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