/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.create_account:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateAccount: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.NEW_ACCOUNT_UPDATE_ACCOUNT,
			data: {
				property: property,
				value: value
			}
		});
	},

	selectCatalog: function(){
		Resource.get({
			resource: 'product_catalog.get_all_first_catalog',
			data: {
				is_account_page: true
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.NEW_ACCOUNT_SELECT_CATALOG
			}
		})
	},

	saveAccount: function(data) {
		var account_info = {
			name: data['name'],
			company_name: data['company_name'],
			company_type: JSON.stringify(data['company_type']),
			purchase_method: data['purchase_method'],
			points: data['points'],
			contacter: data['contacter'],
			phone: data['phone'],
			valid_time_from: data['valid_time_from'],
			valid_time_to: data['valid_time_to'],
			username: data['username'],
			password: data['password'],
			account_type: parseInt(data['account_type']),
			note: data['note']
			// self_user_names: JSON.stringify(data['self_user_names']),注释代码 请勿删除
			// rebates: JSON.stringify(data['rebates']),
			// order_money: data['order_money'],
			// rebate_proport: data['rebate_proport'],
			// default_rebate_proport: data['default_rebate_proport']
		};
		if (data.id === -1) {
			Resource.put({
				resource: 'manager.account_create',
				data: account_info,
				success: function() {
					Reactman.PageAction.showHint('success', '创建账号成功');
					setTimeout(function(){
						Dispatcher.dispatch({
							actionType: Constant.NEW_ACCOUNT_CREATE,
							data: data
						});
					},1000);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				}
			});
		} else {
			account_info['id'] = data.id;
			Resource.post({
				resource: 'manager.account_create',
				data: account_info,
				success: function() {
					Reactman.PageAction.showHint('success', '编辑账号成功');
					setTimeout(function(){
						Dispatcher.dispatch({
							actionType: Constant.NEW_ACCOUNT_CREATE,
							data: data
						});
					},1000);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				}
			});
		}
	},

	addSelfShop: function(self_user_name){
		Dispatcher.dispatch({
			actionType: Constant.ADD_SELF_SHOP,
			data: {
				self_user_name: self_user_name
			}
		});
	},

	deleteSelfShop: function(index) {
		Dispatcher.dispatch({
			actionType: Constant.DELETE_SELF_SHOP,
			data: {
				index: index
			}
		});
	},

	addRebateDialog: function(){
		Dispatcher.dispatch({
			actionType: Constant.ADD_REBATE_DIALOG,
			data: {}
		});
	},

	updateRebates: function(index, property, value){
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_REBATES,
			data: {
				index: index,
				property: property,
				value: value
			}
		});
	},

	deleteRebateValue: function(index){
		Dispatcher.dispatch({
			actionType: Constant.DELETE_REBATE_VALUE,
			data: {
				index: index
			}
		});
	},

	updateGroupPoints: function(index, property, value){
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_GROUP_POINTS,
			data: {
				index: index,
				property: property,
				value: value
			}
		});
	}
};

module.exports = Action;