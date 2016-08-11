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
			actionType: Constant.PRODUCT_RELATION_DATAS_FILTER,
			data: filterOptions
		});
	},

	cancleChecked: function(product_id, self_names){
		Resource.delete({
			resource: 'product.weapp_relation',
			data: {
				'product_id': product_id,
				'self_names': self_names
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.DELETE_PRODUCT_RELATION_WEAPP
			}
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
	},

	getHasSyncShop: function(product_id){
		Resource.get({
			resource: 'product.weapp_relation',
			data: {
				'product_id': product_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.GET_HAS_SYNC_SHOP
			}
		});
	},

	chooseSelfShop: function(value){
		Dispatcher.dispatch({
			actionType: Constant.CHOOSE_SELF_SHOP,
			data: {
				value: value
			}
		});
	},

	chooseAllSelfShop: function(){
		Dispatcher.dispatch({
			actionType: Constant.CHOOSE_ALL_SELF_SHOP,
			data: {}
		});
	},

	cancleSelectSyncProduct: function(){
		Dispatcher.dispatch({
			actionType: Constant.CANCLE_SELECT_SYNC_PRODUCT,
			data: {}
		});
	}
};

module.exports = Action;