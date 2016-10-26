/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_orders_list:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var ChooseExpressStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateExpressCompany': Constant.ORDER_CUSTOMER_ORDERS_LIST_UPDATE_EXPRESS_COMPANY
	},

	init: function() {
		this.data = {
			optionsForExpress: []
		};
		var optionsForExpress = Reactman.loadJSON('optionsForExpress');
		if(optionsForExpress){
			this.data['optionsForExpress'] = optionsForExpress;
		}
	},

	handleUpdateExpressCompany: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = ChooseExpressStore;