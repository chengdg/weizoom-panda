/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:AddCatalogQualificationDialog');
var ProductModel = require('./ProductModel.react');
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogQualificationDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var qualification_infos = JSON.parse(this.props.data.qualification_infos);
		var catalog_id = this.props.data.catalog_id;
		return {
			'models': qualification_infos,
			qualification_infos: qualification_infos,
			name: qualification_infos,
			catalog_id: catalog_id
		}
	},
	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},
	onChangeModel: function(value, event) {
		var model = this.state.models[value.index];
		model.name = value.name;
	},
	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState({
			models: infomations['models']
		})
	},
	onClickAddModel: function(event) {
		Action.addCatalogQualification(this.state.qualification_infos);
	},
	onDeleteModel: function(index) {
		Action.deleteCatalogQualification(index,this.state.qualification_infos);
	},
	onBeforeCloseDialog: function() {
		Reactman.Resource.put({
			resource: 'product_catalog.qualification',
			data: {
                catalog_id: this.state.catalog_id,
				qualification_infos: JSON.stringify(this.state.models)
			},
			success: function() {
				this.closeDialog();
				_.delay(function(){
					Reactman.PageAction.showHint('success', '配置资质成功');
				},500);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			},
			scope: this
		})
	},
	render:function(){
		var models = this.state.qualification_infos;
		var cModels = '';
		if (models) {
			var _this = this;
			cModels = models.map(function(model, index) {
				return (
					<ProductModel models={models} model={model} value={name} index={index} key={index} onChange={_this.onChangeModel} onDelete={_this.onDeleteModel} />
				)
			});
		}
		return (
		<div className="xui-formPage">
			{cModels}
			<a className="ml15" onClick={this.onClickAddModel}>+ 添加资质</a>
		</div>
		)
	}
})
module.exports = AddCatalogQualificationDialog;