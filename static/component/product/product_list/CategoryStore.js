/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var CategoryStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleProductCategory': Constant.PRODUCT_LIST_CATEGORY,
		'handleProductSecondCategory': Constant.PRODUCT_SECOND_CATEGORY,
		'handleProductChooseSecondCategory': Constant.PRODUCT_CHOOSE_SECOND_CATEGORY
	},

	init: function() {
		this.category = {};
		this.category['second_id'] = 0;
	},

	handleProductCategory: function(action){
		var first_levels = JSON.parse(action.data['first_levels']);
		var second_levels = JSON.parse(action.data['second_levels']);
		first_levels[0]['is_choose'] = 1;
		second_levels[0]['is_choose'] = 1;
		this.category['first_levels'] = first_levels;
		this.category['second_levels'] = second_levels;
		this.category['second_id'] = second_levels[0].id;
		this.__emitChange();
	},

	handleProductSecondCategory: function(action){
		var first_levels = this.category['first_levels'];
		var first_id = action.data['first_id'];
		_.each(first_levels, function(first_level) {
			if(first_level['id']==first_id){
				first_level['is_choose'] = 1;
			}else{
				first_level['is_choose'] = 0;
			}
		});
		this.category['first_levels'] = first_levels;
		this.category['second_id'] = 0;
		var second_levels = action.data['second_levels'].length>0?JSON.parse(action.data['second_levels']):''
		this.category['second_levels'] = second_levels;
		
		this.__emitChange();
	},

	handleProductChooseSecondCategory: function(action){
		var second_levels = this.category['second_levels'];
		var second_id = action.data.second_id;
		_.each(second_levels, function(second_level) {
			if(second_level['id']==second_id){
				second_level['is_choose'] = 1;
			}else{
				second_level['is_choose'] = 0;
			}
		});
		this.category['second_id'] = second_id;
		this.__emitChange();
	},

	getCategory: function() {
		return this.category;
	}
});

module.exports = CategoryStore;