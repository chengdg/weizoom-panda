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

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleFilterOrders': Constant.ORDER_DATAS_FILTER_ORDERS,
		//'handleOrderShipInformations': Constant.ORDER_SHIP_INFORMATIONS,
		'handleOrderDatasExport': Constant.ORDER_DATAS_EXPORT,
		'handleOrderUpdateShip':Constant.ORDER_DATAS_UPDATE_SHIP,
		'handlePrintOrder': Constant.ORDER_CUSTOMER_ORDER_LIST_PRINT_ORDER,
		'handleCanPRint': Constant.ORDER_CUSTOMER_ORDERS_LIST_CAN_PRINT
	},

	init: function() {
		this.data = {
			documents: [],
			optionsForExpress: [],
			template: '',
			canPrint: false
		};
		var optionsForExpress = Reactman.loadJSON('optionsForExpress');
		if(optionsForExpress){
			console.log(optionsForExpress,"=====");
			this.data['optionsForExpress'] = optionsForExpress;
		}
	},

	handleFilterOrders: function(action) {
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	handleOrderUpdateShip: function(action) {
		debug('update %s to %s', action.data.property, JSON.stringify(action.data.value));
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleOrderDatasExport: function(action){
		var filterOptions = this.data.filterOptions;
		var filter_str = '';
		for (var key in filterOptions){
			filter_str = filter_str + key + '=' + filterOptions[key] + '&';
		}
		filter_str = filter_str.substring(0,filter_str.length-1);
		window.location.href = '/order/export_orders/?'+filter_str;
	},

	handlePrintOrder: function(action){
		var template = action.data['template'];
		console.log(action.data,"=========");
		this.data['template'] = template;
		// this.__emitChange();
	},

	handleCanPRint: function(){
		this.data['canPrint'] = true;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;