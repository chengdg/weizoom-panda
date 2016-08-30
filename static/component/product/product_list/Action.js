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
	},

	ProductCategory: function(){
		Resource.get({
			resource: 'product.category',
			data: {},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_LIST_CATEGORY
			}
		});
	},

	changeSecondLevel: function(first_id){
		Resource.get({
			resource: 'product.second_category',
			data: {
				'first_id': first_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_SECOND_CATEGORY
			}
		});
	},

	chooseSecondLevel: function(second_id){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_CHOOSE_SECOND_CATEGORY,
			data: {
				'second_id': second_id
			}
		});
	},

	lookProductModelDetail: function(product_id){
		Resource.get({
			resource: 'product.model_details',
			data: {
				'product_id': product_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_MODEL_DETAILS
			}
		});
	},

	plusProductStore: function(){
		Dispatcher.dispatch({
			actionType: Constant.PLUS_PRODUCT_STORE,
			data: {}
		});
	}
};

module.exports = Action;