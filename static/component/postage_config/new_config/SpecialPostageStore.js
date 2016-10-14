/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:SpecialPostageStore');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var SpecialPostageStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateSpecialPostages': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_POSTAGE,
		'handleUpdateSpecialArea': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_AREA,
		'handleAddSpecialPostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_ADD_SPECIAL_POSTAGE,
		'handleUpdateSpecialValues': Constant.POSTAGE_CONFIG_NEW_CONFIG_UPDATE_SPECIAL_VALUES,
		'handleDeleteSpecialPostage': Constant.POSTAGE_CONFIG_NEW_CONFIG_DELETE_SPECIAL_POSTAGE
	},

	init: function() {
		this.data = {
			'hasSpecialPostage': [],
			'specialPostages': [{
				'firstWeight': '',
				'firstWeightPrice': '',
				'addedWeight': '',
				'addedWeightPrice': '',
				'selectedIds': []
			}]
		};

		var postages = Reactman.loadJSON('postages');
		var provinceId2name = Reactman.loadJSON('provinceId2name');
		if(postages){
			var specialPostages = postages['special_postages'];
			this.data['specialPostages'] = specialPostages.length>0? specialPostages: this.data['specialPostages'];
			this.data['hasSpecialPostage'] = specialPostages.length>0? ['1']: [];
		}

		if(provinceId2name){
			this.data['provinceId2name'] = provinceId2name['province_id2name'];
		}
	},

	handleUpdateSpecialPostages: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleAddSpecialPostage: function() {
		var specialPostages = this.data.specialPostages;
		specialPostages.push({
			'firstWeight': '',
			'firstWeightPrice': '',
			'addedWeight': '',
			'addedWeightPrice': '',
			'selectedIds': []
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

	handleUpdateSpecialArea: function(action){
		var index = action.data.index;
		var selectedIds = action.data.selectedIds;
		this.data.specialPostages[index]['selectedIds'] = selectedIds;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = SpecialPostageStore;