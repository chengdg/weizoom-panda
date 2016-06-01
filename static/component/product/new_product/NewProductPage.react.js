/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:NewProductPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var ProductPreviewDialog = require('./ProductPreviewDialog.react');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var NewProductPage = React.createClass({
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

	productPreview: function(){
		var product = Store.getData();
		if(product.images.length == 0){
			Reactman.PageAction.showHint('error', '请先上传图片！');
			return;
		}

		if(!product.hasOwnProperty('product_name') || !product.hasOwnProperty('product_price')){
			Reactman.PageAction.showHint('error', '请先填写商品名称和价格！');
			return;
		}
		
		Reactman.PageAction.showDialog({
			title: "商品预览",
			component: ProductPreviewDialog,
			data: {
				product: product
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	onSubmit: function(){
		var product = Store.getData();
		if(product.product_name.length > 30 || product.promotion_title.length > 30){
			Reactman.PageAction.showHint('error', '商品名称或促销标题最多输入30个字,请重新输入!');
			return;
		}
		if(product.images.length == 0){
			Reactman.PageAction.showHint('error', '请先上传图片！');
			return ;
		}
		Action.saveNewProduct(product);
	},

	render:function(){
		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var role = W.role;
		var disabled = role == 3 ? 'disabled' : '';
		return (
			<div className="xui-newProduct-page xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<div className="preview-btn"><a href='javascript:void(0);' onClick={this.productPreview}>商品预览</a></div>
					</fieldset>
					<fieldset>
						<legend className="pl10 pt10 pb10">基本信息</legend>
						<Reactman.FormInput label="商品名称:" type="text" readonly={disabled} name="product_name" value={this.state.product_name} onChange={this.onChange} validate="require-string" placeholder="最多30个字" />
						<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="promotion_title" value={this.state.promotion_title} placeholder="最多30个字" onChange={this.onChange} validate="require-string" />
						<Reactman.FormInput label="商品价格:" type="text" readonly={disabled} name="product_price" value={this.state.product_price} onChange={this.onChange} validate="require-price" />
						<span className="money_note">
							元
						</span>
						<div></div>
						<Reactman.FormInput label="结算价:" type="text" readonly={disabled} name="clear_price" value={this.state.clear_price} onChange={this.onChange} validate="require-price"/>
						<span className="money_note">
							元
						</span>
						<div></div>
						<Reactman.FormInput label="商品重量:" type="text" readonly={disabled} name="product_weight" value={this.state.product_weight} onChange={this.onChange} validate="require-float"/>
						<span className="money_note">
							Kg
						</span>
						<Reactman.FormRadio label="商品库存:" type="text" name="product_store_type" value={this.state.product_store_type} options={optionsForStore} onChange={this.onChange} />
						<div> <StoreInfo onChange={this.onChange} productStore={this.state.product_store} Type={this.state.product_store_type}/> </div>
						<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} onChange={this.onChange} validate="require-string"/>
						<Reactman.FormRichTextInput label="商品描述:" name="remark" value={this.state.remark} width="800" height="250" onChange={this.onChange} validate="require-notempty"/>
					</fieldset>
					<fieldset>
						{role == 3? '': <Reactman.FormSubmit onClick={this.onSubmit} />}
					</fieldset>
				</form>
			</div>
		)
	}
})

var StoreInfo = React.createClass({
	render: function() {
		var store_type = this.props.Type;
		if (store_type == '0'){
			return(
				<div>
					<Reactman.FormInput label="库存数量" type="text" name="product_store" value={this.props.productStore} validate="require-int" onChange={this.props.onChange} />
				</div>
			)
		}else {
			return(
				<div></div>
			)
		}
	}
});
module.exports = NewProductPage;