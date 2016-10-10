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
var AddProductModelDialog = require('./AddProductModelDialog.react');
var W = Reactman.W;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateProduct': Constant.NEW_PRODUCT_UPDATE_PRODUCT,
		'handleCreateNewProduct': Constant.NEW_PRODUCT_CREATE,
		'handleNewProductAddModel': Constant.NEW_PRODUCT_ADD_PRODUCT_MODEL,
		'handleSaveProductAddModel': Constant.SAVE_PRODUCT_MODEL_VALUE,
		'handleDeleteProductModelValue': Constant.DELETE_PRODUCT_MODEL_VALUE,
		'handleCancleValidataTIME': Constant.CANCLE_VALIDATA_TIME,
		'handleProductCategory': Constant.PRODUCT_LIST_CATEGORY,
		'handleProductSecondCategory': Constant.PRODUCT_SECOND_CATEGORY,
		'handleProductChooseSecondCategory': Constant.PRODUCT_CHOOSE_SECOND_CATEGORY,
		'handleProductCancleChooseCatalog': Constant.PRODUCT_CANCLE_CHOOSE_CATALOG,
		'handleProductSaveChooseCatalog': Constant.PRODUCT_SAVE_CHOOSE_CATALOG
	},

	init: function() {
		var _this = this;
		var limit_zone_info = Reactman.loadJSON('limit_zone_info');
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
			this.data['limit_zone_type'] = this.data['limit_zone_type'].toString();
			this.data['limit_zone_id'] = this.data['limit_zone_id'].toString();
			this.data['limit_zone_info'] = limit_zone_info;
		} else {
			this.data = {
				'id':-1,
				'images':[],
				'remark': '',
				'product_store_type':'-1',
				'has_product_model': '',
				'has_limit_time': '0',
				'value_ids': [],
				'model_values': [],
				'name2model': {},
				'model_names': [],
				'second_id': 0,
				'catalog_name': '',
				'limit_zone_type': '-1',
				'limit_zone_id': '0',
				'limit_zone_info': limit_zone_info
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

	handleUpdateProduct: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleNewProductAddModel: function(action){
		var value_id = action.data.value_id;
		var value_ids = this.data['value_ids'];
		if(value_ids.indexOf(value_id)!=-1){
			for(var index in value_ids){
				if (value_ids[index] == value_id){
					value_ids.splice(index,1);
				}
			}
		}else{
			this.data['value_ids'].push(action.data.value_id);
		}
		this.__emitChange();
	},

	handleSaveProductAddModel: function(action){
		var data = this.organizeData(action.data.rows);
		var headers = data[0];
		var models = data[1];

		if(action.data.rows.length>3){
			setTimeout(function() {
			 	Reactman.PageAction.showHint('error', '最多添加三种规格,请重新选择规格');
			}, 10);
			return;
		}else{
			this.data['model_values']= models;
			this.data['model_names']= headers;
			setTimeout(function() {
			 	Reactman.PageAction.showHint('success', '添加成功!');
			}, 10);
			this.__emitChange();
		}
	},

	handleDeleteProductModelValue: function(action){
		var customModels = this.data['model_values'];
		var value_ids = this.data['value_ids'];
		var this_customModels = _.filter(customModels, function(customModel) {
			return customModel.modelId !== action.data.modelId;
		});
		var delete_customModels = _.filter(customModels, function(customModel) {
			return customModel.modelId === action.data.modelId;
		});

		var this_customModels_value_id = []
		_.each(this_customModels, function(customModels){
			_.each(customModels.propertyValues, function(customModel){
				this_customModels_value_id.push(customModel.id)
			})
		})
		for(var i in delete_customModels){
			var propertyValues = delete_customModels[i].propertyValues;
			for(var j in propertyValues){
				var is_cansle= true;
				if(this_customModels_value_id.indexOf(propertyValues[j].id)!= -1){
					is_cansle = false;
				}
				if(is_cansle){
					var index = value_ids.indexOf(propertyValues[j].id);
					value_ids.splice(index,1);
				}
			}
		}
		this.data['model_values'] = this_customModels;
		this.data['value_ids'] = value_ids;
		this.__emitChange();
	},

	handleCreateNewProduct: function(action) {
		setTimeout(function() {
		 	Reactman.PageAction.showHint('success', '保存成功!');
		}, 10);
		setTimeout(function() {
		 	W.gotoPage('/product/product_list/');
		}, 500);
	},

	handleCancleValidataTIME: function(action){
		var modelId = action.data.modelId;
		this.data['valid_time_from_'+modelId] = '';
		this.data['valid_time_to_'+modelId] = '';
		this.__emitChange();
	},

	handleProductCategory: function(action){
		var first_levels = JSON.parse(action.data['first_levels']);
		var second_levels = action.data['second_levels'];
		if(second_levels.length>0){
			second_levels = JSON.parse(action.data['second_levels']);
			this.data['second_levels'] = second_levels;
			this.data['second_id'] = second_levels[0].id;
		}
		// first_levels[0]['is_choose'] = 1;
		// second_levels[0]['is_choose'] = 1;
		this.data['first_levels'] = first_levels;
		this.__emitChange();
	},

	handleProductSecondCategory: function(action){
		var first_levels = this.data['first_levels'];
		var first_id = action.data['first_id'];
		_.each(first_levels, function(first_level) {
			if(first_level['id']==first_id){
				first_level['is_choose'] = 1;
			}else{
				first_level['is_choose'] = 0;
			}
		});
		this.data['first_levels'] = first_levels;
		this.data['second_id'] = 0;
		var second_levels = action.data['second_levels'].length>0?JSON.parse(action.data['second_levels']):''
		this.data['second_levels'] = second_levels;
		
		this.__emitChange();
	},

	handleProductChooseSecondCategory: function(action){
		var second_levels = this.data['second_levels'];
		var second_id = action.data.second_id;
		_.each(second_levels, function(second_level) {
			if(second_level['id']==second_id){
				second_level['is_choose'] = 1;
			}else{
				second_level['is_choose'] = 0;
			}
		});
		this.data['second_id'] = second_id;
		this.__emitChange();
	},

	handleProductCancleChooseCatalog: function(){
		this.data['second_id'] = this.data['old_second_catalog_id'];
		this.__emitChange();
	},

	handleProductSaveChooseCatalog: function(action){
		this.data['catalog_name'] = action.data.catalogName;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;