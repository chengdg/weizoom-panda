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
	saveNewProduct: function(data) {
		var product = {
			product_name: data['product_name'],
			promotion_title: data['promotion_title'],
			product_price: data['product_price'],
			clear_price: data['clear_price'],
			product_weight: data['product_weight'],
			product_store: data['product_store'],
			product_store_type: data['product_store_type'],
			has_limit_time: data['has_limit_time'][0],
			limit_clear_price: data['limit_clear_price'].trim(),
			valid_time_from: data['valid_time_from'],
			valid_time_to: data['valid_time_to'],
			images: JSON.stringify(data['images']),
			remark: data['remark']
		};
		if (data.id === -1) {
			Resource.put({
				resource: 'product.new_product',
				data: product,
				success: function() {
					Dispatcher.dispatch({
						actionType: Constant.NEW_PRODUCT_CREATE,
						data: data
					});
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMg);
				}
			});
		} else {
			product['id'] = data.id;
			Resource.post({
				resource: 'product.new_product',
				data: product,
				success: function() {
					Dispatcher.dispatch({
						actionType: Constant.NEW_PRODUCT_CREATE,
						data: data
					});
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMg);
				}
			});
		}		

		
	},

	updateProduct: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.NEW_PRODUCT_UPDATE_PRODUCT,
			data: {
				property: property,
				value: value
			}
		});
	},
};

module.exports = Action;