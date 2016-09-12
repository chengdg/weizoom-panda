/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateCatalogs: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.CATALOG_DATAS_FILTER,
			data: {}
		});
	},

	deleteCatalog: function(id) {
		Resource.delete({
			resource: 'product_catalog.product_catalogs',
			data: {
				id: id
			},
			success: function() {
				Reactman.PageAction.showHint('success', '删除分类成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.CATALOG_DATAS_FILTER,
						data: {}
					});
				},500);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	},

	//更新类目所需特殊资质
	updateCatalog: function(property, value, models, index) {
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_CATALOG,
			data: {
				property: property,
				value: value,
				models: models,
				index: index
			}
		});
	},

	deleteCatalogQualification: function(index, models) {
		Dispatcher.dispatch({
			actionType: Constant.DELETE_CATALOG,
			data: {
				index: index,
				models: models
			}
		});
	},

	addCatalogQualification: function(models) {
		var index = models.length;
		Dispatcher.dispatch({
			actionType: Constant.ADD_CATALOG_QUALIFICATION,
			data: {
				models: models,
				index: index
			}
		});
	},
	//分类配置标签
	getLabels: function(){
		Resource.get({
			resource: 'label.catalog_label',
			data: {},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_CATALOGS_GET_LABELS
			}
		});
	},

	chooseLabelValue: function(propertyId, valueId) {
		Dispatcher.dispatch({
			actionType: Constant.PRODUCT_CATALOGS_CHOOSE_LABEL_VALUE,
			data: {
				propertyId: propertyId,
				valueId: valueId
			}
		});
	},

	getCatalogHasLabel: function(catalogId, productId) {
		Resource.get({
			resource: 'product_catalog.catalog_has_labels',
			data: {
				catalog_id: catalogId,
				product_id: productId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PRODUCT_CATALOGS_GET_CATALOG_HAS_LABEL
			}
		});
	},

	updateLabels: function(){
		Dispatcher.dispatch({
			actionType: Constant.CATALOG_DATAS_FILTER,
			data: {}
		});
	}
};

module.exports = Action;