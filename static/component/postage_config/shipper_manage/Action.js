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
	updateShipperMessages: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_MESSAGES,
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

	updateTable: function(){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_SHIPPER_MANAGE_UPDATE_TABLE,
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
	}
};

module.exports = Action;