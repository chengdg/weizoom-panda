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
		Reactman.Resource.get({
			resource: 'product_catalog.get_all_first_catalog',
			data: {},
			success: function(data) {
				var options = data.rows;
				Reactman.PageAction.showDialog({
					title: "添加/修改分类",
					component: AddCatalogDialog,
					data: {
						catalog_id: catalog_id,
						father_catalog: father_catalog,
						catalog_name: catalog_name,
						note: note,
						options: options
					},
					success: function() {
						Action.updateCatalogs();
					}
				});
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			},
			scope: this
		})
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

	showSecondCatalogs:function(class_name){
		var display = document.getElementsByClassName(class_name)[0].style.display;
		if (display == 'none'){
			document.getElementsByClassName(class_name)[0].style.display = "block";
		}else{
			document.getElementsByClassName(class_name)[0].style.display = "none";
		}
	},
	
	rowFormatter: function(field, value, data) {
		if (field === 'expand-row') {
			var _this = this;
			var class_name = 'data-' +data['id'];
			var second_catalogs = JSON.parse(data['second_catalogs'])
			if(second_catalogs.length>0){
				var catalogs = second_catalogs.map(function(catalog,index){
					var catalog_id = catalog['id'];
					var src = '/product/product_relation/?second_catalog_id='+catalog_id;
				return(
						<div style={{backgroundColor: '#EFEFEF',height: '50px',lineHeight: '50px'}} key={index}>
							<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'15px',width: '44%',height: '50px'}}>{catalog.catalog_name} </div>
							<div className="xui-expand-row-info" style={{display: 'inline'}}>创建时间：{catalog.created_at}</div>
							<div className="xui-expand-row-info" style={{marginLeft:'5%',display: 'inline'}}>
								商品数：<a href={src} target="_blank">{catalog.products_number}</a>
							</div>
							<div className="xui-expand-row-info" style={{float:'right',paddingRight:'24px',display:'inline'}}>
								<a className="btn btn-primary" onClick={_this.onAddCatalog} data-id={catalog.id} data-father-catalog={catalog.father_catalog} data-catalog-name={catalog.catalog_name} data-note={catalog.note}>修改</a>
								<a className="btn btn-danger ml10" onClick={_this.onClickDelete} data-id={catalog.id}>删除</a>
							</div>
						</div>
					)
				});
				return (
					<div className={class_name} style={{display:'none'}}>{catalogs}</div>
				)
			}else{
				return (
					<div className={class_name} style={{backgroundColor: '#EFEFEF',height: '50px',lineHeight: '50px',display:'none'}}>
						<div style={{float: 'left',paddingLeft:'15px'}}>暂无二级分类</div>
					</div>
				)
			}
			
		}else if(field === 'products_number'){
			var catalog_id = data['id'];
			var src = '/product/product_relation/?first_catalog_id='+catalog_id;
			return (
				<a href={src} target="_blank">{value}</a>
			)
		}else if(field === 'action'){
			return (
				<div className="orders-list-btn-group">
					<a className="btn btn-primary" onClick={this.onAddCatalog} data-id={data.id} data-father-catalog={data.father_catalog} data-catalog-name={data.catalog_name} data-note={data.note}>修改</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-id={data.id}>删除</a>
				</div>
			);
		}else if(field === 'catalog_name'){
			var class_name = 'data-' +data['id'];
			return (
				<a href="javascript:void(0);" onClick={this.showSecondCatalogs.bind(this,class_name)}>{value}</a>
			)
		}else{
			return value;
		}
	},
	render:function(){
		var catalogsResource = {
			resource: 'product_catalog.product_catalogs',
			data: {}
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
						<Reactman.TableColumn name="操作" field="action" width='150px'/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductCatalogPage;