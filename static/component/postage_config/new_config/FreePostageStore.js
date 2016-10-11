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
		'handleUpdateFreeValues': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_FREE_VALUES,
		'handleUpdateCondition': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_CONDITION,
		'handleUpdateFreePostages': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_FREE_POSTAGE,
		'handleUpdateFreeArea': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_FREE_AREA,
		'handleAddFreePostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_ADD_FREE_POSTAGE,
		'handleDeleteFreePostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_DELETE_FREE_POSTAGE
	},

	init: function() {
		this.data = {
			'hasFreePostage': [],
			'freePostages': [{
				'conditionValue': '',
				'condition': 'count',
				'selectedIds': []
			}]
		};

		var postages = Reactman.loadJSON('postages');
		var provinceId2name = Reactman.loadJSON('provinceId2name');
		if(postages){
			var freePostages = postages['free_postages'];
			this.data['freePostages'] = freePostages.length>0? freePostages: this.data['freePostages'];
			this.data['hasFreePostage'] = freePostages.length>0? ['1']: [];
		}

		if(provinceId2name){
			this.data['provinceId2name'] = provinceId2name['province_id2name'];
		}
	},

	handleUpdateFreePostages: function(action){
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleUpdateFreeValues: function(action) {
		var index = action.data.index;
		var property = action.data.property;
		this.data.freePostages[index][property] = action.data.value;
		this.__emitChange();
	},

	handleUpdateCondition: function(action) {
		var index = action.data.index;
		var condition = action.data.condition;
		var freePostages = this.data.freePostages;

		if(condition == 'count'){
			freePostages[index]['condition'] = 'money';
		}else{
			freePostages[index]['condition'] = 'count';
		}

		freePostages[index]['conditionValue'] = '';

		this.data.freePostages = freePostages;
		this.__emitChange();
	},

	handleAddFreePostage: function() {
		var freePostages = this.data.freePostages;
		freePostages.push({
			'conditionValue': '',
			'condition': 'count',
			'selectedIds': []
		})
		this.data.freePostages = freePostages;
		this.__emitChange();
	},

	handleDeleteFreePostage: function(action){
		var index = action.data.index;
		var freePostages = this.data.freePostages;
		freePostages.splice(index,1)
		this.data.freePostages = freePostages;
		this.__emitChange();
	},

	handleUpdateFreeArea: function(action){
		var index = action.data.index;
		var selectedIds = action.data.selectedIds;
		this.data.freePostages[index]['selectedIds'] = selectedIds;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = FreePostageStore;