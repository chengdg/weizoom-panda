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

var AccountTableStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateArea': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_AREA,
		'handleUpdateAccountTable': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_ACCOUNT_TABLE,
		'handleDeleteExpressBillAccount': Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_DELETE_EXPRESS_ACCOUNT
	},

	init: function() {
		this.data = {
			'expressId': -1
		};
	},

	handleUpdateArea: function(action){
		this.data.selectedIds = action.data.selectedIds;
		this.__emitChange();
	},

	handleUpdateAccountTable: function(){
		this.__emitChange();
	},

	handleDeleteExpressBillAccount: function(action){
		_.delay(function(){
			Reactman.PageAction.showHint('success', '删除成功');
		},100)
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = AccountTableStore;