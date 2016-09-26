/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_relation:RevokeSelfShopStore');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var RevokeSelfShopStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleChooseUnpassReason': Constant.PRODUCT_PRODUCT_RELATION_CHOOSE_UNPASS_REASON,
		'handleUpdateUnpassReason': Constant.PRODUCT_PRODUCT_RELATION_UPDATE_REASON,
		'handleCancleChooseReason': Constant.PRODUCT_PRODUCT_RELATION_CANCLE_CHOOSE_REASON
	},

	init: function() {
		this.data = {
			'reasons': [],
			'customReason': ''
		};
	},

	handleUpdateUnpassReason: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},


	handleChooseUnpassReason: function(action){
		var reasons = this.data.reasons;
		var reason = action.data.reason;
		var isChoosed = true;

		for(var index in reasons){
			if(reasons[index]==reason){
				isChoosed = false;
				reasons.splice(index,1);
			}
		}

		if(isChoosed){
			reasons.push(reason);
		}

		this.data.reasons = reasons;
		this.__emitChange();
	},

	handleCancleChooseReason: function(){
		this.data = {
			'reasons': [],
			'customReason': ''
		};
	},

	getData: function() {
		return this.data;
	}
});

module.exports = RevokeSelfShopStore;