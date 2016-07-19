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
		'handleCreateNewProductModel': Constant.NEW_PRODUCT_MODEL,
		'handleUpdateProductModel': Constant.UPDATE_PRODUCT_MODEL,
		'handleDeleteProductModel': Constant.DELETE_PRODUCT_MODEL,

		'handleAddProductModelValue': Constant.ADD_PRODUCT_MODEL_VALUE,
		'handleCreateProductModelValue': Constant.NEW_PRODUCT_MODEL_VALUE,
		'handleDeleteProductModelValue': Constant.DELETE_PRODUCT_MODEL_VALUE,
		'handleClearProductModelValue': Constant.CLEAR_PRODUCT_MODEL_VALUE,
	},

	init: function() {
		this.data = {
			'images': [],
			'model_value': '',
		};
		this.filter = {};
	},

	handleAddProductModelValue: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleCreateProductModelValue: function(action){
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '添加成功');
		}, 10);
		
		this.__emitChange();
	},

	handleDeleteProductModelValue: function(action) {
		this.__emitChange();
	},

	handleCreateNewProductModel: function(action){
		this.__emitChange();
	},

	handleUpdateProductModel: function(action){
		this.__emitChange();
	},

	handleDeleteProductModel: function(action) {
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '删除成功');
		}, 10);
		this.__emitChange();
	},

	handleClearProductModelValue: function(){
		this.data = {
			'images': [],
			'model_value': '',
		};
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.filter;
	}
});

module.exports = Store;