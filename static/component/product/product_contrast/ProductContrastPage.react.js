/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:ProductContrastPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var ProductModelInfo = require('./ProductModelInfo.react');
var OldProductModelInfo = require('./OldProductModelInfo.react');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var ProductContrastPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	render:function(){
		var catalogName = W.catalogName;
		if(this.state.catalog_name.length>0){
			catalogName = this.state.catalog_name;
		}

		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]
		var role = W.role;
		var disabled = role == 3 ? 'disabled' : '';
		console.log(this.state.remark,'+========')
		return (
			<div className="xui-newProduct-page xui-formPage">
				<OldProduct />
				<form className="form-horizontal mt15">
					<fieldset>
						<legend className="pl10 pt10 pb10">修改后信息</legend>
						<span className="form-group ml15">
							<label className="col-sm-2 control-label pr0">商品类目:</label>
							<span className="xui-catalog-name">{catalogName}</span>
						</span>
						<Reactman.FormInput label="商品名称:" type="text" readonly={disabled} name="product_name" value={this.state.product_name} />
						<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="promotion_title" value={this.state.promotion_title} />
						<Reactman.FormRadio label="多规格商品:" type="text" name="has_product_model" value={this.state.has_product_model} options={optionsForModel} />
						<div> <ProductModelInfo Disabled={disabled} onChange={this.onChange} Modeltype={this.state.has_product_model}/> </div>	
						<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} />
						<Reactman.FormRichTextInput label="商品描述:" name="remark" value={this.state.remark} width="800" height="250" />
					</fieldset>
				</form>
			</div>
		)
	}
})

var OldProduct = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	render:function(){
		var catalogName = W.catalogName;
		if(this.state.old_catalog_name.length>0){
			catalogName = this.state.old_catalog_name;
		}

		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]
		var role = W.role;
		var disabled = role == 3 ? 'disabled' : '';

		var oldProductName = this.state.old_product_name.length>0?this.state.old_product_name: this.state.product_name;
		var oldPromotionTitle = this.state.old_promotion_title.length>0?this.state.old_promotion_title: this.state.promotion_title;
		var oldRemark = this.state.old_remark.length>0?this.state.old_remark: this.state.remark;
		console.log(this.state.old_remark,'+========')
		var hasProductModel = this.state.old_has_product_model;
		
		return (
			<form className="form-horizontal mt15">
				<fieldset>
					<legend className="pl10 pt10 pb10">修改前信息</legend>
					<span className="form-group ml15">
						<label className="col-sm-2 control-label pr0">商品类目:</label>
						<span className="xui-catalog-name">{catalogName}</span>
					</span>
					<Reactman.FormInput label="商品名称:" type="text" readonly={disabled} name="old_product_name" value={oldProductName} />
					<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="old_promotion_title" value={oldPromotionTitle}  />
					<Reactman.FormRadio label="多规格商品:" type="text" name="old_has_product_model" value={hasProductModel} options={optionsForModel} />
					<div> <OldProductModelInfo Disabled={disabled} Modeltype={hasProductModel}/> </div>	
					<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} onChange={this.onChange} validate="require-string"/>
					<Reactman.FormRichTextInput label="商品描述:" name="old_remark" value={this.state.remark} width="800" height="250" />
				</fieldset>
			</form>
		)
	}
})

module.exports = ProductContrastPage;