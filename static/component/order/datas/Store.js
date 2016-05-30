/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.datas:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleFilterOrders': Constant.ORDER_DATAS_FILTER_ORDERS
	},

	init: function() {
		this.data = {
		};
	},

	handleFilterOrders: function(action) {
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;