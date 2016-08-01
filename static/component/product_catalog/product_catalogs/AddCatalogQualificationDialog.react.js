/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:AddCatalogQualificationDialog');

var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogQualificationDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var catalog_id = this.props.data.catalog_id;
		return {
			catalog_id: catalog_id
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
	onClickAddModel: function(event) {
		var html = '<div class="add_model-btn"><div class="form-group ml15"><label class="col-sm-2 control-label xui-mandatory" for="qualification_name">资质名称:</label><div class="col-sm-5"><input type="text" class="form-control" id="qualification_name" name="qualification_name" data-validate="require-notempty" value=""><div class="errorHint"></div></div></div><a class="btn btn-default ml20" onClick={this.onClickDelete}><span class="glyphicon glyphicon-remove"></span></a></div>';
		$('.add_model').append(html);
	},
	onBeforeCloseDialog: function() {
		var qualification_name = this.state.qualification_name;
		if(qualification_name.length>48){
			Reactman.PageAction.showHint('error', '资质名称不能超过48个字符');
			return;
		}
	},
	onClickDelete: function(event) {
		console.log(event);
		console.log(this);
		if (this.props.onDelete) {
			this.props.onDelete(this.props.index);
		}
	},
	render:function(){
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15 add_model">
				<fieldset>
					<div className='add_model-btn'>
						<Reactman.FormInput label="资质名称:" name="qualification_name" validate="require-notempty" value={this.state.qualification_name} onChange={this.onChange} />
						<a className="btn btn-default ml20" onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></a>
					</div>
				</fieldset>
			</form>
			<a className="ml15" onClick={this.onClickAddModel}>+ 添加资质</a>
		</div>
		)
	}
})
module.exports = AddCatalogQualificationDialog;