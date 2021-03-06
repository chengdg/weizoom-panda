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
//		'handleAddRebateValue': Constant.ADD_REBATE_VALUE,
		'handleMessageFilter': Constant.MESSAGE_FILTER
	},

	init: function() {
		this.data = {
		    'models': [],
		};
	},

	handleMessageFilter: function(action) {
		this.data.models = action.data.models;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;