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
		'handleCanPrintTrue': Constant.ORDER_CUSTOMER_ORDERS_LIST_CAN_PRINT_TRUE,
		'handleCanPrintFalse': Constant.ORDER_CUSTOMER_ORDERS_LIST_CAN_PRINT_FALSE
	},

	init: function() {
		this.data = {
			documents: [],
			optionsForExpress: [],
			templates: '[]',
			canPrint: false,
			isSuccess: false
		};
		var optionsForExpress = Reactman.loadJSON('optionsForExpress');
		if(optionsForExpress){
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
		var templates = action.data['templates'];
		var isSuccess = action.data['is_success'];
		var reason = action.data['reason'];
		this.data['templates'] = templates;
		this.data['isSuccess'] = isSuccess;
		this.data['reason'] = reason;
		if(!isSuccess){
			_.delay(function(){
				Reactman.PageAction.showHint('error', reason);
			},500)
		}else{
			this.data['canPrint'] = true;
		}
		this.__emitChange();
		
	},

	handleCanPrintTrue: function(action){
		var isSuccess = this.data.isSuccess;
		var reason = this.data.reason;
		if(!isSuccess){
			_.delay(function(){
				Reactman.PageAction.showHint('error', reason);
			},500)
		}else{
			this.data['canPrint'] = action.data.canPrint;
		}
		this.__emitChange();
	},

	handleCanPrintFalse: function(action){
		this.data['canPrint'] = action.data.canPrint;
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;