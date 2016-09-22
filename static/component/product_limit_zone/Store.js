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

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateTemplates': Constant.LIMIT_ZONE_TEMPLATE_UPDATE,
	},

	init: function() {
		this.data = {
			
		};
	},

    handleUpdateTemplates: function(action){
		this.__emitChange();
    },

    getData: function() {
		return this.data;
	}
});

module.exports = Store;