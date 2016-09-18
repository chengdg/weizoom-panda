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
var AddLimitZoneTemplateDialog = require('./AddLimitZoneTemplateDialog.react');
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

	componentDidMount: function(){
		Action.getLabels();
	},

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

		Reactman.PageAction.showDialog({
			title: "配置特殊资质文件",
			component: AddCatalogQualificationDialog,
			data: {

			},
			success: function() {
			}
		});
	},

	onAddTemplate: function(event){
	    var template_id = event.target.getAttribute('data-id');
	    var name = event.target.getAttribute('data-name');
		Reactman.PageAction.showDialog({
			title: "禁售/仅售模板",
			component: AddLimitZoneTemplateDialog,
			data: {
                id: template_id,
                name: name
			},
			success: function() {
			}
		});
	},

	onClickDelete: function(event) {
		var template_id = parseInt(event.target.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除该商品分类吗?',
			confirm: _.bind(function() {
				Action.deleteCatalog(template_id);
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

        if(field=='action'){
            return (
                <div className="orders-list-btn-group">
					<a className="btn btn-primary" onClick={this.onAddTemplate}
					    data-id={data.id}
					    data-name={data.name} >修改</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-id={data.id}>删除</a>
				</div>
            )
        }
		return value;
	},
	render:function(){
		var catalogsResource = {
			resource: 'limit_zone.template_list',
			data: {}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加模板" icon="plus" onClick={this.onAddTemplate}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={catalogsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="模板名称" field="name" width='150px'/>
						<Reactman.TableColumn name="地区" field="zone_info" />
						<Reactman.TableColumn name="操作" field="action" width='150px'/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductCatalogPage;