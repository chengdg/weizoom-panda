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

	getOrderShipInformations: function(orderId) {
		Resource.get({
			resource: 'order.order_ship_informations',
			data: {
				'order_id': orderId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.ORDER_SHIP_INFORMATIONS
			}
		});
	},

	updateOrderShipInformations: function() {
		Dispatcher.dispatch({
			actionType: Constant.ORDER_DATAS_FILTER_ORDERS,
			data: {}
		});
	},

	completeOrder: function(orderId) {
		Resource.post({
			resource: 'order.order_complete_ship',
			data: {
				order_id: orderId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.ORDER_DATAS_FILTER_ORDERS
			}
		});
	},

	exportOrders: function(){
		Dispatcher.dispatch({
			actionType: Constant.ORDER_DATAS_EXPORT,
			data: {}
		});
	}
};

module.exports = Action;