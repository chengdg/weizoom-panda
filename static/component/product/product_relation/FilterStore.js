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
		'handleProductRelationDataFilter': Constant.PRODUCT_RELATION_DATAS_FILTER
	},

	init: function() {
		this.filter = {};
	},

	handleProductRelationDataFilter: function(action){
		this.filter = action.data;
		this.__emitChange();
	},

	getFilter: function() {
		return this.filter;
	}
});

module.exports = Store;