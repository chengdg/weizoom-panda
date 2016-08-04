/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	addSalePhone: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.ADD_SALE_PHONE,
			data: {
				property: property,
				value: value
			}
		});
	},

	saveSalePhone: function(preSaleTel,afterSaleTel){
		Resource.put({
			resource: 'freight_service.service',
			data: {
				'pre_sale_tel': preSaleTel,
				'after_sale_tel': afterSaleTel
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.SAVE_SALE_PHONE
			}
		});
	}
};

module.exports = Action;