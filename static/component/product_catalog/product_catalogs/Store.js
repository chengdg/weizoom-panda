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
		'handleAddCatalog': Constant.ADD_CATALOG_QUALIFICATION,
		'handleGetLabels': Constant.PRODUCT_CATALOGS_GET_LABELS
	},

	init: function() {
		this.data = {
			'models': [],
			'propertyId2names': {},
			'labelCatalogs': [],
			'labelValues': []
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
		var oldModels = action.data.models;
		var targetIndex = action.data.index;
		_.each(oldModels, function(oldModel) {
			if(oldModel.index == targetIndex){
				oldModel['name'] = action.data.value;
			}
		});
		this.data['models'] = oldModels;
		this.__emitChange();
	},

	handleDeleteCatalog: function(action) {
		var index = action.data.index;
		var oldModels = action.data.models;
		oldModels.splice(index, 1);
		this.data['models'] = oldModels;
		this.__emitChange();
	},

	handleAddCatalog: function(action) {
		var oldModels = action.data.models;
		oldModels.push({
				name: '',
				index: action.data.index
			});
		this.data['models'] = oldModels;
		this.__emitChange();
	}
});

module.exports = Store;