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
var W = Reactman.W;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateProduct': Constant.NEW_PRODUCT_UPDATE_PRODUCT
	},

	init: function() {
		var _this = this;
		try{
			this.data = Reactman.loadJSON('product');
		}catch(e){
			console.log("json.parse error");
		}
		this.model_value = {}	
		if (this.data) {
			this.data['product_store_type'] = this.data['product_store'] > -1 ? '0' : '-1';
			this.data['product_store'] = this.data['product_store'] == -1 ? '9999' : String(this.data['product_store']);
			this.data['name2model'] = {};
			console.log(this.data['value_ids'],"=====");
			var dataStrArr=this.data['value_ids'].split(",");//分割成字符串数组  
			var dataIntArr=[];//保存转换后的整型字符串  
			dataStrArr.forEach(function(data,index,arr){  
				dataIntArr.push(+data);
			});
			this.data['value_ids'] = dataIntArr;
			//组织数据结构
			var organize_data = this.organizeData(JSON.parse(this.data['model_values']));
			//判断这个规格存不存在
			var model_values = _.filter(organize_data[1], function(customModel) {
				var product_price = 'product_price_'+ customModel.modelId;
				return _this.data[product_price] !== undefined;
			});

			this.data['model_values'] = model_values;
			this.data['model_names'] = organize_data[0];
		} else {
			this.data = {
				'id':-1,
				'images':[],
				'remark': '',
				'product_store_type':'-1',
				'has_product_model': '0',
				'has_limit_time': '0',
				'value_ids': [],
				'model_values': [],
				'name2model': {},
				'model_names': [],
				'second_id': 0,
				'catalog_name': ''
			};
		}
	},

	organizeData: function(rows){
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
		return [headers,models]
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;