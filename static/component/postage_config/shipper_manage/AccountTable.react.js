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

var AccountTableStore = require('./AccountTableStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddAccountDialog = require('./AddAccountDialog.react');

var AccountTable = React.createClass({
	getInitialState: function() {
		AccountTableStore.addListener(this.onChangeStore);
		return AccountTableStore.getData();
	},

	onChangeStore: function() {
		this.refs.accountTable.refresh();
	},

	addExpressBillAccount: function() {
		Action.clearData();
		Reactman.PageAction.showDialog({
			title: "电子面单账号",
			component: AddAccountDialog,
			data: {},
			success: function() {
				Action.updateAccountTable();
			}
		});
	},

	editExpressBill: function(expressId){
		Action.getExpressBillAccount(expressId);
		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "电子面单账号",
				component: AddAccountDialog,
				data: {},
				success: function() {
					Action.updateAccountTable();
				}
			});
		},100)
	},

	deleteExpressBill: function(expressId, event){
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确定删除么？',
			confirm: _.bind(function() {
				Action.deleteExpressBillAccount(expressId);
			}, this)
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			var expressId = data['expressId'];
			return (
				<div>
					<a href="javascript:void(0);" onClick={this.editExpressBill.bind(this, expressId)}>编辑</a>
					<span className="xui-split-line">|</span>
					<a href="javascript:void(0);" onClick={this.deleteExpressBill.bind(this, expressId)}>删除</a>
				</div>
			);
		}else if(field === 'expressName'){
			var options = {
				'yuantong': '圆通速递',
				'zhongtong': '中通速递',
				'shentong': '申通快递',
				'tiantian': '天天快递',
				'yunda': '韵达快运',
				'huitongkuaidi': '百世快递',
				'shunfeng': '顺丰速运',
				'debangwuliu': '德邦物流',
				'zhaijisong': '宅急送',
				'youshuwuliu': '优速物流',
				'guangdongyouzheng': '广东邮政',
				'ems': 'EMS'
			}
			
			return(
				<span>{options[value]}</span>
			)
		}else{
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
			<div className="xui-AccountManagerTable">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} enableSelector={true} pagination={true} ref="accountTable">
						<Reactman.TableColumn name="快递公司" field="expressName" />
						<Reactman.TableColumn name="商家号/ID(CustomerName)" field="customerName" />
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