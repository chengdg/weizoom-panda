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
var AddProductModelDialog = require('./AddProductModelDialog.react');
var W = Reactman.W;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleNewProductAddModel': Constant.NEW_PRODUCT_ADD_PRODUCT_MODEL
	},

	init: function() {
		var _this = this;
		this.data = Reactman.loadJSON('product');
		if (this.data) {
			var dataStrArr=this.data['value_ids'].split(",");//分割成字符串数组  
			var dataIntArr=[];//保存转换后的整型字符串  
			dataStrArr.forEach(function(data,index,arr){  
				dataIntArr.push(+data);
			});
			this.data['value_ids'] = dataIntArr;
		} else {
			this.data = {
				'value_ids': []
			};
		}
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

	getData: function() {
		return this.data;
	}
});

module.exports = Store;