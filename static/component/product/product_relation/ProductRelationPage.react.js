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

	chooseSyncSelfShop: function(productId, productStatus) {
		Action.getHasSyncShop(productId);

		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "选择平台进行同步商品",
				component: ChooseSyncSelfShopDialog,
				data: {
					product_id: String(productId),
					product_status: productStatus,
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

	showRevokeReason: function(event){
		var revokeReasons = event.target.getAttribute('data-product-reasons');
		Reactman.PageAction.showPopover({
			target: event.target,
			content: '<span style="color:red">' + revokeReasons + '</span>'
		});
	},

	hideRevokeReason: function(event) {
		Reactman.PageAction.hidePopover();
	},

	rowFormatter: function(field, value, data) {
		if(field === 'product_name'){
			var colorStyle = data['is_update']? {color: 'red'}: {};

			return(
				<a className="btn btn-link btn-xs" style={colorStyle} href={'/product/new_product/?id='+data.id}>{value}</a>
			)
		} else if(field === 'action'){
			if(data['product_status_value']==0){
				//未同步
				return(
					<div>
						<a className="btn btn-primary" onClick={this.chooseSyncSelfShop.bind(this, data['id'], data['product_status_value'])}>同步商品</a>
						<a className="btn btn-primary ml10" onClick={this.onClickDelete.bind(this,data['id'])}>驳回修改</a>
						<a className="btn btn-danger mt5" onClick={this.onClickDelete.bind(this,data['id'])}>删除商品</a>
					</div>
				)
			}else if(data['product_status_value']==1){
				//已入库,已同步
				return(
					<div>
						<a className="btn btn-primary" onClick={this.chooseSyncSelfShop.bind(this,data['id'], data['product_status_value'])}>同步商品</a>
					</div>
				)
			}else{
				//已入库,已停售
				return(
					<div>
						<a className="btn btn-primary" onClick={this.chooseSyncSelfShop.bind(this,data['id'], data['product_status_value'])}>同步商品</a>
						<a className="btn btn-danger ml10" onClick={this.onClickDelete.bind(this,data['id'])}>删除商品</a>
					</div>
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
		}else if(field === 'expand-row'){
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

			return (
				<div>
					<ul style={{height: 'auto'}}>
						{labelNameLi}
						<li style={{display:'inline-block'}}><a href='javascript:void(0);' onClick={this.onAddLabel} data-catalog-id={data.catalogId} data-id={data.id}>配置标签</a></li>
					</ul>
				</div>
			)
		}else if (field === 'product_status') {
			var name = data['product_status_value'];
			if(data['product_status_value'] == 2){
				return (
					<a href="javascript:void(0);" onMouseOut={this.hideRevokeReason} onMouseOver={this.showRevokeReason} data-product-reasons={data.revoke_reasons}>{data['product_status']}</a>
				)
			}else{
				return (
					<span>{data['product_status']}</span>
				)
			}

		}else {
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDatas(data);
	},

	onExport: function(){
		Action.exportProducts();
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
		var optionsForProductStatus = [{text: '全部', value: '0'},{text: '已入库,已同步', value: '1'},{text: '已入库,已停售', value: '3'},{text: '未同步', value: '2'}];
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
							<Reactman.FormSelect label="入库状态:" name="product_status_query" options={optionsForProductStatus} match="=" />
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
						<Reactman.TableActionButton text="导出商品" onClick={this.onExport}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} enableSelector={true} ref="table">
						<Reactman.TableColumn name="商品名称" field="product_name" />
						<Reactman.TableColumn name="客户名称" field="customer_name" />
						<Reactman.TableColumn name="分类" field="catalog_name" />
						<Reactman.TableColumn name="来源" field="customer_from_text" />
						<Reactman.TableColumn name="总销量" field="total_sales" />
						<Reactman.TableColumn name="入库状态" field="product_status" />
						<Reactman.TableColumn name="操作" field="action" width='200px' />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductRelationPage;