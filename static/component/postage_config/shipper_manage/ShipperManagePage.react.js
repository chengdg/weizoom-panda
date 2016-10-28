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
		var style = {};
		style['accountIsShow'] = {display: 'none'};
		style['shipperIsShow'] = {display: 'none'};

		style['accountIsActive'] = {};
		style['shipperIsActive'] = {};
		
		if(accountOrShipper=='account'){
			style['accountIsShow'] = {display: 'block'};
			style['accountIsActive'] = {
				backgroundColor: 'rgba(25, 158, 216, 1)',
				borderColor: 'rgba(22, 155, 213, 1)',
				color: '#FFF',
				textDecoration: 'none'
			};
		}else{
			style['shipperIsShow'] = {display: 'block'};
			style['shipperIsActive'] = {
				backgroundColor: 'rgba(25, 158, 216, 1)',
				borderColor: 'rgba(22, 155, 213, 1)',
				color: '#FFF',
				textDecoration: 'none'
			};
		}

		return (
			<div className="mt15 xui-shipperManage-productListPage">
				<div className="pl15">
					<a className="xui-shipperManage-button" style={style['accountIsActive']} href="javascript:void(0);" onClick={this.changeTable.bind(this, 'shipper')}>电子面单账号配置</a>
					<a className="xui-shipperManage-button" style={style['shipperIsActive']} href="javascript:void(0);" onClick={this.changeTable.bind(this, 'account')}>发货人</a>
				</div>
				<div style={style['accountIsShow']}><AccountTable /></div>
				<div style={style['shipperIsShow']}><ShipperTable /></div>
			</div>
		)
	}
})
module.exports = ShipperManagePage;