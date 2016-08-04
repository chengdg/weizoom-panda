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
	setFreightValue: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.SET_FREIGHT_VALUE,
			data: {
				property: property,
				value: value
			}
		});
	},

	saveSalePhone: function(freeFreightMoney,needFreightMoney){
		Resource.put({
			resource: 'freight_service.freight',
			data: {
				'free_freight_money': freeFreightMoney,
				'need_freight_money': needFreightMoney
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.SAVE_FREIGHT_MONEY
			}
		});
	}
};

module.exports = Action;