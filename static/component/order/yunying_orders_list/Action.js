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
	}
};

module.exports = Action;