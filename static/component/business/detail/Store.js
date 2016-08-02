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

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleCustomerDataFilter': Constant.CUSTOMER_DATAS_FILTER
	},

	init: function() {
		this.data = Reactman.loadJSON('business_data');
		if (this.data) {
			this.data['account_type'] = String(this.data['account_type']);
			if (this.data['account_type'] == '1'){
				this.data['purchase_method'] = String(this.data['purchase_method']);
				this.data['company_type'] = JSON.parse(this.data['company_type']);
				this.data['options_for_type'] = [];
				if (this.data['purchase_method'] != '2'){
					this.data['points'] = '';
				}
			}
		}
	},

	handleSelect: function(action) {
		this.data['options_for_type'] = action.data.rows;
		this.__emitChange();
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