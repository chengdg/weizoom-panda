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
require('./style.css');
var W = Reactman.W;

var ProductDataListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		this.refs.table.refresh();
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
		var user_has_products = W.user_has_products;
		if(Store.getData().user_has_products){
			user_has_products = Store.getData().user_has_products;
		}
		if(user_has_products >= 3){
			Reactman.PageAction.showHint('error', '达到最大商品数,如有更多需要请联系客服400-688-6929!');
			return;
		}else{
			W.gotoPage('/product/new_product/');
		}
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" href={'/product/new_product/?id='+data.id}>编辑</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>彻底删除</a>
				</div>
			);
		}else if(field === 'product_name'){
			var role = data['role'];
			var img = <img className="product-img" src={data['image_path']} style={{width:'60px',height:'60px',marginRight:'10px'}}></img>
			if(role == 3){
				return(
					<span className="product-name">
						{img}
						<a title={value} href={'/product/new_product/?id='+data.id}>{value}</a>
					</span>
				)
			}else{
				return(
					<span className="product-name">
						{img}
						<a title={value} style={{cursor:'default',textDecoration:'none'}}>{value}</a>
					</span>
				)
			}
		} else {
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
						<Reactman.TableActionButton text="添加新商品" icon="plus" onClick={this.onValidateAddProduct}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="商品信息" field="product_name" width="400px"/>
						<Reactman.TableColumn name="结算价" field="clear_price" />
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