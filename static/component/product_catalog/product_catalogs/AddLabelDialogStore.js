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

var AddLabelDialogStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleGetLabels': Constant.PRODUCT_CATALOGS_GET_LABELS,
		'handleChooseLabelValue': Constant.PRODUCT_CATALOGS_CHOOSE_LABEL_VALUE,
		'handleGetCatalogHasLabel': Constant.PRODUCT_CATALOGS_GET_CATALOG_HAS_LABEL
	},

	init: function() {
		this.data = {
			'labelFirstId': 0,//默认首次显示分类id
			'catalogs': '',
			'propertyId2names': {},
			'labelCatalogs': [],//所有的标签分类值
			'labelValues': [],//所有的标签值
			'selectLabels': [],//选择的标签值(id)
			'selectCatalogLabels': [],//组织 选择的标签,分类
			'valueId2name': {},
			'labelId2name': {}
		};
	},

	handleGetLabels: function(action){
		this.data['propertyId2names'] = action.data.propertyId2name;
		this.data['labelCatalogs'] = action.data.labelCatalogs;
		this.data['valueId2name'] = action.data.valueId2name;
		this.data['labelId2name'] = action.data.labelId2name;
		this.data['labelFirstId'] = action.data.labelFirstId;
	},

	handleGetCatalogHasLabel: function(action){
		var selectCatalogLabels = action.data.selectCatalogLabels.length>0 ? JSON.parse(action.data.selectCatalogLabels): [];
		this.data['selectCatalogLabels'] = selectCatalogLabels;
		this.data['selectLabels'] = action.data.selectLabels;
		this.data['labelFirstId'] = action.data.labelFirstId;
		this.data['catalogs'] = action.data.labelFirstId;
	},

	handleChooseLabelValue: function(action){
		var selectLabels = this.data.selectLabels;
		var selectCatalogLabels = this.data.selectCatalogLabels;
		var valueId = action.data.valueId;
		var propertyId = action.data.propertyId
		var isChoosed = true;

		for(var index in selectLabels){
			if(selectLabels[index]==valueId){
				isChoosed = false;
				selectLabels.splice(index,1);
			}
		}

		if(isChoosed){
			selectLabels.push(valueId);
		}

		//组织 选择的分类id和标签id的对应关系 [{'1':[1,2,3]}]
		var hasPropertyId = false;
		for(var i in selectCatalogLabels){
			if(selectCatalogLabels[i].hasOwnProperty('propertyId') && selectCatalogLabels[i].propertyId == propertyId){
				hasPropertyId = true;
				if(isChoosed){
					selectCatalogLabels[i].valueIds.push(valueId);
				}else{
					for(var index in selectCatalogLabels[i].valueIds){
						if(selectCatalogLabels[i].valueIds[index]==valueId){
							selectCatalogLabels[i].valueIds.splice(index,1);
						}
					}
					if(selectCatalogLabels[i].valueIds.length==0){
						selectCatalogLabels.splice(i,1);
					}
				}
			}
		}

		if(!hasPropertyId){
			selectCatalogLabels.push({
				propertyId: propertyId,
				valueIds: [valueId]
			})
		}

		this.data.selectLabels = selectLabels;
		this.data.selectCatalogLabels = selectCatalogLabels;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = AddLabelDialogStore;