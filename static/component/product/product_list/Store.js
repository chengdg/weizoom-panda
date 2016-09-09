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
		'handleUpdateProduct': Constant.PRODUCT_LIST_UPDATE_PRODUCT,
		'handleProductDataFilter': Constant.PRODUCT_DATAS_FILTER,
		'handleProductDataExport': Constant.PRODUCT_DATAS_EXPORT,
		'handleProductModelDetails': Constant.PRODUCT_MODEL_DETAILS,
		'handlePlusProductStore': Constant.PLUS_PRODUCT_STORE
	},

	init: function() {
		this.data = {};
		this.data.user_has_products = '';
		this.filter = {};
		this.category = {};
		this.data.model_names = [];
		this.data.model_values = [];
		this.data.name2model = {};
	},

	handleUpdateProduct: function(action) {
		this.data.user_has_products = parseInt(action.data.user_has_products)-1;
		this.__emitChange();
	},

	handleProductDataFilter: function(action){
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	handleProductDataExport: function(action){
		var filterOptions = this.data.filterOptions;
		var filter_str = '';
		for (var key in filterOptions){
			filter_str = key +'=' + filterOptions[key];
		}
		window.location.href = '/product/product_exported/?'+filter_str;
	},

	handleProductModelDetails: function(action){
		var rows = action.data.rows
		this.data['model_values']= [];
		this.data['model_names']= [];
		var source = [];
		var target = [];
		var headers = [];
		var name2model = this.data['name2model'];
		var _this = this;
		/*
		 * 将数据结构：
		 * [
		 *		{id:1, product_model_name:'颜色', product_model_value:[{id:1, name:'黑色'}, {id:2, name:'白色'}]},
		 *		{id:2, product_model_name:'尺寸', product_model_value:[{id:3, name:'S'}, {id:4, name:'M'}]},
		 *	]
		 * 转换为:
		 * headers: [{id:1, name:'颜色'}, {id:2, name:'尺寸'}]
		 * values: [
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}],
		 ]
		 */
		_.each(rows, function(property) {
			headers.push({
				id: property.id,
				name: property.product_model_name
			});

			_.each(JSON.parse(property.product_model_value), function(propertyValue) {
				var valueName = propertyValue.name;
				var valueId = propertyValue.id;
				if (source.length === 0) {
					target.push([{
						name:valueName, 
						id:valueId, 
						propertyId:property.id
					}]);
				} else {
					_.each(source, function(sourceItem) {
						sourceItem = _.clone(sourceItem);
						sourceItem.push({
							name: valueName,
							id: valueId,
							propertyId: property.id
						})
						target.push(sourceItem);
					});
				}
			});

			source = target;
			target = [];
		});

		/*
		 * 将数据结构：
		 values: [
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}],
		 ]
		 转换为:
		 models: [{
		 	modelId: '1:1_2:3',
		 	propertyValues: [{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}]
		 }, {
		 	modelId: '1:1_2:4',
		 	propertyValues: [{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}]
		 }, {
		 	modelId: '1:2_2:3',
		 	propertyValues: [{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}]
		 }, {
		 	modelId: '1:2_2:4',
		 	propertyValues: [{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}]
		 }]
		 */
		var models = [];
		_.each(source, function(values) {
			var ids = [];
			for (var i = 0; i < values.length; ++i) {
				var value = values[i];
				ids.push(value['propertyId']+':'+value['id']);
			}
			ids = _.sortBy(ids, function(id) { return id; });
			var modelId = ids.join('_');
			if (_this.data.name2model.hasOwnProperty(modelId)) {
				models.push(_this.data.name2model[modelId]);
			} else {
				models.push({
					modelId: modelId,
					propertyValues: values
				})
			}
		});

		this.data = action.data.product_data;
		//判断这个规格存不存在
		var model_values = _.filter(models, function(customModel) {
			console.log(customModel.modelId);
			var price = 'price_'+ customModel.modelId;
			return action.data.product_data[price] !== undefined;
		});
		this.data['model_values']= model_values;
		this.data['model_names']= headers;
		this.data['name2model']= {};
		this.__emitChange();
	},

	handlePlusProductStore: function(){
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	},

	getFilter: function() {
		return this.data.filterOptions;
	}
});

module.exports = Store;