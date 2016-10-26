/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:customer_profile.list_customer_profile:ListCustomerProfilePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var ListCustomerProfilePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onClickChangeStatus: function(event) {
		var accountId = parseInt(event.target.getAttribute('data-account-id'));
		var method = event.target.getAttribute('data-method');
		var title = '确认关闭该账号吗?';
		if( method == 'open'){
			title = '确认开启该账号吗?'
		}
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: title,
			confirm: _.bind(function() {
				Action.changeAccountStatus(accountId,method);
			}, this)
		});
	},

	onClickDelete: function(event) {
		var accountId = parseInt(event.target.getAttribute('data-account-id'));
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除该账号吗?',
			confirm: _.bind(function() {
				Action.deleteAccount(accountId);
			}, this)
		});
	},

	updateAccount: function(id){
		W.gotoPage('/manager/account_create/?id='+id);
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'name') {
			return (
				<a href={'/manager/account_create/?id='+data.id}>{value}</a>
			)
		} else if (field === 'action') {
			if(data.status == 1){
				return (
				<div>
					<a className="btn btn-primary" onClick={this.updateAccount.bind(this,data.id)}>编辑</a>
					<a className="btn btn-primary ml10" onClick={this.onClickChangeStatus} data-account-id={data.id} data-method='close'>关闭</a>
				</div>
				);
			}else if(data.status == 2){
				return (
				<div>
					<a className="btn btn-danger" onClick={this.updateAccount.bind(this,data.id)}>开启</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-account-id={data.id}>删除</a>
				</div>
				);
			}else{
				return (
				<div>
					<a className="btn btn-danger" onClick={this.onClickChangeStatus} data-account-id={data.id} data-method='open'>开启</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-account-id={data.id}>删除</a>
				</div>
				);
			}
		} else {
			return value;
		}
	},

	onConfirmFilter: function(data) {
		Action.filterAccounts(data);
	},
	onExport: function(){
		Action.exportAccounts();
	},
	render:function(){
		var productsResource = {
			resource: 'customer_profile.list',
			data: {
				page: 1
			}
		};
		var statusOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '使用中',
			value: 1
		}, {
			text: '已关闭',
			value: 0
		}];
		var isCpsOptions = [{
			text: '不限',
			value: -1
		}, {
			text: '投放',
			value: 1
		}, {
			text: '未投放',
			value: 0
		}]

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="客户名称:" name="companyName" match='=' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="商品名称:" name="productName" match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="客户账号状态:" name="accountStatus" options={statusOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormSelect label="效果通投放:" name="isCps" options={isCpsOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>
			
			<Reactman.TablePanel>
				<Reactman.TableActionBar>
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
					<Reactman.TableColumn name="客户名称" field="companyName" />
					<Reactman.TableColumn name="客户来源" field="source" />
					<Reactman.TableColumn name="入驻类目" field="companyType" />
					<Reactman.TableColumn name="入驻时间" field="settledTime" />
					<Reactman.TableColumn name="平台开售" field="onShelvesTime" />
					<Reactman.TableColumn name="在售商品" field="onShelvesCount" />
					<Reactman.TableColumn name="累计订单" field="orderCount" />
					<Reactman.TableColumn name="累计成交额" field="orderPrice" />
					<Reactman.TableColumn name="效果通" field="isCps" />
					<Reactman.TableColumn name="入驻方式" field="settledMethod"/>
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = ListCustomerProfilePage;