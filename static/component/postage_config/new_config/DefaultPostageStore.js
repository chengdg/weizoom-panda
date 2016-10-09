/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:DefaultPostageStore');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var DefaultPostageStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateDefaultPostages': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_DEFAULT_POSTAGE,
	},

	init: function() {
		this.data = {
		    'defaultPostages': [{
		    	'first_weight': '',
		    	'first_weight_price': '',
		    	'added_weight': '',
		    	'added_weight_price': ''
		    }]
		};
	},

	handleUpdateDefaultPostages: function(action) {
		this.data.defaultPostages[0][action.data.property] = action.data.value;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = DefaultPostageStore;