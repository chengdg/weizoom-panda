/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.account_list:AccountManagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AccountManagePage = React.createClass({
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
					<a className="btn btn-link btn-xs" href={'/manager/account_create/?id='+data.id}>编辑</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickChangeStatus} data-account-id={data.id} data-method='close'>关闭</a>
				</div>
				);
			}else if(data.status == 2){
				return (
				<div>
					<a className="btn btn-link btn-xs" href={'/manager/account_create/?id='+data.id}>开启</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-account-id={data.id}>删除</a>
				</div>
				);
			}else{
				return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.onClickChangeStatus} data-account-id={data.id} data-method='open'>开启</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-account-id={data.id}>删除</a>
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
			resource: 'manager.account',
			data: {
				page: 1,
				is_for_list: true
			}
		};
		var typeOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '客户账号',
			value: 1
		}, {
			text: '代理商账号',
			value: 2
		}, {
			text: '运营账号',
			value: 3
		}];

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="账号名称:" name="name" match='=' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="登录名:" name="username" match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="账号类型:" name="account_type" options={typeOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>
			
			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="导出" onClick={this.onExport}/>
					<Reactman.TableActionButton text="添加账号" icon="plus" href="/manager/account_create/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
					<Reactman.TableColumn name="账号名称" field="name" />
					<Reactman.TableColumn name="登录名" field="username" />
					<Reactman.TableColumn name="经营类目" field="company_type" />
					<Reactman.TableColumn name="采购方式" field="purchase_method" />
					<Reactman.TableColumn name="类型" field="account_type" />
					<Reactman.TableColumn name="操作" field="action" width="100px"/>
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = AccountManagePage;