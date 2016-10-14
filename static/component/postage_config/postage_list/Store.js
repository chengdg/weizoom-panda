/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:self_shop.manage:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleSetHasUsed': Constant.POSTAGE_CONFIG_POSTAGE_LIST_SET_HAS_USED,
		'handleDeletePostage': Constant.POSTAGE_CONFIG_POSTAGE_LIST_DELETE_POSTAGE
	},

	init: function() {
		this.data = {
		   'postageId': 0
		};
	},

	handleSetHasUsed: function(action){
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '设置成功!');
		}, 100);

		this.data.postageId = action.data.postageId;
		this.__emitChange();
	},

	handleDeletePostage: function(action){
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '删除成功!');
		}, 100);

		// this.data.postageId = action.data.postageId;
		_.delay(function(){
			W.gotoPage('/postage_config/postage_list/');
		},500)
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;