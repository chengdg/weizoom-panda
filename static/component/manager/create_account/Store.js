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
		'handleDeleteSelfShop':Constant.DELETE_SELF_SHOP
	},

	init: function() {
		this.data = Reactman.loadJSON('user_profile_data');
		if (this.data) {
			this.data['account_type'] = String(this.data['account_type']);
			if (this.data['account_type'] == '1'){
				this.data['purchase_method'] = String(this.data['purchase_method']);
				this.data['company_type'] = JSON.parse(this.data['company_type']);
				this.data['options_for_type'] = [];
				if (this.data['purchase_method'] != '2'){
					this.data['points'] = '';
				}
			}
		} else {
			this.data = {
				'id':-1,
				'account_type':'1',
				'purchase_method': '2',
				'company_type': [],
				'options_for_type': [],
				'self_user_names': [],
				'points': ''
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
		this.data[selfUserName+'_value'] = this.data.points;
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

	getData: function() {
		return this.data;
	}
});

module.exports = Store;