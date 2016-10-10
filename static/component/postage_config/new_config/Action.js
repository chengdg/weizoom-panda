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
	savePostage: function(data){
		var postageName = data['postageName'] || '';
		var defaultPostages = data['defaultPostages'] || [];
		var specialPostages = data['specialPostages'] || [];
		var freePostages = data['freePostages'] || [];

		Resource.put({
			resource: 'postage_config.new_config',
			data: {
				postage_name: postageName,
				default_postages: JSON.stringify(defaultPostages),
				special_postages: JSON.stringify(specialPostages),
				free_postages: JSON.stringify(freePostages)
			},
			success: function() {
				Reactman.PageAction.showHint('success', '保存成功！');
				_.delay(function(){
					Dispatcher.dispatch({
						actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_SAVE_POSTAGE,
						data: data
					});
				},500)
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', "保存失败！");
			}
		})
	},

	updateConfig: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_CONFIG,
			data: {
				property: property,
				value: value
			}
		});
	},

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

	updateCondition: function(condition, index){
		Dispatcher.dispatch({
			actionType: Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_CONDITION,
			data: {
				condition: condition,
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
	}
};

module.exports = Action;