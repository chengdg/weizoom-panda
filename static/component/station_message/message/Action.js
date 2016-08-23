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

	addMessage: function(message) {
        if(message.id <= 0){
            Reactman.Resource.put({
                resource: 'message.message',
                data: {
                    title: message.title,
                    text: message.text,
                    attachment: JSON.stringify(message.attachment)
                },
                success: function() {
                    Reactman.PageAction.showHint('success', '创建消息成功!');
                    W.gotoPage('/message/message_list');
                },
                error: function() {
                    Reactman.PageAction.showHint('error', '创建消息失败!');
                },
                dispatch: {
                    dispatcher: Dispatcher,
                    actionType: Constant.ADD_MESSAGE
                }
            })
        }else{
            Reactman.Resource.post({
                resource: 'message.message',
                data: {
                    title: message.title,
                    text: message.text,
                    attachment: JSON.stringify(message.attachment),
                    message_id: message.id
                },
                success: function() {
                    Reactman.PageAction.showHint('success', 'SUCCESS!');
                    W.gotoPage('/message/message_list');
                },
                error: function() {
                    Reactman.PageAction.showHint('error', 'FAILED!');
                },
                dispatch: {
                    dispatcher: Dispatcher,
                    actionType: Constant.ADD_MESSAGE
                }
            })
        }


	},
	updateMessage: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_MESSAGE,
			data: {
				property: property,
				value: value
			}
		});
	},

};

module.exports = Action;