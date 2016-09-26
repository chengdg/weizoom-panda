/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleProductDataFilter': Constant.PRODUCT_DATAS_FILTER,
		'handleUpdateSyncProduct': Constant.UPDATE_SYNC_PRODUCT,
		'handleProductRefused': Constant.PRODUCT_REFUSED
	},

	init: function() {
		this.data = {
			'reasons': [],
			'custom_reason': ''
		};
	},

	handleProductDataFilter: function(action){
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	handleUpdateSyncProduct: function(action){
		if(action.data['code']==200){
			//更新二级导航栏的数字
			var updateSyncCount = action.data['count'];
			var str = '\\((.| )+?\\)';
			var afterSyncCount = parseInt($('.xui-secondNav >ul >li:nth-child(2) span').text().match(str)[1])-parseInt(updateSyncCount);
			if(afterSyncCount > 0){
				$('.xui-secondNav >ul >li:nth-child(2) span').text('商品更新('+afterSyncCount+')')
			}else{
				$('.xui-secondNav >ul >li:nth-child(2) span').text('商品更新')
			}
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '更新成功');
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', '更新失败');
			}, 10);
		}
		this.__emitChange();
	},

	handleProductRefused: function(action){
		if(action.data['code']==200){
			this.data.reasons = [];
			this.data.custom_reason = '';
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '驳回成功');
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', '驳回失败');
			}, 10);
		}
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.data.filterOptions;
	}
});

module.exports = Store;