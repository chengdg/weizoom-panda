/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var BusinessDialog = require('./BusinessDialog.react');

var BusinessManagerPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return({})
	},

	onClickPass: function(event) {
		var businessId = parseInt(event.target.getAttribute('data-id'));
		var title = '确认通过该申请吗?';
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: title,
			confirm: _.bind(function() {
				Action.changeBusinessStatus(businessId);
			}, this)
		});
	},

	onClickUnPass: function(event) {
		var businessId = event.target.getAttribute('data-id');
		Reactman.PageAction.showDialog({
			title: "商家入驻驳回",
			component: BusinessDialog,
			data: {
				id: businessId
			},
			success: function() {
				Action.updateBusinessStatus();
			}
		});
	},

	onClickDelete: function(event) {
		var accountId = parseInt(event.target.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除该申请吗?',
			confirm: _.bind(function() {
				Action.deleteBusiness(accountId);
			}, this)
		});
	},
	
	onChangeStore: function(event) {
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	rowFormatter: function(field, value, data) {
		if(field === 'company_name'){
			return (
				<div style={{textAlign:'left'}}>
					<a href={'/business/business_detail/?id='+data.id}>{data.company_name}</a>
				</div>
			)
		}else if (field === 'action') {
			if(data.status == '待审核'){
				return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.onClickPass} data-id={data.id}>通过</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickUnPass} data-id={data.id}>驳回</a>
					<a className="btn btn-link btn-xs" href={'/business/business_detail/?id='+data.id}>修改</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-id={data.id} data-method='close'>删除</a>
				</div>
				);
			}else{
				return (
				<div>
					<a className="btn btn-link btn-xs" href={'/business/business_detail/?id='+data.id}>修改</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-id={data.id} data-method='close'>删除</a>
				</div>
				);
			}
		} else{
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDatas(data);
	},

	render:function(){
		var productsResource = {
			resource: 'business.manager',
			data: {
				page: 1
			}
		};
		var typeOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '厂家直销',
			value: 1
		}, {
			text: '代理/贸易/分销',
			value: 2
		}];
		var statusOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '待审核',
			value: 1
		}, {
			text: '审核通过',
			value: 2
		}, {
			text: '已驳回',
			value: 3
		}];
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="客户编号:" name="customer_number" match='=' />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormInput label="公司名称:" name="company_name" match='=' />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormInput label="所在地:" name="company_location" match='=' />
						</Reactman.FilterField>
					</Reactman.FilterRow>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormSelect label="企业类型:" name="company_type" options={typeOptions} match="=" />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormInput label="手机号:" name="phone" match='=' />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormSelect label="客户状态:" name="status" options={statusOptions} match='=' />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="客户编号" field="customer_number" />
						<Reactman.TableColumn name="公司名称" field="company_name" />
						<Reactman.TableColumn name="所在地" field="company_location" />
						<Reactman.TableColumn name="企业类型" field="company_type" />
						<Reactman.TableColumn name="类目" field="product_catalogs" />
						<Reactman.TableColumn name="联系人" field="contacter" />
						<Reactman.TableColumn name="手机号" field="phone" />
						<Reactman.TableColumn name="状态" field="status" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = BusinessManagerPage;