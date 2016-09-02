/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateSelfShopDialog: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_SELF_SHOP_DIALOG,
			data: {
				property: property,
				value: value
			}
		});
	},
	syncSelfShopProduct: function(userName) {
		Resource.post({
			resource: 'self_shop.manage',
			data: {
				self_user_name: userName
			},
			success: function() {
				Reactman.PageAction.showHint('success', '同步成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.UPDATE_SELF_SHOPS,
						data: {}
					});
				},500);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	},
};

module.exports = Action;