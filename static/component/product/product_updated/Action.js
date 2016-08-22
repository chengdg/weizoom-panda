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
	filterDatas: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_DATAS_FILTER,
			data: filterOptions
		});
	},

	updateSyncProduct: function(product_id){
		Resource.post({
			resource: 'product.sync_product',
			data: {
				'product_id': product_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.UPDATE_SYNC_PRODUCT
			}
		});
	}
};

module.exports = Action;