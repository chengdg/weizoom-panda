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

var TableStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateShipperMessages': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_MESSAGES,
		'handleUpdateArea': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_AREA
	},

	init: function() {
		this.data = {
			'accountOrShipper': 'shipper',
			'selectedIds': []
		};
	},

	handleUpdateShipperMessages: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleUpdateArea: function(action){
		this.data.selectedIds = action.data.selectedIds;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = TableStore;