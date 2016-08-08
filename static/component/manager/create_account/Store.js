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
		'handleUpdateAccount': Constant.NEW_ACCOUNT_UPDATE_ACCOUNT,
		'handleCreateNewAccount': Constant.NEW_ACCOUNT_CREATE,
		'handleSelect':Constant.NEW_ACCOUNT_SELECT_CATALOG,
		'handleAddSelfShop':Constant.ADD_SELF_SHOP,
		'handleDeleteSelfShop':Constant.DELETE_SELF_SHOP,
		'handleAddRebateDialog':Constant.ADD_REBATE_DIALOG,
		'handleUpdateRebates':Constant.UPDATE_REBATES,
		'handleDeleteRebateValue':Constant.DELETE_REBATE_VALUE,
		'handleUpdateGroupPoiints':Constant.UPDATE_GROUP_POINTS
	},

	init: function() {
		this.data = Reactman.loadJSON('user_profile_data');
		if (this.data) {
			this.data['account_type'] = String(this.data['account_type']);
			this.data['self_user_names'] = this.data['self_user_names'].length>0?JSON.parse(this.data['self_user_names']): [];
			if (this.data['account_type'] == '1'){
				this.data['purchase_method'] = String(this.data['purchase_method']);
				this.data['company_type'] = JSON.parse(this.data['company_type']);
				this.data['options_for_type'] = [];
				if (this.data['purchase_method'] != '2'){
					this.data['points'] = '';
				}
				this.data['rebates'] = []
			}
		} else {
			this.data = {
				'id':-1,
				'account_type':'1',
				'purchase_method': '2',
				'company_type': [],
				'options_for_type': [],
				'self_user_names': [],
				'points': '',
				'rebates': []
			};
		}
	},

	handleSelect: function(action) {
		this.data['options_for_type'] = action.data.rows;
		this.__emitChange();
	},

	handleUpdateAccount: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleCreateNewAccount: function(action) {
		W.gotoPage('/manager/account/');
	},

	handleAddSelfShop: function(action){
		var selfUserName = action.data.self_user_name;

		var selfShop = this.data.self_user_names;
		var self_obj = {
			'self_user_name': selfUserName
		}
		selfShop.push(self_obj)
		self_obj[selfUserName+'_value'] = this.data.points;
		// this.data[selfUserName+'_value'] = this.data.points;
		this.data.self_user_names = selfShop;
		this.__emitChange();
	},

	handleDeleteSelfShop: function(action) {
		var selfShop = this.data.self_user_names;
		var index = action.data.index;
		selfShop.splice(index,1)
		this.data.self_user_names = selfShop;
		this.__emitChange();
	},

	handleAddRebateDialog: function(){
		var oldRebates = this.data.rebates;
		oldRebates.push({
			'validate_from_condition':'',
			'validate_to_condition':'',
			'order_money_condition': 1000,
			'rebate_proport_condition': 50,
			'default_rebate_proport_condition': 5
		})
		this.data.rebates = oldRebates;
		this.__emitChange();
	},

	handleUpdateRebates: function(action){
		var index = action.data.index;
		var property = action.data.property;
		var value = action.data.value;
		var oldRebates = this.data.rebates;
		oldRebates[index][property] = value;
		this.data.rebates = oldRebates;
		this.__emitChange();
	},

	handleDeleteRebateValue: function(action){
		var index = action.data.index;
		var oldRebates = this.data.rebates;
		oldRebates.splice(index,1)
		this.data.rebates = oldRebates;
		this.__emitChange();
	},

	handleUpdateGroupPoiints: function(action){
		var index = action.data.index;
		var property = action.data.property;
		var value = action.data.value;
		var selfUserName = this.data.self_user_names;
		selfUserName[index][property] = value;
		this.data.self_user_names = selfUserName;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;