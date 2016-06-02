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
		'handleUpdateProduct': Constant.ORDER_DATA_SHIP_ORDER
	},

	init: function() {
		this.data = {};
	},

	handleUpdateProduct: function(action) {
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;