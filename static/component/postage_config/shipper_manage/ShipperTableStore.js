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
		'handleUpdateShipperMessages': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_SHIPPER_MESSAGES,
		'handleUpdateShipperTable': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_SHIPPER_TABLE,
		'handleGetShipperData': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_GET_SHIPPER_DATA,
		'handleDeleteShipper': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_DELETE_SHIPPER
	},

	init: function() {
		this.data = {
			'shipperId': -1
		};
	},

	handleUpdateShipperMessages: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleUpdateShipperTable: function(){
		this.__emitChange();
	},

	handleGetShipperData: function(action){
		console.log(action.data.rows[0],"----------");
		this.data = action.data.rows[0];
		this.__emitChange();
	},

	handleDeleteShipper: function(action){
		console.log(action,"1111111111");
		_.delay(function(){
			Reactman.PageAction.showHint('success', '删除成功');
		},100)
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = ShipperTableStore;