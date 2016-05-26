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

	onClickDelete: function(event) {
		//var productId = parseInt(event.target.getAttribute('data-product-id'));
		//Reactman.PageAction.showConfirm({
		//	target: event.target,
		//	title: '确认删除吗?',
		//	confirm: _.bind(function() {
		//		Action.deleteProduct(productId);
		//	}, this)
		//});
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
			return (
			<div>
				<a className="btn btn-link btn-xs" href={'/manager/account_create/?id='+data.id}>编辑</a>
				<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>关闭</a>
			</div>
			);
		} else {
			return value;
		}
	},

	onConfirmFilter: function(data) {
		Action.filterProducts(data);
	},

	render:function(){
		var productsResource = {
			resource: 'manager.account',
			data: {
				page: 1
			}
		};
		var typeOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '客户账号',
			value: 'customer'
		}, {
			text: '代理商账号',
			value: 'agency'
		}, {
			text: '运营账号',
			value: 'yunying'
		}];

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="账号名称:" name="name" match='~' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="登录账号:" name="username" match="~" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="账号类型:" name="account_type" options={typeOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>
			
			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="添加账号" icon="plus" href="/manager/account_create/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
					<Reactman.TableColumn name="账号名称" field="name" />
					<Reactman.TableColumn name="登录账号" field="username" />
					<Reactman.TableColumn name="操作" field="action" width="100px"/>
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = AccountManagePage;