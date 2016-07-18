/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_model:AddProductModelValueDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddProductModelValueDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	productRelationSave: function(){
		var relations = Store.getData();
		var hasProp = false;  
		for (var prop in relations){  
			hasProp = true;  
			break;  
		}
		if(!hasProp){
			Reactman.PageAction.showHint('error', "请输入关联的云商通商品ID");
			return;
		}
		Action.saveProductRelation(relations,this.state.product_id)
	},

	productRelationCancle: function(){
		this.closeDialog();
	},

	render:function(){
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormInput label="名称:" type="text" name="model_value" value={this.state.model_value} onChange={this.onChange} validate="require-string" />
						<Reactman.FormImageUploader label="图片:" name="images" value={this.state.images} onChange={this.onChange} validate="require-string"/>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddProductModelValueDialog;