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
		'handleUpdateSyncProduct': Constant.UPDATE_SYNC_PRODUCT
	},

	init: function() {
		this.data = {};
	},

	handleProductDataFilter: function(action){
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	handleUpdateSyncProduct: function(action){
		if(action.data['code']==200){
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

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.data.filterOptions;
	}
});

module.exports = Store;