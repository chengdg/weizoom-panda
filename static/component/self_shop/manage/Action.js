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
	updateSelfShopDialog: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.updateSelfShopDialog,
			data: {
				property: property,
				value: value
			}
		});
	}
};

module.exports = Action;