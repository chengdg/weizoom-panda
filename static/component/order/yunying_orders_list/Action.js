/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.yunying_orders_list:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	filterOrders: function(filterOptions) {
		Dispatcher.dispatch({
			actionType: Constant.FILTER_ORDERS,
			data: filterOptions
		});
	},
	exportOrders: function(){
		Dispatcher.dispatch({
			actionType: Constant.ORDER_DATAS_EXPORT,
			data: {}
		});
	},
	getAllSyncedSelfShops: function(){
		Resource.get({
			resource: 'self_shop.get_all_synced_self_shops',
			data: {
				'is_for_search': true
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.INIT_ALL_SELF_SHOPS
			}
		})
	}
};

module.exports = Action;