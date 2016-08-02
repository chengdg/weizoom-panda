/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleCustomerDataFilter': Constant.CUSTOMER_DATAS_FILTER,
		'handleCustomerDataExport': Constant.CUSTOMER_DATAS_EXPORT
	},

	init: function() {
		this.data = {};
	},

	handleCustomerDataFilter: function(action){
		this.data = action.data;
		this.__emitChange();
	},

	handleCustomerDataExport: function(action){
		var filterOptions = this.data;
		console.log('filterOptions');
		console.log(filterOptions);
		var filter_str = '';
		for (var key in filterOptions){
			filter_str = key +'=' + filterOptions[key];
		}
		console.log('/customer/customer_exported/?'+filter_str)
		window.location.href = '/customer/customer_exported/?'+filter_str;
	},

	getFilter: function() {
		return this.data;
	}
});

module.exports = Store;