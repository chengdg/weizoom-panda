/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.datas:OrderDatasPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var OrderDatasPage = React.createClass({
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
		if (field === 'name') {
			return (
				<a href={'/outline/data/?id='+data.id}>{value}</a>
			)
		} else if (field === 'action') {
			return (
			<div>
				<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>删除</a>
				<a className="btn btn-link btn-xs mt5" href={'/outline/data/?id='+data.id}>编辑</a>
				<a className="btn btn-link btn-xs mt5" onClick={this.onClickComment} data-product-id={data.id}>备注</a>
			</div>
			);
		}else {
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
			resource: 'order.datas',
			data: {
				page: 1
			}
		};
		var typeOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '待发货',
			value: '0'
		}, {
			text: '已发货',
			value: '1'
		}, {
			text: '已完成',
			value: '2'
		}];

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="订单编号:" name="order_id" match='~' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormDateRangeInput label="下单时间:" name="order_date" match="[t]" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormSelect label="订单状态:" name="order_status" options={typeOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>

			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="批量发货" href="/outline/data/" />
					<Reactman.TableActionButton text="导出" href="/outline/data/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
					<Reactman.TableColumn name="商品" field="name" />
					<Reactman.TableColumn name="备注" field="comment" width="150px"/>
					<Reactman.TableColumn name="价格" field="price" width="80px" />
					<Reactman.TableColumn name="规格" field="models" width="100px" />
					<Reactman.TableColumn name="创建日" field="created_at" width="160px" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = OrderDatasPage;