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

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateLabelProperty': Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_PROPERTY,
		'handleDeleteLabelProperty': Constant.LABEL_LABEL_MANAGER_DELETE_LABEL_PROPERTY,

		'handleUpdateLabelValue': Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_VALUE
	},

	init: function() {
		this.data = {
			'labelValue': ''
		};
	},

	handleUpdateLabelValue: function(action) {
		this.__emitChange();
	},

	handleUpdateLabelProperty: function(action){
		this.__emitChange();
	},

	handleDeleteLabelProperty: function(action) {
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '删除成功');
		}, 10);
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;