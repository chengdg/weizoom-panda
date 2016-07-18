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
	addProductModelValue: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.ADD_PRODUCT_MODEL_VALUE,
			data: {
				property: property,
				value: value
			}
		});
	},

	addProductModel: function(filterOptions){
		Resource.put({
			resource: 'product.product_model',
			data: {},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.NEW_PRODUCT_MODEL
			}
		});
	},

	updateProductModel: function(id,name){
		Resource.post({
			resource: 'product.product_model',
			data: {
				'id':id,
				'name':name
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.UPDATE_PRODUCT_MODEL
			}
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