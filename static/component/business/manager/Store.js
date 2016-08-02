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
		'handleBusinessDataFilter': Constant.BUSINESS_DATAS_FILTER,
		'handleUpdateBusinessApply': Constant.UPDATE_BUSINESS_APPLY
	},

	init: function() {
		this.data = {};
	},

	handleBusinessDataFilter: function(action){
		this.data = action.data;
		this.__emitChange();
	},

	handleUpdateBusinessApply: function(action) {
		this.__emitChange();
	},
	
	getFilter: function() {
		return this.data;
	}
});

module.exports = Store;