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
		// 'handleProductCategory': Constant.PRODUCT_LIST_CATEGORY,
		// 'handleProductSecondCategory': Constant.PRODUCT_SECOND_CATEGORY,
		// 'handleProductChooseSecondCategory': Constant.PRODUCT_CHOOSE_SECOND_CATEGORY
	},

	init: function() {
		this.data = {};
		this.data.user_has_products = '';
		this.filter = {};
		this.category = {};
		this.data.first_levels = '';
		this.data.second_levels = '';
		this.data.first_id = 0;
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

	// handleProductCategory: function(action){
	// 	this.category['first_levels'] = JSON.parse(action.data['first_levels']);
	// 	this.category['second_levels'] = JSON.parse(action.data['second_levels']);
	// 	console.log(action.data['first_levels'],"===11====")
	// 	this.__emitChange();
	// },

	// handleProductSecondCategory: function(action){
	// 	var first_levels = this.category['first_levels'];
	// 	console.log(first_levels,"===22222====");
	// 	var first_id = action.data['first_id'];
	// 	_.each(first_levels, function(first_level) {
	// 		console.log(first_level,"-----");
	// 		console.log(first_level['id'],first_id,"-----");
	// 		if(first_level['id']==first_id){
	// 			first_level['is_choose'] = 1;
	// 		}else{
	// 			first_level['is_choose'] = 0;
	// 		}
	// 	});
	// 	this.category['first_levels'] = first_levels;
	// 	console.log(first_levels,"===22222====");
	// 	this.category['second_levels'] = JSON.parse(action.data['second_levels']);
		
	// 	this.__emitChange();
	// },

	// handleProductChooseSecondCategory: function(action){
	// 	var second_levels = this.category['second_levels'];
	// 	var second_id = action.data.second_id;
	// 	_.each(second_levels, function(second_level) {
	// 		console.log(second_level,"-----");
	// 		console.log(second_level['id'],second_id,"-----");
	// 		if(second_level['id']==second_id){
	// 			second_level['is_choose'] = 1;
	// 		}else{
	// 			second_level['is_choose'] = 0;
	// 		}
	// 	});
	// 	this.__emitChange();
	// },

	// getCategory: function() {
	// 	return this.category;
	// },

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.filter;
	}
});

module.exports = Store;