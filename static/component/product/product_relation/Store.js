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
		'handleProductRelationDataFilter': Constant.PRODUCT_RELATION_DATAS_FILTER,
		'handleDeleteProductRelationWeapp': Constant.DELETE_PRODUCT_RELATION_WEAPP,
		'handleChooseSelfShop': Constant.CHOOSE_SELF_SHOP,
		'handleGetHasSyncShop': Constant.GET_HAS_SYNC_SHOP,
		'handleChooseAllSelfShop': Constant.CHOOSE_ALL_SELF_SHOP
	},

	init: function() {
		var selfShop = [{
			'name': '微众白富美',
			'value': 'weizoom_baifumei'
		},{
			'name': '微众俱乐部',
			'value': 'weizoom_club'
		},{
			'name': '微众家',
			'value': 'weizoom_jia'
		},{
			'name': '微众妈妈',
			'value': 'weizoom_mama'
		},{
			'name': '微众商城',
			'value': 'weizoom_shop'
		},{
			'name': '微众学生',
			'value': 'weizoom_xuesheng'
		},{
			'name': '微众Life',
			'value': 'weizoom_life'
		},{
			'name': '微众一家人',
			'value': 'weizoom_yjr'
		},{
			'name': '惠惠来啦',
			'value': 'weizoom_fulilaile'
		}]
		this.filter = {};
		this.data = {};
		this.data.selfShop = selfShop;
		this.data.selectSelfShop = []
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

	handleDeleteProductRelationWeapp: function(action){
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '取消成功');
		}, 10);
		this.__emitChange();
	},

	handleChooseSelfShop: function(action){
		var selectSelfShop = this.data.selectSelfShop;
		var value = action.data.value;
		var is_choosed = true;
		for(var index in selectSelfShop){
			if(selectSelfShop[index]==value){
				is_choosed = false;
				selectSelfShop.splice(index,1);
			}
		}
		if(is_choosed){
			selectSelfShop.push(value);
		}
		this.data.selectSelfShop = selectSelfShop;
		this.__emitChange();
	},

	handleGetHasSyncShop: function(action){
		console.log(action.data,'+=========')
		this.data.selectSelfShop = action.data.self_user_name;
		this.data['product_info'] = action.data.product_info;
		this.__emitChange();
	},

	handleChooseAllSelfShop: function(){
		var selectSelfShop = this.data.selectSelfShop;
		console.log(selectSelfShop.length,'++++==')
		if(selectSelfShop.length==9){
			selectSelfShop = []
		}else{
			selectSelfShop = ['weizoom_baifumei','weizoom_club','weizoom_jia','weizoom_mama','weizoom_shop','weizoom_xuesheng','weizoom_life','weizoom_yjr','weizoom_fulilaile'];
		}	
		this.data.selectSelfShop = selectSelfShop;
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