/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var NewProductUnPassDialogStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleChooseUnpassReason': Constant.NEW_PRODUCT_REJECT_UNPASS_REASON,
		'handleUpdateUnpassReason': Constant.NEW_PRODUCT_REJECT_UPDATE_UNPASS_REASON,
		'handleCancleCheckedReason': Constant.NEW_PRODUCT_REJECT_UNDATE_CANCLE_CHECKED
	},

	init: function() {
		this.data = {
			'reasons': [],
			'custom_reason': ''
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

	handleCancleCheckedReason: function(){
		this.data = {
			'reasons': [],
			'custom_reason': ''
		};
	},

	getData: function() {
		return this.data;
	}
});

module.exports = NewProductUnPassDialogStore;