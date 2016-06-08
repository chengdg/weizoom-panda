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
		var is_true = this.validateProduct();
		if(product.images.length == 0){
			Reactman.PageAction.showHint('error', '请先上传图片！');
			return;
		}
		if(is_true){
			Reactman.PageAction.showHint('error', '请先填写带*的内容！');
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

	validateProduct: function(){
		var is_true = false;
		var product = Store.getData();
		if(!product.hasOwnProperty('product_name') || !product.hasOwnProperty('product_price') || !product.hasOwnProperty('promotion_title')
		 || !product.hasOwnProperty('remark') || !product.hasOwnProperty('clear_price') || !product.hasOwnProperty('product_weight')){
			is_true = true;
		}
		if((product.hasOwnProperty('product_name') && product.product_name.length<=0) || (product.hasOwnProperty('product_price') && product.product_price.length<=0)){
			is_true = true;
		}
		if((product.hasOwnProperty('promotion_title') && product.promotion_title.length<=0) || (product.hasOwnProperty('clear_price') && product.clear_price.length<=0)){
			is_true = true;
		}
		if((product.hasOwnProperty('product_weight') && product.product_weight.length<=0) || (product.hasOwnProperty('remark') && product.remark.length<=0)){
			is_true = true;
		}
		return is_true;
	},

	onSubmit: function(){
		var product = Store.getData();
		var reg =/^\d{0,9}\.{0,1}(\d{1,2})?$/;
		var has_limit_time = parseInt(product.has_limit_time[0]);
		if(product.hasOwnProperty('limit_clear_price') && !reg.test(product.limit_clear_price)){
			Reactman.PageAction.showHint('error', '限时结算价只能保留两位有效数字,请重新输入!');
			return;
		}
		if(has_limit_time ==1 && (!product.hasOwnProperty('valid_time_from') || !product.hasOwnProperty('valid_time_to'))){
			Reactman.PageAction.showHint('error', '请选择有效期截止日期!');
			return;
		}
		if(has_limit_time ==1 && ((product.hasOwnProperty('valid_time_from') && product.valid_time_from.length<=0) 
			|| (product.hasOwnProperty('valid_time_to')&& product.valid_time_to.length<=0))){
			Reactman.PageAction.showHint('error', '请选择有效期截止日期!');
			return;
		}
		if(has_limit_time ==1 && (!product.hasOwnProperty('limit_clear_price') || product.limit_clear_price.length<=0) ){
			Reactman.PageAction.showHint('error', '请填写限时结算价!');
			return;
		}
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
		var optionsForCheckbox = [{text: '', value: '1'}]
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
						<Reactman.FormInput label="限时结算价:" type="text" readonly={disabled} name="limit_clear_price" value={this.state.limit_clear_price} onChange={this.onChange}/>
						<span className="limit_money_note">
							元
						</span>
						<Reactman.FormCheckbox label="" name="has_limit_time" value={this.state.has_limit_time} options={optionsForCheckbox} onChange={this.onChange} />
						<Reactman.FormDateTimeInput label="有效期:" name="valid_time_from" value={this.state.valid_time_from} readOnly onChange={this.onChange} />
						<Reactman.FormDateTimeInput label="至:" name="valid_time_to" value={this.state.valid_time_to} readOnly onChange={this.onChange} />
						<span className="limit_money_note_tips">
							(注:如有让利活动推广时,可设置限时结算价,则优惠期间产生的订单按限时结算价统计账单)
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