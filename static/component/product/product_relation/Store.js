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
		'handleProductRelationWeapp': Constant.PRODUCT_RELATION_WEAPP,
		'handleProductRelationUpdate': Constant.PRODUCT_RELATION_UPDATE,
		'handleProductRelationSave': Constant.PRODUCT_RELATION_WEAPP_SAVE
	},

	init: function() {
		this.data = {};
	},

	handleProductRelationWeapp: function(action) {
		this.data = action.data.rows;
		this.__emitChange();
	},

	handleProductRelationUpdate: function(action){
		console.log(action.data.value,"-----------");
		console.log(action.data.property,"2222222");
		var name = action.data.property;
		var value = action.data.value;
		console.log(this.data);
		this.data[name] = value;
		console.log("==========");
		this.__emitChange();
	},

	handleProductRelationSave: function(action){
		if(action.data.code == 200){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', action.data.Msg);
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', action.data.Msg);
			}, 10);
		}
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;