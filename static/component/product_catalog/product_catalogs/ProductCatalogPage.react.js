/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var AddCatalogDialog = require('./AddCatalogDialog.react');
require('./style.css')

var ProductCatalogPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},
	onAddCatalog: function(event) {
		var catalog_id = event.target.getAttribute('data-id');
		var father_catalog = event.target.getAttribute('data-father-catalog');
		var catalog_name = event.target.getAttribute('data-catalog-name');
		var note = event.target.getAttribute('data-note');
		Reactman.PageAction.showDialog({
			title: "添加/修改分类",
			component: AddCatalogDialog,
			data: {
				catalog_id: catalog_id,
				father_catalog: father_catalog,
				catalog_name: catalog_name,
				note: note,
			},
			success: function() {
				Action.updateCatalogs();
			}
		});
	},
	onClickDelete: function(event) {
		var catalog_id = parseInt(event.target.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除该商品分类吗?',
			confirm: _.bind(function() {
				Action.deleteCatalog(catalog_id);
			}, this)
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'expand-row') {
			var order_infos = data['order_infos'];
			var class_name = 'data-' +data['user_id'];
			if(order_infos){
				var products = JSON.parse(order_infos).map(function(order,index){
					var order_id = order['order_id'];
					var src = '/order/customer_order_detail/?id='+order_id;
					return(
							<div style={{marginTop:'5px'}} key={index}>
								<div className="xui-expand-row-info" style={{float: 'left',width:'190px'}}>
									<a href={src} target="_blank">{order.order_id}</a> 
								</div>
								<div className="xui-expand-row-info" style={{float: 'right',width:'100px'}}>{order.status} </div>
								<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>{order.total_order_money}(元)</div>
								<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>{order.purchase_price}(元)/{order.total_count}(件)</div>
								<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'300px'}}>{order.product_name}</div>
								<div style={{clear:'both'}}></div>
							</div>
						)
					});
				return (
					<div className={class_name} style={{display:'none !important',margin:'5px 0px 5px 5px'}}>
						<div>
							<div className="xui-expand-row-info" style={{float: 'left',width:'190px'}}>订单号<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'right',width:'100px'}}>状态<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>总金额<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>单价/件数<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'300px'}}>商品名称<br></br></div>
							<div style={{clear:'both'}}></div>
							{products}
						</div>
					</div>
				)
			}
		}else if(field === 'action'){
			return (
				<div className="orders-list-btn-group">
					<a className="btn btn-link btn-xs" onClick={this.onAddCatalog} data-id={data.id} data-father-catalog={data.father_catalog} data-catalog-name={data.catalog_name} data-note={data.note}>修改</a>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-id={data.id}>删除</a>
				</div>
			);
		}else{
			return value;
		}
	},
	render:function(){
		var catalogsResource = {
			resource: 'product_catalog.product_catalogs',
			data: {
			}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加分类" icon="plus" onClick={this.onAddCatalog}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={catalogsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="分类名称" field="catalog_name" />
						<Reactman.TableColumn name="创建时间" field="created_at" width='200px'/>
						<Reactman.TableColumn name="商品数" field="products_number"/>
						<Reactman.TableColumn name="操作" field="action" width='100px'/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductCatalogPage;