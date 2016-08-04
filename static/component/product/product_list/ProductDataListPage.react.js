/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_list:ProductDataListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var AddProductCategoryDialog = require('./AddProductCategoryDialog.react');
var LookProductModelDetail = require('./LookProductModelDetail.react');

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

	lookProductModelDetail: function(product_id,value){
		Action.lookProductModelDetail(product_id);
		Reactman.PageAction.showDialog({
			title: value,
			component: LookProductModelDetail,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	onValidateAddProduct: function(){
		// Action.ProductCategory();
		// Reactman.PageAction.showDialog({
		// 	title: "请选择商品分类",
		// 	component: AddProductCategoryDialog,
		// 	data: {},
		// 	success: function(inputData, dialogState) {
		// 		console.log("success");
		// 	}
		// });
		W.gotoPage('/product/new_product/?second_level_id='+0);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" target="_blank" href={'/product/new_product/?id='+data.id}>编辑</a>
				</div>
			);
		}else if(field === 'product_name'){
			var _this = this;
			var role = data['role'];
			var product_has_model = data['product_has_model'];
			var img = <img className="product-img" src={data['image_path']} style={{width:'60px',height:'60px',marginRight:'10px'}}></img>
			var isModel = data['is_model'];
			if(role == 3){
				if(product_has_model>0){
					return(
						<span className="product-name">
							{img}
							<a title={value} href={'/product/new_product/?id='+data.id}>{value}</a>
							{isModel==true?<a href='javascript:void(0);' className='product-model-detail' onClick={_this.lookProductModelDetail.bind(_this,data.id,value)}>查看{product_has_model}个规格详情</a>:''} 
						</span>
					)
				}else{
					return(
						<span className="product-name">
							{img}
							<a title={value} href={'/product/new_product/?id='+data.id}>{value}</a>
						</span>
					)
				}
				
			}else{
				if(product_has_model>0){
					return(
						<span className="product-name">
							{img}
							<a title={value} style={{cursor:'default',textDecoration:'none'}}>{value}</a>
							{isModel==true?<a href='javascript:void(0);' className='product-model-detail' onClick={_this.lookProductModelDetail.bind(_this,data.id,value)}>查看{product_has_model}个规格详情</a>:''} 
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
			resource: 'product.product_list',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="商品名称:" name="product_name_query" match="=" />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="导出商品" onClick={this.onExport}/>
						<Reactman.TableActionButton text="添加新商品" icon="plus" onClick={this.onValidateAddProduct}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="商品信息" field="product_name" width="400px"/>
						<Reactman.TableColumn name="结算价(元)" field="clear_price" />
						<Reactman.TableColumn name="售价(元)" field="product_price" />
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