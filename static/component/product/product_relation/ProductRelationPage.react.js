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
var Constant = require('./Constant');
var Action = require('./Action');

var ChooseSyncSelfShopDialog = require('./ChooseSyncSelfShopDialog.react');
var AddLabelDialog = require('../.././product_catalog/product_catalogs/AddLabelDialog.react');
var ProductCatalogAction = require('../.././product_catalog/product_catalogs/Action');
require('./ProductRelation.css');

var ProductRelationPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getFilter();
		this.refs.table.refresh(filterOptions);  
	},

	componentDidMount: function() {
		ProductCatalogAction.getLabels();
	},

	chooseSyncSelfShop: function(productId) {
		Action.getHasSyncShop(productId);

		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "选择平台进行同步商品",
				component: ChooseSyncSelfShopDialog,
				data: {
					product_id: String(productId),
					sync_type: 'single'
				},
				success: function(inputData, dialogState) {
					console.log("success");
				}
			});
		},100)
	},

	batchSyncProduct: function() {
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

	onClickDelete: function(productId, event) {
		var title = '确定删除么?';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.deleteProduct(productId);
			}, this)
		});
	},

	onAddLabel: function(event) {
		var catalogId = event.target.getAttribute('data-catalog-id');
		var productId = event.target.getAttribute('data-id');
		ProductCatalogAction.getCatalogHasLabel(catalogId, productId);//获取已经配置好的分类标签

		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "配置标签",
				component: AddLabelDialog,
				data: {
					catalogId: catalogId,
					productId: productId
				},
				success: function() {
					Action.updateDatas();
				}
			});
		},300)
	},

	rowFormatter: function(field, value, data) {
		if(field === 'product_name'){
			var colorStyle = data['is_update']? {color: 'red'}: {};

			return(
				<a className="btn btn-link btn-xs" style={colorStyle} href={'/product/new_product/?id='+data.id}>{value}</a>
			)
		} else if(field === 'action'){
			if(data['product_status_value']==0){
				return(
					<div>
						<a className="btn btn-link btn-xs" onClick={this.chooseSyncSelfShop.bind(this,data['id'])}>同步商品</a>
						<a className="btn btn-link btn-xs" onClick={this.onClickDelete.bind(this,data['id'])}>删除商品</a>
					</div>
				)
			}else{
				return(
					<a className="btn btn-link btn-xs" onClick={this.chooseSyncSelfShop.bind(this,data['id'])}>同步商品</a>
				)
			}	
		}else if (field === 'catalog_name') {
			var name = data['second_level_name'];
			var line =name.length>0?'-':'';

			return (
				<div>
					<span>{data['first_level_name']}</span><br></br>
					<span style={{paddingLeft:'10px'}}>{line}{data['second_level_name']}</span>
				</div>
			);
		}
		else if(field === 'expand-row'){
			var labelNames = data['labelNames'];
			var catalogId = data['catalogId'];
			var labelNameLi = '';

			if(labelNames.length>0){
				labelNameLi = JSON.parse(labelNames).map(function(labelName, index){
					return(
						<li className='xui-label-name-li' key={index}>{labelName.name} ;</li>
					)
				})
			}

			var catalogManager = catalogId != 0? <li style={{display:'inline-block'}}><a href='javascript:void(0);' onClick={this.onAddLabel} data-catalog-id={data.catalogId} data-id={data.id}>配置标签</a></li>: '';
			return (
				<div>
					<ul style={{height: '30px'}}>
						{labelNameLi}
						{catalogManager}
					</ul>
				</div>
			)
		}
		else {
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
			<div className="mt15 xui-product-productRelationPage">
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
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="商品分类:" name="catalog_query" match='=' />
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
						<Reactman.TableColumn name="分类" field="catalog_name" />
						<Reactman.TableColumn name="来源" field="customer_from_text" />
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