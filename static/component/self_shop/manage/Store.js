/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:self_shop.manage:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateSelfShopDialog': Constant.UPDATE_SELF_SHOP_DIALOG,
		'handelUpdateSelfShops': Constant.UPDATE_SELF_SHOPS
	},

	init: function() {
		this.data = {};
	},

	handleUpdateSelfShopDialog: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handelUpdateSelfShops: function(action){
		this.data = action.data;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;