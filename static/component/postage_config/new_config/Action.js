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
	updateDefaultPostages: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_DEFAULT_POSTAGE,
			data: {
				property: property,
				value: value
			}
		});
	},

	updateSpecialPostages: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_POSTAGE,
			data: {
				property: property,
				value: value
			}
		});
	},

	updateFreePostages: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_FREE_POSTAGE,
			data: {
				property: property,
				value: value
			}
		});
	},

	updateFreeValues: function(property, value, index) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_FREE_VALUES,
			data: {
				property: property,
				value: value,
				index: index
			}
		});
	},

	updateSpecialValues: function(index, property, value){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_VALUES,
			data: {
				index: index,
				property: property,
				value: value
			}
		});
	},

	updateCondition: function(conditionValue, index){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_CONDITION,
			data: {
				conditionValue: conditionValue,
				index: index
			}
		});
	},

	updateSpecialArea: function(selectedIds, index){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_AREA,
			data: {
				selectedIds: selectedIds,
				index: index
			}
		});
	},

	updateFreeArea: function(selectedIds, index){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_FREE_AREA,
			data: {
				selectedIds: selectedIds,
				index: index
			}
		});
	},

	addSpecialPostage: function(){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_ADD_SPECIAL_POSTAGE,
			data: {}
		});
	},

	addFreePostage: function(){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_ADD_FREE_POSTAGE,
			data: {}
		});
	},

	deleteSpecialPostage: function(index){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_DELETE_SPECIAL_POSTAGE,
			data: {
				index: index
			}
		});
	},

	deleteFreePostage: function(index){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_DELETE_FREE_POSTAGE,
			data: {
				index: index
			}
		});
	},
};

module.exports = Action;