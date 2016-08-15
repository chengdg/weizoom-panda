/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_relation:ProductRelationPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var Reactman = require('reactman');

var Store = require('./Store');
var FilterStore = require('./FilterStore');
var Constant = require('./Constant');
var Action = require('./Action');

var ChooseSyncSelfShopDialog = require('./ChooseSyncSelfShopDialog.react');

var ProductRelationPage = React.createClass({
	getInitialState: function() {
		return ({});
	},

	onChangeFilterStore: function(event) {
		var filterOptions = FilterStore.getFilter();
		this.refs.table.refresh(filterOptions); 
	},

	onChangeStore: function(event) {
		this.setState(Store.getData());
	},

	componentDidMount: function() {
		FilterStore.addListener(this.onChangeFilterStore);
		Store.addListener(this.onChangeStore);
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
		if(field === 'product_name'){
			return(
				<a className="btn btn-link btn-xs" href={'/product/new_product/?id='+data.id}>{value}</a>
			)
		} else if(field === 'action'){
			return(
				<a className="btn btn-link btn-xs" onClick={this.chooseSyncSelfShop.bind(this,data['id'])}>同步商品</a>
			)
		}else {
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDatas(data);
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_relation',
			data: {
				page: 1,
				first_catalog_id: W.first_catalog_id,
				second_catalog_id: W.second_catalog_id
			}
		};
		var optionsForProductStatus = [{text: '全部', value: '0'},{text: '已同步', value: '1'},{text: '未同步', value: '2'}];
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="客户名称:" name="customer_name_query" match='=' />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormInput label="商品名称:" name="product_name_query" match="=" />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormSelect label="状态:" name="product_status_query" options={optionsForProductStatus} match="=" />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="批量同步" onClick={this.batchSyncProduct}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} enableSelector={true} ref="table">
						<Reactman.TableColumn name="商品名称" field="product_name" />
						<Reactman.TableColumn name="客户名称" field="customer_name" />
						<Reactman.TableColumn name="总销量" field="total_sales" />
						<Reactman.TableColumn name="状态" field="product_status" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductRelationPage;