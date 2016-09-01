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
	addLabelProperty: function(filterOptions){
		Resource.put({
			resource: 'label.label_manager',
			data: {},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_PROPERTY
			}
		});
	},

	updateLabelProperty: function(id,name){
		Resource.post({
			resource: 'label.label_manager',
			data: {
				'label_id':id,
				'name':name
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_PROPERTY
			}
		});
	},

	deleteLabelProperty:function(labelId){
		Resource.delete({
			resource: 'label.label_manager',
			data: {
				'label_id': labelId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.LABEL_LABEL_MANAGER_DELETE_LABEL_PROPERTY
			}
		});
	},

	updateLabelValue:function(){
		Dispatcher.dispatch({
			actionType: Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_VALUE,
			data: {}
		});
	},

	deleteLabelValue:function(labelValueId){
		Resource.delete({
			resource: 'label.label_value',
			data: {
				'label_value_id': labelValueId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.LABEL_LABEL_MANAGER_UPDATE_LABEL_VALUE
			}
		});
	}
};

module.exports = Action;