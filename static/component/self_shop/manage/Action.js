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
	addRebateValue: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.ADD_REBATE_VALUE,
			data: {
				property: property,
				value: value
			}
		});
	}
};

module.exports = Action;