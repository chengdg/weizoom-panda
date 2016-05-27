/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_list:ProductDataListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var ProductDataListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var title = '彻底删除商品会导致该商品的订单无法同步到当前账号中';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.deleteProduct(productId);
			}, this)
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" href={'/product/new_product/?id='+data.id}>编辑</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>彻底删除</a>
				</div>
			);
		}else {
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_list',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加新商品" icon="plus" href="/product/new_product/" />
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
						<Reactman.TableColumn name="商品信息" field="product_name" />
						<Reactman.TableColumn name="商品价格" field="product_price" />
						<Reactman.TableColumn name="销量" field="sales" />
						<Reactman.TableColumn name="创建时间" field="created_at" />
						<Reactman.TableColumn name="状态" field="status" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductDataListPage;