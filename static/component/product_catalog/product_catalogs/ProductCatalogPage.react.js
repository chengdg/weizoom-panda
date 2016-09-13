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
var AddCatalogQualificationDialog = require('./AddCatalogQualificationDialog.react');
var AddLabelDialog = require('./AddLabelDialog.react');
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

	// componentDidMount: function(){
	// 	Action.getLabels();
	// },

	onAddCatalog: function(event) {
		var catalogId = event.target.getAttribute('data-id');
		var fatherCatalog = event.target.getAttribute('data-father-catalog');
		var catalogName = event.target.getAttribute('data-catalog-name');
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
						catalogId: catalogId,
						fatherCatalog: fatherCatalog,
						catalogName: catalogName,
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

	onAddQualification: function(event) {
		var catalogId = event.target.getAttribute('data-id');
		var qualificationInfos = event.target.getAttribute('data-qualification-info');
		Reactman.PageAction.showDialog({
			title: "配置特殊资质文件",
			component: AddCatalogQualificationDialog,
			data: {
				catalogId: catalogId,
				qualificationInfos: qualificationInfos
			},
			success: function() {
				Action.updateCatalogs();
			}
		});
	},

	onAddLabel: function(event){
		var catalogId = event.target.getAttribute('data-id');
		var productId = -1;
		Action.getCatalogHasLabel(catalogId, productId);//获取已经配置好的分类标签
		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "配置标签",
				component: AddLabelDialog,
				data: {
					catalogId: catalogId,
					productId: productId
				},
				success: function() {
					Action.updateLabels();
				}
			});
		},100)
	},

	onClickDelete: function(event) {
		var catalogId = parseInt(event.target.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除该商品分类吗?',
			confirm: _.bind(function() {
				Action.deleteCatalog(catalogId);
			}, this)
		});
	},

	showSecondCatalogs:function(className){
		var display = document.getElementsByClassName(className)[0].style.display;
		if (display == 'none'){
			document.getElementsByClassName(className)[0].style.display = "block";
		}else{
			document.getElementsByClassName(className)[0].style.display = "none";
		}
	},
	
	rowFormatter: function(field, value, data) {
		if (field === 'expand-row') {
			var _this = this;
			var className = 'data-' +data['id'];
			var secondCatalogs = JSON.parse(data['secondCatalogs']);
			if(secondCatalogs.length > 0){
				var catalogs = secondCatalogs.map(function(catalog,index){
					var catalogId = catalog['id'];
					var src = '/product/product_relation/?second_catalog_id='+catalogId;
					var hasInfo = catalog['qualificationId2name'];
					var hasLabel = catalog['has_label'];
					// {hasLabel? <a className="btn btn-info ml10" style={{width:'110px'}} onClick={_this.onAddLabel} data-id={catalog.id}>已配置标签</a>: <a className="btn btn-primary ml10" style={{width:'110px'}} onClick={_this.onAddLabel} data-id={catalog.id}>配置标签</a>}
					return(
						<div style={{backgroundColor: '#EFEFEF',height: '50px',lineHeight: '50px'}} key={index}>
							<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'15px',width: '44%',height: '50px'}}>{catalog.catalogName} </div>
							<div className="xui-expand-row-info" style={{display: 'inline'}}>{catalog.createdAt}</div>
							<div className="xui-expand-row-info" style={{marginLeft:'5%',display: 'inline'}}>
								商品数：<a href={src} target="_blank">{catalog.productsNumber}</a>
							</div>
							<div className="xui-expand-row-info" style={{float:'right',paddingRight:'24px',display:'inline'}}>
								<a className="btn btn-primary" onClick={_this.onAddCatalog} data-id={catalog.id} data-father-catalog={catalog.fatherCatalog} data-catalog-name={catalog.catalogName} data-note={catalog.note}>修改</a>
								<a className="btn btn-danger ml10" onClick={_this.onClickDelete} data-id={catalog.id}>删除</a>
								{hasInfo == '[]'? <a className="btn btn-primary ml10" onClick={_this.onAddQualification} data-id={catalog.id} data-qualification-info={catalog.qualificationId2name}>配置特殊资质</a>: <a className="btn btn-info ml10" style={{width:'110px'}} onClick={_this.onAddQualification} data-id={catalog.id} data-qualification-info={catalog.qualificationId2name}>已配置资质</a>}
								
							</div>
						</div>
					)
				});

				return (
					<div className={className} style={{display:'none'}}>{catalogs}</div>
				)
			}else{
				return (
					<div className={className} style={{backgroundColor: '#EFEFEF',height: '50px',lineHeight: '50px',display:'none'}}>
						<div style={{float: 'left',paddingLeft:'15px'}}>暂无二级分类</div>
					</div>
				)
			}
			
		}else if(field === 'productsNumber'){
			var catalogId = data['id'];
			var src = '/product/product_relation/?first_catalog_id='+catalogId;
			return (
				<a href={src} target="_blank">{value}</a>
			)
		}else if(field === 'action'){
			return (
				<div className="orders-list-btn-group">
					<a className="btn btn-primary" onClick={this.onAddCatalog} data-id={data.id} data-father-catalog={data.fatherCatalog} data-catalog-name={data.catalogName} data-note={data.note}>修改</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-id={data.id}>删除</a>
				</div>
			);
		}else if(field === 'catalogName'){
			var className = 'data-' +data['id'];
			return (
				<a href="javascript:void(0);" onClick={this.showSecondCatalogs.bind(this,className)}>{value}</a>
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
						<Reactman.TableColumn name="分类名称" field="catalogName" />
						<Reactman.TableColumn name="创建时间" field="createdAt" width='200px'/>
						<Reactman.TableColumn name="商品数" field="productsNumber"/>
						<Reactman.TableColumn name="操作" field="action" width='150px'/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductCatalogPage;