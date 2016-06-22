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
	getWeappProductRelation: function(product_id) {
		Resource.get({
			resource: 'product.weapp_relation',
			data: {
				'product_id': product_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_RELATION_WEAPP
			}
		});
	},

	updateProductRelation: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_RELATION_UPDATE,
			data: {
				property: property,
				value: value
			}
		});
	},

	saveProductRelation: function(data,product_id){
		var relation = [];
		relation.push(data)
		Resource.put({
			resource: 'product.weapp_relation',
			data: {
				relations: JSON.stringify(relation),
				product_id: product_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_RELATION_WEAPP_SAVE
			}
		});
	},

	filterDates: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_RELATION_DATAS_FILTER,
			data: filterOptions
		});
	},

	relationFromWeapp: function(product_data){
		Resource.get({
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