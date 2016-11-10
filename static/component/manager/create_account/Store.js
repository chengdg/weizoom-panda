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
		'handleSelect': Constant.NEW_ACCOUNT_SELECT_CATALOG,
		'handleAddSelfShop': Constant.ADD_SELF_SHOP,
		'handleDeleteSelfShop': Constant.DELETE_SELF_SHOP,
		'handleAddRebateDialog': Constant.ADD_REBATE_DIALOG,
		'handleUpdateRebates': Constant.UPDATE_REBATES,
		'handleDeleteRebateValue': Constant.DELETE_REBATE_VALUE,
		'handleUpdateGroupPoiints': Constant.UPDATE_GROUP_POINTS,
		'handleGetCompanyInfoFromAxe': Constant.GET_COMPANY_INFO_FROM_AXE
	},

	init: function() {
		this.data = Reactman.loadJSON('user_profile_data');
		if (this.data) {
			this.data['accountType'] = String(this.data['account_type']);
			if (this.data['accountType'] == '1'){
				this.data['companyName'] = this.data['company_name'];
				this.data['purchaseMethod'] = String(this.data['purchase_method']);
				this.data['companyType'] = JSON.parse(this.data['company_type']);
				this.data['optionsForType'] = [];
				this.data['companyNameOption'] = this.data['contacter']+'/'+this.data['phone'];
				this.data['optionsForCompanyName'] = [];
				this.data['validTimeFrom'] = this.data['valid_time_from'];
				this.data['validTimeTo'] = this.data['valid_time_to'];
				if (this.data['purchaseMethod'] != '2'){
					this.data['points'] = '';
				}
				if (this.data['purchaseMethod'] == '3'){
					this.data['orderMoney'] = this.data['order_money'];
					this.data['rebateProport'] = this.data['rebate_proport'];
					this.data['defaultRebateProport'] = this.data['default_rebate_proport'];
				}
				this.data['rebates'] = this.data['rebates'].length > 0 ?JSON.parse(this.data['rebates']): [];
				this.data['selfUserNames'] = this.data['self_user_names'].length>0?JSON.parse(this.data['self_user_names']): [];
				this.data['maxProduct'] = this.data['max_product'];
				this.data['settlementPeriod'] = String(this.data['settlement_period']);
			}
		} else {
			this.data = {
				'id': -1,
				'accountType': '1',
				'purchaseMethod': '2',
				'settlementPeriod': '1',
				'companyType': [],
				'optionsForType': [],
				'optionsForCompanyName': [],
				'selfUserNames': [],
				'points': '',
				'rebates': [],
				'orderMoney': '',
				'rebateProport': '',
				'defaultRebateProport': '',
				'maxProduct': 3,
				'customerServiceTel': '',
				'customerServiceQQFirst': '',
				'customerServiceQQSecond': '' 
			};
		}
	},

	handleSelect: function(action) {
		this.data['optionsForType'] = action.data.rows;
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
			'validate_from_condition': '',
			'validate_to_condition': '',
			'order_money_condition': '',
			'rebate_proport_condition': '',
			'default_rebate_proport_condition': ''
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

	handleGetCompanyInfoFromAxe: function(action) {
		this.data['optionsForCompanyName'] = action.data.rows;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;