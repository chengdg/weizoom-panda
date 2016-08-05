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
	updateCatalog: function(property, value, models, id) {
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_CATALOG,
			data: {
				property: property,
				value: value,
				models: models,
				id: id
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
		Dispatcher.dispatch({
			actionType: Constant.ADD_CATALOG_QUALIFICATION,
			data: {
				models: models
			}
		});
	},
};

module.exports = Action;