/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.shipper_manage:AccountTable');
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

var AddAccountDialog = require('./AddAccountDialog.react');

var AccountTable = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function() {
		this.refs.table.refresh();
	},

	addExpressBillAccount: function() {
		Reactman.PageAction.showDialog({
			title: "电子面单账号",
			component: AddAccountDialog,
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
			resource: 'postage_config.express_bill',
			data: {
				page: 1
			}
		};

		return (
			<div className="xui-shipperManage-AccountManagerTable">
				<Reactman.TablePanel>
					<Reactman.TableActionBar></Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} enableSelector={true} pagination={true} ref="table">
						<Reactman.TableColumn name="快递公司" field="expressName" />
						<Reactman.TableColumn name="商家号/ID(CustomerName)" field="customerName" width="300"/>
						<Reactman.TableColumn name="商家密码(CustomerPwd)" field="customerPwd" />
						<Reactman.TableColumn name="MonthCode" field="logisticsNumber" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加新快递公司电子面单账号" onClick={this.addExpressBillAccount}/>
					</Reactman.TableActionBar>
				</Reactman.TablePanel>
			</div>
		)
	}
})

module.exports = AccountTable;