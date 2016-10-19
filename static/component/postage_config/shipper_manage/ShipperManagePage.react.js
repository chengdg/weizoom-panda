/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.shipper_manage:ShipperManagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var Reactman = require('reactman');
var W = Reactman.W;

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AccountTable = require('./AccountTable.react');
var ShipperTable = require('./ShipperTable.react');

var ShipperManagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	changeTable: function(status){
		Action.changeTable(status);
	},

	render:function(){
		var accountOrShipper = this.state.accountOrShipper;
		// if(accountOrShipper=='account'){
		// 	return (
		// 		<div className="mt15 xui-shipperManage-productListPage">
		// 			<div>
		// 				<a className="xui-shipperManage-button xui-active-btn" href="javascript:void(0);">电子免单账号配置</a>
		// 				<a className="xui-shipperManage-button" href="javascript:void(0);" onClick={this.changeTable.bind(this, 'account')}>发货人</a>
		// 			</div>
		// 			<AccountTable />
		// 		</div>
		// 	)
		// }else{
		// 	return (
		// 		<div className="mt15 xui-shipperManage-productListPage">
		// 			<div>
		// 				<a className="xui-shipperManage-button" href="javascript:void(0);" onClick={this.changeTable.bind(this, 'shipper')}>电子免单账号配置</a>
		// 				<a className="xui-shipperManage-button xui-active-btn" href="javascript:void(0);">发货人</a>
		// 			</div>
		// 			<ShipperTable />
		// 		</div>
		// 	)
		// }

		return (
			<div className="mt15 xui-shipperManage-productListPage">
				<AccountTable />
				<ShipperTable />
			</div>
		)
	}
})
module.exports = ShipperManagePage;