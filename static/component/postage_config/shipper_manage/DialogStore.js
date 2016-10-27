/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var DialogStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateData': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_DATA,
		'handleGetData': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_GET_DATA,
		'handleClearData': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_CLEAR_DATA
	},

	init: function() {
		this.data = {
			'shipperId': -1,
			'expressId': -1,
			'expressName': -1,
			'regional': ''
		};
	},

	handleUpdateData: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleGetData: function(action){
		console.log(action.data.rows[0],"+++++ssss++++");
		this.data = action.data.rows[0];
		this.__emitChange();
	},

	handleClearData: function(){
		this.data = {
			'shipperId': -1,
			'expressId': -1,
			'expressName': -1
		};
	},

	getData: function() {
		return this.data;
	}
});

module.exports = DialogStore;