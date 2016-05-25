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
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteProduct(productId);
			}, this)
		});
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	onClickPrice: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var product = this.refs.table.getData(productId);

		Reactman.PageAction.showPopover({
			target: event.target,
			content: '<span style="color:red">' + product.name + ':' + product.price + '</span>'
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'models') {
			var models = value;
			var modelEls = models.map(function(model, index) {
				return (
					<div key={"model"+index}>{model.name} - {model.stocks}</div>
				)
			});
			return (
				<div style={{color:'red'}}>{modelEls}</div>
			);
		} else if (field === 'name') {
			return (
				<a href={'/outline/data/?id='+data.id}>{value}</a>
			)
		} else if (field === 'price') {
			return (
				<a onClick={this.onClickPrice} data-product-id={data.id}>{value}</a>
			)
		} else if (field === 'action') {
			return (
			<div>
				<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>删除</a>
				<a className="btn btn-link btn-xs mt5" href={'/outline/data/?id='+data.id}>编辑</a>
				<a className="btn btn-link btn-xs mt5" onClick={this.onClickComment} data-product-id={data.id}>备注</a>
			</div>
			);
		} else if (field === 'expand-row') {
			return (
				<div style={{paddingBottom:'20px'}}>
				<div className="clearfix" style={{backgroundColor:'#EFEFEF', color:'#FF0000', padding:'5px', borderBottom:'solid 1px #CFCFCF'}}>
					<div className="fl">促销结束日：{data.promotion_finish_time}</div>
					<div className="fr">总金额: {data.price}元</div>
				</div>
				</div>
			)
		} else {
			return value;
		}
	},

	onClickComment: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var product = this.refs.table.getData(productId);
		Reactman.PageAction.showDialog({
			title: "创建备注", 
			component: CommentDialog, 
			data: {
				product: product
			},
			success: function(inputData, dialogState) {
				var product = inputData.product;
				var comment = dialogState.comment;
				Action.updateProduct(product, 'comment', comment);
			}
		});
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
					<Reactman.TableColumn name="#" field="index" width="40px" />
					<Reactman.TableColumn name="账号名称" field="name" />
					<Reactman.TableColumn name="登录账号" field="comment" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = AccountManagePage;