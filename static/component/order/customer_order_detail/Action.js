/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_order_detail:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	saveProduct: function(orderId) {
		Resource.get({
			resource: 'order.customer_order_detail',
			data: {
				order_id: orderId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.ORDER_DATA_SAVE_PRODUCT
			}
		});
	}
};

module.exports = Action;