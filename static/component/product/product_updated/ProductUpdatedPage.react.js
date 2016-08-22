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

	onConfirmFilter: function(data){
		Action.filterDatas(data);
	},

	updateSyncProduct: function(product_id, event) {
		var title = '确定更新么?';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.updateSyncProduct(String(product_id));
			}, this)
		});
	},

	batchUpdateSyncProduct: function(event) {
		var productIds = _.pluck(this.refs.table.getSelectedDatas(), 'id');
		if (productIds.length == 0){
			Reactman.PageAction.showHint('error', '请先选择要更新的商品!');
			return false;
		}

		var title = '确定更新么?';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.updateSyncProduct(productIds.join(","));
			}, this)
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.updateSyncProduct.bind(this,data['id'])}>商品更新</a><br></br>
					<a className="btn btn-link btn-xs" >驳回修改</a>
				</div>
			);
		}else if(field === 'product_name'){
			var _this = this;
			var colorStyle = data['is_update']? {color: 'red'}: {};
			var img = <img className="product-img" src={data['image_path']} style={{width:'60px',height:'60px',marginRight:'10px'}}></img>
			return(
				<span className="product-name">
					{img}
					<a title={value} style={colorStyle} href={'/product/new_product/?id='+data.id}>{value}</a>
				</span>
			)
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
						<Reactman.TableActionButton text="批量更新" onClick={this.batchUpdateSyncProduct}/>
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