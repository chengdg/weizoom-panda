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
		'handleProductDataFilter': Constant.PRODUCT_DATAS_FILTER,
		'handleProductDataExport': Constant.PRODUCT_DATAS_EXPORT,
		'handleProductCategory': Constant.PRODUCT_LIST_CATEGORY
	},

	init: function() {
		this.data = {};
		this.data.user_has_products = '';
		this.filter = {};
		this.category = {};
		this.data.first_levels = '';
		this.data.second_levels = '';
	},

	handleUpdateProduct: function(action) {
		this.data.user_has_products = parseInt(action.data.user_has_products)-1;
		this.__emitChange();
	},

	handleProductDataFilter: function(action){
		this.filter = action.data;
		this.__emitChange();
	},

	handleProductDataExport: function(action){
		var filterOptions = this.filter;
		var filter_str = '';
		for (var key in filterOptions){
			filter_str = key +'=' + filterOptions[key];
		}
		window.location.href = '/product/product_exported/?'+filter_str;
	},

	handleProductCategory: function(action){
		this.category['first_levels'] = action.data['first_levels'];
		this.category['second_levels'] = action.data['second_levels'];
		console.log(action.data['first_levels'],"===11====")
		this.__emitChange();
	},

	getCategory: function() {
		return this.category;
	},

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.filter;
	}
});

module.exports = Store;