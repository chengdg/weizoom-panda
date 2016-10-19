/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:self_shop.manage:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateData: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_DATA,
			data: {
				property: property,
				value: value
			}
		});
	},

	updateArea: function(selectedIds){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_AREA,
			data: {
				selectedIds: selectedIds
			}
		});
	},

	updateAccountTable: function(){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_ACCOUNT_TABLE,
			data: {}
		});
	},

	updateShipperTable: function(){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_SHIPPER_TABLE,
			data: {}
		});
	},

	changeTable: function(status){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_CHANGE_TABLE,
			data: {
				status: status
			}
		});
	},

	getShipperData: function(shipperId){
		Resource.get({
			resource: 'postage_config.shipper',
			data: {
				'shipper_id': shipperId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_GET_DATA
			}
		});
	},

	deleteShipper: function(shipperId){
		Resource.delete({
			resource: 'postage_config.shipper',
			data: {
				'shipper_id': shipperId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_DELETE_SHIPPER
			}
		});
	},

	getExpressBillAccount: function(expressId){
		Resource.get({
			resource: 'postage_config.express_bill',
			data: {
				'express_id': expressId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_GET_DATA
			}
		});
	},

	deleteExpressBillAccount: function(expressId){
		Resource.delete({
			resource: 'postage_config.express_bill',
			data: {
				'express_id': expressId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_DELETE_EXPRESS_ACCOUNT
			}
		});
	},

	clearData: function(){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_CLEAR_DATA,
			data: {}
		});
	}
};

module.exports = Action;