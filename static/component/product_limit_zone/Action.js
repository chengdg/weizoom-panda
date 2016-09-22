/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateLimitZoneTemplates: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.LIMIT_ZONE_TEMPLATE_UPDATE,
			data: {}
		});
	},

	updateLimitZoneTemplateInfo: function(selectedDatas, selectedIds, event){
		Reactman.Resource.post({
			resource: 'product_limit_zone.template',
			data: {
				name: event.props['data-name'],
				id: event.props['data-id'],
				selected_data: JSON.stringify(selectedDatas),
				flag: 'provinces'
			},
			success: function() {
				Reactman.PageAction.showHint('success', '保存成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.LIMIT_ZONE_TEMPLATE_UPDATE,
						data: {}
					});
				},500);
			},
			error: function() {
				Reactman.PageAction.showHint('error', '保存失败！');
			},
			scope: this
		});

	},

	deleteLimitZone: function(id) {
		Resource.delete({
			resource: 'product_limit_zone.template',
			data: {
				id: id
			},
			success: function() {
				Reactman.PageAction.showHint('success', '删除成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.LIMIT_ZONE_TEMPLATE_UPDATE,
						data: {}
					});
				},500);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	}
};

module.exports = Action;