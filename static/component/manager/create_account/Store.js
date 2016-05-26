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
var W = Reactman.W;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateAccount': Constant.NEW_ACCOUNT_UPDATE_ACCOUNT,
		'handleCreateNewAccount': Constant.NEW_ACCOUNT_CREATE
	},

	init: function() {
		this.data = {
			'account_type':'1'
		};
	},

	handleUpdateAccount: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleCreateNewAccount: function(action) {
		W.gotoPage('/manager/account/');
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;