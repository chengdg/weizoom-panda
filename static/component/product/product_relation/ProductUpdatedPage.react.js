/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_list:ProductUpdatedPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var ChooseSyncSelfShopDialog = require('./ChooseSyncSelfShopDialog.react');
require('./style.css');
var W = Reactman.W;

var ProductUpdatedPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getFilter();
		this.refs.table.refresh(filterOptions);
	},

	chooseSyncSelfShop: function(product_id){
		Action.getHasSyncShop(product_id);

		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "选择平台进行同步商品",
				component: ChooseSyncSelfShopDialog,
				data: {
					product_id: String(product_id),
					sync_type: 'single'
				},
				success: function(inputData, dialogState) {
					console.log("success");
				}
			});
		},100)
	},

	batchSyncProduct: function(){
		//取消选中的平台
		Action.cancleSelectSyncProduct();
		var productIds = _.pluck(this.refs.table.getSelectedDatas(), 'id');
		if (productIds.length == 0){
			Reactman.PageAction.showHint('error', '请先选择要同步的商品!');
			return false;
		}

		Reactman.PageAction.showDialog({
			title: "选择平台进行同步商品",
			component: ChooseSyncSelfShopDialog,
			data: {
				product_id: productIds.join(","),
				sync_type: 'batch'
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.chooseSyncSelfShop.bind(this,data['id'])}>商品更新</a><br></br>
					<a className="btn btn-link btn-xs" >驳回修改</a>
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
		} else if (field === 'catalog_name') {
			var name = data['second_level_name'];
			var line =name.length>0?'-':''
			return (
				<div>
					<span>{data['first_level_name']}</span><br></br>
					<span style={{paddingLeft:'10px'}}>{line}{data['second_level_name']}</span>
				</div>
			);
		} else {
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_list',
			data: {
				page: 1,
				is_update: true
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="商品名称:" name="product_name_query" match="=" />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormInput label="商品分类:" name="catalog_query" match='=' />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="批量同步" onClick={this.batchSyncProduct}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} enableSelector={true} ref="table">
						<Reactman.TableColumn name="商品信息" field="product_name" width="400px"/>
						<Reactman.TableColumn name="分类" field="catalog_name" />
						<Reactman.TableColumn name="结算价(元)" field="clear_price" />
						<Reactman.TableColumn name="售价(元)" field="product_price" />
						<Reactman.TableColumn name="销量" field="sales" />
						<Reactman.TableColumn name="状态" field="status" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductUpdatedPage;