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
		'handleUpdateConfig': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_CONFIG,
		'handleSavePostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_SAVE_POSTAGE
	},

	init: function() {
		this.data = {
		    'postageName': '',
		    'postageId': -1
		};

		var postages = Reactman.loadJSON('postages');
		if(postages){
			this.data['postageName'] = postages['postage_name'];
			this.data['postageId'] = postages['postage_id'];
		}
	},

	handleUpdateConfig: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleSavePostage: function(action){
		W.gotoPage('/postage_config/postage_list/');
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;