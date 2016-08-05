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
			actionType: Constant.BUSINESS_DATAS_FILTER,
			data: filterOptions
		});
	},

	changeBusinessStatus: function(id) {
		Resource.post({
			resource: 'business.manager',
			data: {
				id: id
			},
			success: function() {
				Reactman.PageAction.showHint('success', '通过审核成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.BUSINESS_DATAS_FILTER,
						data: {}
					});
				},1000);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	},
	
	updateBusinessStatus: function(filterOptions) {
		Dispatcher.dispatch({
			actionType: Constant.BUSINESS_DATAS_FILTER,
			data: {}
		});
	},
	
	deleteBusiness: function(id) {
		Resource.delete({
			resource: 'business.manager',
			data: {
				id: id
			},
			success: function() {
				Reactman.PageAction.showHint('success', '删除成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.UPDATE_BUSINESS_APPLY,
						data: {}
					});
				},1000);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	},
};

module.exports = Action;