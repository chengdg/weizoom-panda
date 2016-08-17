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
		'handleCatelogDataFilter': Constant.CATALOG_DATAS_FILTER,
		'handleUpdateCatalog': Constant.UPDATE_CATALOG,
		'handleDeleteCatalog': Constant.DELETE_CATALOG,
		'handleAddCatalog': Constant.ADD_CATALOG_QUALIFICATION
	},

	init: function() {
		this.data = {
			'models': [],
		};
	},

	handleCatelogDataFilter: function(action){
		this.data = action.data;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	},
	handleUpdateCatalog: function(action) {
		var old_models = action.data.models;
		var target_index = action.data.index;
		_.each(old_models, function(old_model) {
			if(old_model.index==target_index){
				old_model['name'] = action.data.value;
			}
		});
		console.log(old_models);
		this.data['models'] = old_models;
		this.__emitChange();
	},
	handleDeleteCatalog: function(action) {
		var index = action.data.index;
		var old_models = action.data.models;
		old_models.splice(index, 1);
		this.data['models'] = old_models;
		this.__emitChange();
	},
	handleAddCatalog: function(action) {
		var old_models = action.data.models;
		old_models.push({
				name: '',
				index: action.data.index
			});
		this.data['models'] = old_models;
		this.__emitChange();
	},
});

module.exports = Store;