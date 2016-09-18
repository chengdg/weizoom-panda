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
		var qualificationInfos = JSON.parse(this.props.data.qualificationInfos);
		var catalogId = this.props.data.catalogId;
		return {
			'models': qualificationInfos,
			qualificationInfos: qualificationInfos,
			name: qualificationInfos,
			catalogId: catalogId
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
		Action.addCatalogQualification(this.state.qualificationInfos);
	},
	onDeleteModel: function(index) {
		Action.deleteCatalogQualification(index,this.state.qualificationInfos);
	},
	onBeforeCloseDialog: function() {
		Reactman.Resource.put({
			resource: 'product_catalog.qualification',
			data: {
                catalog_id: this.state.catalogId,
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
		var models = this.state.qualificationInfos;
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