/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:AddCatalogDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var catalog_id = this.props.data.catalog_id;
		if(this.props.data.father_catalog){
			var father_catalog = this.props.data.father_catalog;
		}else{
			var father_catalog = '-1';
		}
		var catalog_name = this.props.data.catalog_name;
		var note = this.props.data.note;
		var options = this.props.data.options;
		return {
			catalog_id: catalog_id,
			father_catalog: father_catalog,
			catalog_name: catalog_name,
			note: note,
			options: options
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		if(property == 'father_catalog'){
			if(!this.props.data.catalog_id){
				this.setState(newState);
			}
		}else{
			this.setState(newState);
		}
		
	},

	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState({
			father_catalog: infomations['father_catalog'],
			catalog_name: infomations['catalog_name'],
			note: infomations['note']
		})
	},

	onBeforeCloseDialog: function() {
		if (this.state.catalog_id){
			Reactman.Resource.post({
				resource: 'product_catalog.product_catalogs',
				data: {
					catalog_id: this.state.catalog_id,
					catalog_name: this.state.catalog_name,
					note: this.state.note
				},
				success: function() {
					Reactman.PageAction.showHint('success', '编辑分类成功');
					this.closeDialog();
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}else{
			Reactman.Resource.put({
				resource: 'product_catalog.product_catalogs',
				data: {
					father_catalog: this.state.father_catalog,
					catalog_name: this.state.catalog_name,
					note: this.state.note
				},
				success: function() {
					Reactman.PageAction.showHint('success', '新建分类成功');
					this.closeDialog();
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}
	},

	render:function(){
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormSelect disabled='true' label="上级分类:" name="father_catalog" value={this.state.father_catalog} options={this.state.options} onChange={this.onChange}/>
					<Reactman.FormInput label="分类名称:" name="catalog_name" validate="require-notempty" value={this.state.catalog_name} onChange={this.onChange} />
					<Reactman.FormText label="备注:" type="text" name="note" value={this.state.note} onChange={this.onChange} inDialog={true} width={300} height={200}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = AddCatalogDialog;