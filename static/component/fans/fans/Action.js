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
	filterDates: function(filterOptions){
		Dispatcher.dispatch({
			actionType: Constant.FANS_DATAS_FILTER,
			data: filterOptions
		});
	}
};

module.exports = Action;