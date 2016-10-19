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
		'handleUpdateShipperMessages': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_SHIPPER_MESSAGES,
		'handleGetShipperData': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_GET_SHIPPER_DATA,

		'handleUpdateAccountMessages': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_ACCOUNT_MESSAGES,
		'handleGetExpressBillAccount': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_GET_EXPREEE_ACCOUNT,
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

	handleUpdateAccountMessages: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleGetExpressBillAccount: function(action){
		this.data = action.data.rows[0];
		this.__emitChange();
	},

	handleGetShipperData: function(action){
		console.log(action.data.rows[0],"----------");
		this.data = action.data.rows[0];
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = DialogStore;