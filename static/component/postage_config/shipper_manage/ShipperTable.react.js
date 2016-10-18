/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.shipper_manage:ShipperTable');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var Reactman = require('reactman');
var W = Reactman.W;

var TableStore = require('./TableStore');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddShipperDialog = require('./AddShipperDialog.react');

var ShipperTable = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function() {
		this.refs.table.refresh();
	},

	addShipper: function() {
		Reactman.PageAction.showDialog({
			title: "快递发货人",
			component: AddShipperDialog,
			data: {},
			success: function() {
				Action.updateTable();
			}
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a href="javascript:void(0);">编辑</a>
					<span>|</span>
					<a href="javascript:void(0);">删除</a>
				</div>
			);
		}else {
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'postage_config.shipper',
			data: {
				page: 1
			}
		};

		return (
			<div className="xui-shipperManage-AccountManagerTable">
				<Reactman.TablePanel>
					<Reactman.TableActionBar></Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} enableSelector={true} pagination={true} ref="table">
						<Reactman.TableColumn name="发货人" field="shipperName" />
						<Reactman.TableColumn name="发货人手机" field="telNumber" width="300"/>
						<Reactman.TableColumn name="发货地区" field="destination" />
						<Reactman.TableColumn name="详细地址" field="address" />
						<Reactman.TableColumn name="邮编" field="postcode" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加新发货人" onClick={this.addShipper}/>
					</Reactman.TableActionBar>
				</Reactman.TablePanel>
			</div>
		)
	}
})

module.exports = ShipperTable;