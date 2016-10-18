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
		'handleChangeTable': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_CHANGE_TABLE,
		'handleUpdateTable': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_TABLE
	},

	init: function() {
		this.data = {
			'accountOrShipper': 'account'
		};
	},

	handleChangeTable: function(action){
		var accountOrShipper = action.data.status;
		if(accountOrShipper=='account'){
			this.data['accountOrShipper'] = 'shipper';
		}else{
			this.data['accountOrShipper'] = 'account';
		}
		this.__emitChange();
	},

	handleUpdateTable: function(){
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;