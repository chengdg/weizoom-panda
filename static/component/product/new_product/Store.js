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
		'handleNewProductAddModel': Constant.NEW_PRODUCT_ADD_PRODUCT_MODEL,
		'handleSaveProductAddModel': Constant.SAVE_PRODUCT_MODEL_VALUE,
	},

	init: function() {
		this.data = Reactman.loadJSON('product');
		this.model_value = {}
		if (this.data) {
			this.data['product_store_type'] = this.data['product_store'] > -1 ? '0' : '-1';
			this.data['product_store'] = this.data['product_store'] == -1 ? '' : String(this.data['product_store']);
		} else {
			this.data = {
				'id':-1,
				'images':[],
				'remark': '',
				'product_store_type':'-1',
				'has_product_model': '0',
				'has_limit_time': '0',
				'value_ids': []
			};
		}
	},

	handleUpdateProduct: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleNewProductAddModel: function(action){
		var value_id = action.data.value_id;
		var value_ids = this.data['value_ids'];
		if(value_ids.indexOf(value_id)!=-1){
			for(var index in value_ids){
				if (value_ids[index] == value_id){
					value_ids.splice(index,1);
				}
			}
		}else{
			this.data['value_ids'].push(action.data.value_id);
		}
		this.__emitChange();
	},

	handleSaveProductAddModel: function(action){
		console.log(action.data.rows,"=======");
		this.model_value= action.data.rows;
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