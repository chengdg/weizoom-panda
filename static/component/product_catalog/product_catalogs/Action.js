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
};

module.exports = Action;