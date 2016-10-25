/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:customer_profile.list_customer_profile:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateAccount': Constant.MANAGER_ACCOUNT_UPDATE_ACCOUNT,
		'handleFilterAccounts': Constant.MANAGER_ACCOUNT_FILTER_ACCOUNTS,
		'handleAccountDatasExport': Constant.MANAGER_ACCOUNT_EXPORT
	},

	init: function() {
		this.data = {
		};
	},

	handleUpdateAccount: function(action) {
		this.__emitChange();
	},

	handleFilterAccounts: function(action) {
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	},
	handleAccountDatasExport: function(action){
		var filterOptions = this.data.filterOptions;
		var filter_str = '';
		window.location.href = '/manager/account_export';
	},
});

module.exports = Store;