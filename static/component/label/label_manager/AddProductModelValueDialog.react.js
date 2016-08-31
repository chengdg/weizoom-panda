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
		return {
			'images': [],
			'model_value': '',
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onSubmit: function(){
		var _this = this;
		var model_id = this.props.data.model_id;
		var model_type = this.props.data.model_type;
		var model_value = this.state.model_value;
		var images = this.state.images;
		if(model_type==1 && images.length==0){
			Reactman.PageAction.showHint('error', '请上传图片');
			return;
		}
		if(images.length>1){
			Reactman.PageAction.showHint('error', '最多上传一张图片!');
			return;
		}
		var path = images.length>0?images[0]['path']:''
		Action.saveProductModelValue(model_id,model_value,path);
		setTimeout(function() {
		 	_this.closeDialog();
		}, 500);
	},

	render:function(){
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormInput label="名称:" type="text" name="model_value" value={this.state.model_value} onChange={this.onChange} validate="require-string" />
						<Reactman.FormImageUploader label="图片:" name="images" value={this.state.images} onChange={this.onChange} validate="require-string"/>
						<span style={{marginLeft:'180px',fontSize:'10px'}}>
							上传图片建议尺寸60*60
						</span>
					</fieldset>
					<fieldset>
						<Reactman.FormSubmit onClick={this.onSubmit} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddProductModelValueDialog;