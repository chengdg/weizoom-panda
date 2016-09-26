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
	},

	updateReason: function(property, value){
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_UNPASS_REASON,
			data: {
				property: property,
				value: value
			}
		});
	},

	chooseUnpassReason: function(reason){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_UNPASS_REASON,
			data: {
				reason: reason
			}
		});
	},

	refused: function(productId, reasons){
		Resource.post({
			resource: 'product.product_updated',
			data: {
				reasons: reasons,
				product_id: productId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_REFUSED
			}
		});
	},

	cancleChecked: function(){
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_UNDATE_CANCLE_CHECKED,
			data: {}
		});
	}
};

module.exports = Action;