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
		'handleAddProductModelValue': Constant.ADD_PRODUCT_MODEL_VALUE,
		'handleCreateNewProductModel': Constant.NEW_PRODUCT_MODEL,
		'handleUpdateProductModel': Constant.UPDATE_PRODUCT_MODEL,
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

	handleCreateNewProductModel: function(action){
		console.log(action.data,"--------");
		this.__emitChange();
	},

	handleUpdateProductModel: function(action){
		console.log(action.data,"---22-----");
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