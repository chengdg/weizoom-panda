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

var ShipperTableStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateShipperTable': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_SHIPPER_TABLE,
		'handleDeleteShipper': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_DELETE_SHIPPER,
		'handleSetSelected': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_SET_SELECTED
	},

	init: function() {
		this.data = {
			'shipperId': -1
		};
	},

	handleUpdateShipperTable: function(){
		this.__emitChange();
	},

	handleDeleteShipper: function(action){
		_.delay(function(){
			Reactman.PageAction.showHint('success', '删除成功');
		},100)
		this.__emitChange();
	},

	handleSetSelected: function(action){
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = ShipperTableStore;