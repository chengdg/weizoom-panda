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

	deleteMessage: function(message_id){

        Reactman.Resource.delete({
            resource: 'message.message',
            data: {
                message_id: message_id,
            },
            success: function() {
                Reactman.PageAction.showHint('success', 'SUCCESS!');
                Dispatcher.dispatch({
						actionType: Constant.MESSAGE_FILTER,
						data: {}
					});
            },
            error: function() {
                Reactman.PageAction.showHint('error', 'FAILED!');
            }
        })
	},

    getUnreadMes: function() {
        Reactman.Resource.get({
            resource: 'message.customer_messages',
            data: {},
            success: function(data) {
                Dispatcher.dispatch({
                    actionType: Constant.GET_UNREAD_MESSAGE,
                    data: data
                });
            }
        })        
    }
};

module.exports = Action;