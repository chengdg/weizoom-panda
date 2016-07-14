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
		'handleProductRelationDataFilter': Constant.PRODUCT_RELATION_DATAS_FILTER
	},

	init: function() {
		this.data = {};
		this.filter = {};
	},

	handleProductRelationWeapp: function(action) {
		this.data = action.data.rows;
		if(action.data['code']==200){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', action.data.errMsg);
			}, 10);
			this.__emitChange();
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', action.data.errMsg);
			}, 10);
		}
	},

	handleProductRelationDataFilter: function(action){
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