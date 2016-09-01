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

	saveProductModelValue: function(model_id,model_value,path){
		Resource.put({
			resource: 'product.product_model_value',
			data: {
				'model_id':model_id,
				'model_value':model_value,
				'path':path	
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.NEW_PRODUCT_MODEL_VALUE
			}
		});
	},

	deleteProductModelValue:function(value_id){
		Resource.delete({
			resource: 'product.product_model_value',
			data: {
				'value_id':value_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.DELETE_PRODUCT_MODEL_VALUE
			}
		});
	},

	addLabelProperty: function(filterOptions){
		Resource.put({
			resource: 'label.label_manager',
			data: {},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.LABEL_LABEL_MANAGER_ADD_LABEL_PROPERTY
			}
		});
	},

	updateLabelProperty: function(id,name){
		Resource.post({
			resource: 'label.label_manager',
			data: {
				'label_id':id,
				'name':name
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_PROPERTY
			}
		});
	},

	deleteProductModel:function(model_id){
		Resource.delete({
			resource: 'product.product_model',
			data: {
				'model_id':model_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.DELETE_PRODUCT_MODEL
			}
		});
	},

	updateProductModelType: function(model_id,model_type){
		Resource.post({
			resource: 'product.product_model',
			data: {
				'model_id':model_id,
				'model_type':model_type
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.UPDATE_PRODUCT_MODEL
			}
		});
	},

	clearProductModelValue: function(){
		Dispatcher.dispatch({
			actionType: Constant.CLEAR_PRODUCT_MODEL_VALUE,
			data: {}
		});
	}
};

module.exports = Action;