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
		'handleGetUnreadMes': Constant.GET_UNREAD_MESSAGE
	},

	init: function() {
		this.data = {
			unmessageList: []
		};
	},

	handleGetUnreadMes: function(data) {
		this.data.unmessageList = data.data.unmessageList;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;