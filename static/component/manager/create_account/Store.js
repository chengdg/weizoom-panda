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
		this.data = Reactman.loadJSON('user_profile_data');
		if (this.data) {
			this.data['account_type'] = String(this.data['account_type']);
			this.data['purchase_method'] = String(this.data['purchase_method']);
			this.data['company_type'] = JSON.parse(this.data['company_type']);
			if (this.data['purchase_method'] != '2'){
				this.data['points'] = '';
			}
		} else {
			this.data = {
				'id':-1,
				'account_type':'1',
				'purchase_method': '2',
				'company_type': []
			};
		}
		debug(this.data);
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