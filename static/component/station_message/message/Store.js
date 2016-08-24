/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleAddMessage': Constant.ADD_MESSAGE,
		'handleUpdateMessage': Constant.UPDATE_MESSAGE,
	},

	init: function() {
	    this.data = Reactman.loadJSON('message');
	    console.log('=================================12')
	    console.log(this.data)
	    if(!this.data){
	        this.data = {
                'title': '',
                'text': '',
                'create_at': '',
                'attachments': '',
            };
	    }
	},

	handleAddMessage: function(message) {

//        console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>message');
        console.log(message);
        W.gotoPage('/message/message_list');
	},
	handleUpdateMessage: function(action){
	    this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;