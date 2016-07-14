/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	filterDates: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_RELATION_DATAS_FILTER,
			data: filterOptions
		});
	},

	relationFromWeapp: function(product_data){
		Resource.post({
			resource: 'product.weapp_relation',
			data: {
				'product_data': product_data
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_RELATION_WEAPP
			}
		});
	}
};

module.exports = Action;