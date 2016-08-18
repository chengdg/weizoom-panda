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
	saveNewProduct: function(data,model_values) {
		var limit_clear_price = data.hasOwnProperty('limit_clear_price')?data['limit_clear_price'].trim():'';
		var product = {
			product_name: data['product_name'],
			promotion_title: data['promotion_title'],
			product_price: data['product_price'],
			clear_price: data['clear_price'],
			product_weight: data['product_weight'],
			product_store: data['product_store'],
			product_store_type: data['product_store_type'],
			has_limit_time: data['has_limit_time'][0],
			limit_clear_price: limit_clear_price,
			valid_time_from: data['valid_time_from'],
			valid_time_to: data['valid_time_to'],
			images: JSON.stringify(data['images']),
			remark: data['remark'],
			has_product_model: data['has_product_model'],
			model_values: model_values,
			second_level_id: data['second_level_id']
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

	addProductModelValue: function(value_id){
		Dispatcher.dispatch({
			actionType: Constant.NEW_PRODUCT_ADD_PRODUCT_MODEL,
			data: {
				value_id: value_id
			}
		});
	},

	saveModelValue: function(value_ids){
		Resource.get({
			resource: 'product.product_has_model',
			data: {
				'value_ids':value_ids.join(',')
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.SAVE_PRODUCT_MODEL_VALUE
			}
		});
	},

	deleteModelValue: function(modelId){
		Dispatcher.dispatch({
			actionType: Constant.DELETE_PRODUCT_MODEL_VALUE,
			data: {
				modelId: modelId
			}
		});
	},

	cancleValidTime: function(modelId){
		Dispatcher.dispatch({
			actionType: Constant.CANCLE_VALIDATA_TIME,
			data: {
				modelId: modelId
			}
		});
	},

	ProductCategory: function(second_level_id){
		Resource.get({
			resource: 'product.category',
			data: {
				second_level_id: second_level_id
			},
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

	cancleChooseCatalog: function(){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_CANCLE_CHOOSE_CATALOG,
			data: {}
		});
	},

	saveChooseCatalog: function(catalogName){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_SAVE_CHOOSE_CATALOG,
			data: {
				'catalogName': catalogName
			}
		});
	}
};

module.exports = Action;