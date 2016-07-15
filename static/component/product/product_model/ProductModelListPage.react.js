/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_model:ProductModelListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var ProductModelListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getFilter();
		this.refs.table.refresh(filterOptions);
	},

	onClickDelete: function(event) {
		var user_has_products = W.user_has_products;
		if(Store.getData().user_has_products){
			user_has_products = Store.getData().user_has_products;
		}
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var title = '彻底删除商品会导致该商品的订单无法同步到当前账号中';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.deleteProduct(productId,user_has_products);
			}, this)
		});
	},

	onValidateAddProduct: function(){
		W.gotoPage('/product/new_product/');
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>彻底删除</a>
				</div>
			);
		}else if(field === 'model_type'){
			var model_type = data['data'];
			if(model_type==0){
				return(
					<div>value</div>
					)
			}else{
				return(
					<div>value</div>
					)
			}
		} else {
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	onExport: function(){
		Action.exportProducts();
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_model',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="规格名" field="product_model_name" width="400px"/>
						<Reactman.TableColumn name="显示样式" field="model_type" />
						<Reactman.TableColumn name="规格值" field="model_name" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductModelListPage;