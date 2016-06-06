/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_orders_list:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {

	filterOrders: function(filterOptions) {
		if(filterOptions.hasOwnProperty('__f-order_create_at-range')){
			var low = $('#order_create_at_low').val();
			var high = $('#order_create_at_high').val();
			if (low && high){
				Dispatcher.dispatch({
					actionType: Constant.ORDER_DATAS_FILTER_ORDERS,
					data: filterOptions
				});
			}else{
				Reactman.PageAction.showHint('error', '请输入完整的筛选日期');
			}
		}else{
			Dispatcher.dispatch({
				actionType: Constant.ORDER_DATAS_FILTER_ORDERS,
				data: filterOptions
			});
		}
	},

	//updateProduct: function(product, field, data) {
	//	Dispatcher.dispatch({
	//		actionType: Constant.OUTLINE_DATAS_UPDATE_PRODUCT,
	//		data: {
	//			product: product,
	//			field: field,
	//			data: data
	//		}
	//	});
	//}
};

module.exports = Action;