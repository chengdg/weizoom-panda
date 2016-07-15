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
	deleteProduct: function(id,user_has_products) {
		Resource.delete({
			resource: 'product.new_product',
			data: {
				id: id,
				user_has_products: user_has_products
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_LIST_UPDATE_PRODUCT
			}
		});
	},

	filterDates: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_DATAS_FILTER,
			data: filterOptions
		});
	},

	exportProducts: function(){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_DATAS_EXPORT,
			data: {}
		});
	}
};

module.exports = Action;