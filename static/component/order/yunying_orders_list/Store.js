/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.yunying_orders_list:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleFilterOrders': Constant.FILTER_ORDERS,
		'handleOrderDatasExport': Constant.ORDER_DATAS_EXPORT
	},

	init: function() {
		this.data = {
		};
	},

	handleFilterOrders: function(action) {
		this.data.filterOptions = action.data;
		this.__emitChange();
	},
	handleOrderDatasExport: function(action){
		var filterOptions = this.data.filterOptions;
		console.log('filterOptions');
		console.log(filterOptions);
		var filter_str = '';
		window.location.href = '/order/yunying_export_orders';
	},
	getData: function() {
		return this.data;
	}
});

module.exports = Store;