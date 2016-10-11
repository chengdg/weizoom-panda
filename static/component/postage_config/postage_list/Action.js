/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:self_shop.manage:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	setHasUsed: function(postageId) {
		Resource.post({
			resource: 'postage_config.postage_list',
			data: {
				'postage_id': postageId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.POSTAGE_CONFIG_POSTAGE_LIST_SET_HAS_USED
			}
		});
	},

	deletePostage: function(postageId){
		Resource.delete({
			resource: 'postage_config.postage_list',
			data: {
				'postage_id': postageId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.POSTAGE_CONFIG_POSTAGE_LIST_DELETE_POSTAGE
			}
		});
	}
};

module.exports = Action;