/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_order_detail::Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');
var window = window;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleShipOrder': Constant.ORDER_DATA_SHIP_ORDER
	},

	init: function() {
		this.data = Reactman.loadJSON('product');
		if (this.data) {
			this.data['isJoinPromotion'] = this.data['is_join_promotion'] ? '1' : '0';
			this.data['promotionFinishDate'] = this.data['promotion_finish_date'];
			this.data['channels'] = JSON.parse(this.data['channels']);
		} else {
			this.data = {
			};
		}
		debug(this.data);
	},

	handleShipOrder: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;