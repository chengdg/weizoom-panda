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
		'handleUpdateProduct': Constant.PRODUCT_LIST_UPDATE_PRODUCT,
		'handleProductDataFilter': Constant.PRODUCT_DATAS_FILTER
	},

	init: function() {
		this.data = {};
		this.data.user_has_products = '';
		this.filter = {};
	},

	handleUpdateProduct: function(action) {
		this.data.user_has_products = parseInt(action.data.user_has_products)-1;
		this.__emitChange();
	},

	handleProductDataFilter: function(action){
		this.filter = action.data;
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