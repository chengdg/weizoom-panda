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
var W = Reactman.W;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateProduct': Constant.NEW_PRODUCT_UPDATE_PRODUCT,
		'handleCreateNewProduct': Constant.NEW_PRODUCT_CREATE,
	},

	init: function() {
		this.data = Reactman.loadJSON('product');
		
		if (this.data) {
			this.data['product_store_type'] = this.data['product_store'] > -1 ? '1' : '0';
		} else {
			this.data = {
				'id':-1,
				'images':[],
				'remark': '',
				'product_store_type':'0'
			};
		}
	},

	handleUpdateProduct: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleCreateNewProduct: function(action) {
		W.gotoPage('/product/product_list/');
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;