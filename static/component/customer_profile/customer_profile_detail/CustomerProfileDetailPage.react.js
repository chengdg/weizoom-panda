/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:customer_profile.customer_profile_detail:CustomerProfileDetailPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var CustomerProfileDetailPage = React.createClass({
	getInitialState: function() {
		return {};
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	rowFormatter: function(field, value, data) {
		// if (field === 'companyName') {
		// 	return (
		// 		<a href={'/customer_profile/detail/?account_id='+data.id}>{value}</a>
		// 	)
		// } else {
			return value;
		// }
	},

	onConfirmFilter: function(data) {
		Action.filterAccounts(data);
	},

	render:function(){
		var productsResource = {
			resource: 'customer_profile.detail',
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
module.exports = CustomerProfileDetailPage;