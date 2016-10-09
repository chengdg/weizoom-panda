/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:FreePostageStore');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var FreePostageStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateSpecialPostages': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_POSTAGE,
		'handleAddSpecialPostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_ADD_SPECIAL_POSTAGE,
		'handleUpdateSpecialValues': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_VALUES,
		'handleDeleteSpecialPostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_DELETE_SPECIAL_POSTAGE
	},

	init: function() {
		this.data = {
			'hasFreePostage': [],
			'freePostages': [{
				'first_weight': '',
				'first_weight_price': '',
				'added_weight': '',
				'added_weight_price': ''
			}]
		};
	},

	handleUpdateSpecialPostages: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleAddSpecialPostage: function() {
		var specialPostages = this.data.specialPostages;
		specialPostages.push({
			'first_weight': '',
			'first_weight_price': '',
			'added_weight': '',
			'added_weight_price': ''
		})
		this.data.specialPostages = specialPostages;
		this.__emitChange();
	},

	handleUpdateSpecialValues: function(action) {
		var index = action.data.index;
		var property = action.data.property;
		var value = action.data.value;
		var specialPostages = this.data.specialPostages;
		specialPostages[index][property] = value;
		this.data.specialPostages = specialPostages;
		this.__emitChange();
	},

	handleDeleteSpecialPostage: function(action){
		var index = action.data.index;
		var specialPostages = this.data.specialPostages;
		specialPostages.splice(index,1)
		this.data.specialPostages = specialPostages;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = FreePostageStore;