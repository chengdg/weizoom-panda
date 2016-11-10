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
		var catalogId = this.props.data.catalogId;
		if(this.props.data.fatherCatalog){
			var fatherCatalog = this.props.data.fatherCatalog;
		}else{
			var fatherCatalog = '-1';
		}
		var catalogName = this.props.data.catalogName;
		var note = this.props.data.note;
		var options = this.props.data.options;
		return {
			catalogId: catalogId,
			fatherCatalog: fatherCatalog,
			catalogName: catalogName,
			note: note,
			options: options
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		if(property == 'fatherCatalog'){
			if(!this.props.data.catalogId){
				this.setState(newState);
			}
		}else{
			this.setState(newState);
		}
		
	},

	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState({
			fatherCatalog: infomations['fatherCatalog'],
			catalogName: infomations['catalogName'],
			note: infomations['note']
		})
	},

	onBeforeCloseDialog: function() {
		var catalogName = this.state.catalogName;
		if(catalogName.length>48){
			Reactman.PageAction.showHint('error', '分类名称不能超过48个字符');
			return;
		}
		if (this.state.catalogId){
			Reactman.Resource.post({
				resource: 'product_catalog.product_catalogs',
				data: {
					catalog_id: this.state.catalogId,
					catalog_name: this.state.catalogName,
					note: this.state.note
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '编辑分类成功');
					},500);
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
					father_catalog: this.state.fatherCatalog,
					catalog_name: this.state.catalogName,
					note: this.state.note
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '新建分类成功');
					},500);
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
					<Reactman.FormSelect label="上级分类:" name="fatherCatalog" value={this.state.fatherCatalog} options={this.state.options} onChange={this.onChange}/>
					<Reactman.FormInput label="分类名称:" name="catalogName" validate="require-notempty" value={this.state.catalogName} onChange={this.onChange} />
					<Reactman.FormText label="备注:" type="text" name="note" value={this.state.note} onChange={this.onChange} inDialog={true} width={300} height={200}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = AddCatalogDialog;