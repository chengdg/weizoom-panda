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
		'handleRevokeProduct': Constant.PRODUCT_PRODUCT_RELATION_REVOKE_PRODUCT,
		'handleProductRelationDataFilter': Constant.PRODUCT_RELATION_DATAS_FILTER,
		'handleDeleteProductRelationWeapp': Constant.DELETE_PRODUCT_RELATION_WEAPP,
		'handleChooseSelfShop': Constant.CHOOSE_SELF_SHOP,
		'handleGetHasSyncShop': Constant.GET_HAS_SYNC_SHOP,
		'handleChooseAllSelfShop': Constant.CHOOSE_ALL_SELF_SHOP,
		'handleCancleSelectSyncProduct': Constant.CANCLE_SELECT_SYNC_PRODUCT,
		'handleDeleteProduct': Constant.PRODUCT_LIST_DELETE_PRODUCT,
		'handleInitAllSelfShops': Constant.INIT_ALL_SELF_SHOPS,
		'handleUpdateDatas': Constant.PRODUCT_PRODUCT_RELATION_UPDATE_DATAS
	},

	init: function() {
		this.filter = {};
		this.data = {
			'selectSelfShop': [],
			'product_info': {}
		};
	},

	handleInitAllSelfShops: function(action) {
		this.data['selfShop'] = action.data.rows;
		this.data['allSelfShop'] = action.data.allSelfShopsValue;
		this.__emitChange();
	},
	
	handleUpdateDatas: function(){
		this.__emitChange();
	},

	handleProductRelationWeapp: function(action) {
		if(action.data['code']==200){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', action.data.errMsg);
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', action.data.errMsg);
			}, 10);
		}

		this.__emitChange();
	},

	handleRevokeProduct: function(action) {
		if(action.data['code']==200){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '撤回成功');
			}, 10);
		}else{
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', '撤回失败');
			}, 10);
		}

		this.__emitChange();
	},

	handleProductRelationDataFilter: function(action){
		this.data.filterOptions = action.data;
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
		var isChoosed = true;

		for(var index in selectSelfShop){
			if(selectSelfShop[index]==value){
				isChoosed = false;
				selectSelfShop.splice(index,1);
			}
		}

		if(isChoosed){
			selectSelfShop.push(value);
		}

		this.data.selectSelfShop = selectSelfShop;
		this.__emitChange();
	},

	handleGetHasSyncShop: function(action){
		// this.data['product_info'] = action.data.product_info;
		this.data['selectSelfShop'] = action.data.self_user_name;
		this.__emitChange();
	},

	handleChooseAllSelfShop: function(action){
		var selectSelfShop = this.data.selectSelfShop;
		var allSelfShop = this.data.allSelfShop;
		if(selectSelfShop.length == this.data.selfShop.length){
			selectSelfShop = [];
		}else{
			selectSelfShop = allSelfShop;
		}
		this.data.selectSelfShop = selectSelfShop;
		this.__emitChange();
	},

	handleCancleSelectSyncProduct: function(){
		this.data.selectSelfShop = [];
		this.__emitChange();
	},

	handleDeleteProduct: function(){
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '删除成功!');
		}, 10);
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.data.filterOptions;
	}
});

module.exports = Store;