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
		'handleSetFreightValue': Constant.SET_FREIGHT_VALUE,
		'handleSaveFreightmoney': Constant.SAVE_FREIGHT_MONEY
	},

	init: function() {
		this.data = {};
	},

	handleSetFreightValue: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleSaveFreightmoney: function(action) {
		if(action.data['code']==200){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '保存成功!');
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '保存失败!');
			}, 10);
		}
		console.log(action,"========");
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;