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
		'handleAddSalePhone': Constant.ADD_SALE_PHONE,
		'handleSaveSalePhone': Constant.SAVE_SALE_PHONE
	},

	init: function() {
		this.data = {};
	},

	handleAddSalePhone: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleSaveSalePhone: function(action){
		if(action.data['code']==200){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '保存成功!');
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', '保存失败!');
			}, 10);
		}
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;