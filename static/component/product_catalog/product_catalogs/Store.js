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
		'handleDeleteCatalog': Constant.DELETE_CATALOG
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
		var target_id = action.data.id;
		_.each(old_models, function(old_model) {
			console.log(old_model.id,old_model.name);
			if(old_model.id==target_id){
				old_model['name'] = action.data.value;
			}
		});
		console.log(old_models);
		this.data['models'] = old_models;
		this.__emitChange();
	},
	handleDeleteCatalog: function(action) {
		var index = action.data.index;
		console.log(index);
		var old_models = action.data.models;
		console.log(old_models);
		old_models.splice(index, 1);
		console.log(old_models);
		this.data['models'] = old_models;
		this.__emitChange();
	},
});

module.exports = Store;