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
var AddProductModelDialog = require('./AddProductModelDialog.react');
var SetValidataTimeDialog = require('./SetValidataTimeDialog.react');
var ProductModelInfo = require('./ProductModelInfo.react');
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
		console.log(this.state.model_values,"==========");
		var model_values = this.state.model_values;
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
				product: product,
				model_values: model_values
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	validateProduct: function(){
		var is_true = false;
		var product = Store.getData();
		if(!product.hasOwnProperty('product_name') || !product.hasOwnProperty('remark') || !product.hasOwnProperty('clear_price') || !product.hasOwnProperty('product_weight')){
			is_true = true;
		}
		if(product.hasOwnProperty('product_name') && product.product_name.length<=0){
			is_true = true;
		}
		if(product.hasOwnProperty('clear_price') && product.clear_price.length<=0){
			is_true = true;
		}
		if((product.hasOwnProperty('product_weight') && product.product_weight.length<=0) || (product.hasOwnProperty('remark') && product.remark.length<=0)){
			is_true = true;
		}
		return is_true;
	},

	onSubmit: function(){
		var product = Store.getData();
		product['second_level_id'] = W.second_level_id;
		var reg =/^\d{0,9}\.{0,1}(\d{1,2})?$/;
		var reg_2 = /^[0-9]+(.[0-9]{1,2})?$/;
		var has_limit_time = parseInt(product.has_limit_time[0]);
		if(product.hasOwnProperty('limit_clear_price') && product.limit_clear_price.length>0){
			if(!isNaN(parseInt(product.limit_clear_price.trim())) && !reg.test(product.limit_clear_price.trim())){
				Reactman.PageAction.showHint('error', '限时结算价只能保留两位小数,请重新输入!');
				return;
			}
		}
		if(product.hasOwnProperty('product_price') && product.product_price.length>0){
			if(!reg_2.test(product.product_price.trim())){
				Reactman.PageAction.showHint('error', '商品价格是数字且保留两位小数,请重新输入!');
				return;
			}
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
		if(has_limit_time ==1 && product.hasOwnProperty('valid_time_from') && product.hasOwnProperty('valid_time_to') && (product.valid_time_from>product.valid_time_to)){
			Reactman.PageAction.showHint('error', '有效期开始日期不能大于截止日期,请重新输入!');
			return;
		}
		if(has_limit_time ==1 && (!product.hasOwnProperty('limit_clear_price') || product.limit_clear_price.length<=0) ){
			Reactman.PageAction.showHint('error', '请填写限时结算价!');
			return;
		}
		if(product.hasOwnProperty('limit_clear_price') && parseFloat(product.limit_clear_price)>parseFloat(product.clear_price)){
			Reactman.PageAction.showHint('error', '限时结算价不能大于结算价,请重新输入!');
			return;
		}
		if(product.product_name.length > 30 || (product.hasOwnProperty('promotion_title') && product.promotion_title.length > 30)){
			Reactman.PageAction.showHint('error', '商品名称或促销标题最多输入30个字,请重新输入!');
			return;
		}
		if(product.images.length == 0){
			Reactman.PageAction.showHint('error', '请先上传图片！');
			return ;
		}

		var model_values = this.state.model_values;
		var has_product_model = this.state.has_product_model;
		product['has_product_model'] = this.state.has_product_model;
		
		if(has_product_model==='1' && model_values.length==0){
			Reactman.PageAction.showHint('error', '请添加商品规格！');
			return ;
		}
		_.each(model_values, function(model) {
			var time_from = product['valid_time_from_'+model.modelId]
			var time_to = product['valid_time_to_'+model.modelId]
			if(time_from>time_to){
				Reactman.PageAction.showHint('error', '有效期开始日期不能大于截止日期,请重新输入!');
				return;
			}
			if(!product.hasOwnProperty('valid_time_from_'+model.modelId) || !product.hasOwnProperty('valid_time_to_'+model.modelId)){
				Reactman.PageAction.showHint('error', '有效期不能为空,请重新输入!');
				return;
			}
			if((product.hasOwnProperty('valid_time_from_'+model.modelId) && time_from.length==0) || (product.hasOwnProperty('valid_time_to_'+model.modelId) && time_to.length==0)){
				Reactman.PageAction.showHint('error', '有效期不能为空,请重新输入!');
				return;
			}
		})
		_.each(model_values, function(model) {
			model['product_price_'+model.modelId] = product['product_price_'+model.modelId]
			model['limit_clear_price_'+model.modelId] = product['limit_clear_price_'+model.modelId]
			model['clear_price_'+model.modelId] = product['clear_price_'+model.modelId]
			model['product_weight_'+model.modelId] = product['product_weight_'+model.modelId]
			model['product_store_'+model.modelId] = product['product_store_'+model.modelId]
			model['product_code_'+model.modelId] = product['product_code_'+model.modelId]
			model['valid_time_from_'+model.modelId] = product['valid_time_from_'+model.modelId]
			model['valid_time_to_'+model.modelId] = product['valid_time_to_'+model.modelId]
			if(W.purchase_method==2){
				var product_price = product["product_price_"+model.modelId];
				if(product_price){
					model["clear_price_"+model.modelId] = ((1-W.points/100)*parseFloat(product_price)).toFixed(2);
				}
			}
		})
		model_values = model_values.length>0?JSON.stringify(model_values):''
		Action.saveNewProduct(product,model_values);
	},

	render:function(){
		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
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
						<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="promotion_title" value={this.state.promotion_title} placeholder="最多30个字" onChange={this.onChange} />
						<Reactman.FormRadio label="多规格商品:" type="text" name="has_product_model" value={this.state.has_product_model} options={optionsForModel} onChange={this.onChange} />
						<div> <ProductModelInfo Disabled={disabled} onChange={this.onChange} Modeltype={this.state.has_product_model}/> </div>	
						<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} onChange={this.onChange} validate="require-string"/>
						<Reactman.FormRichTextInput label="商品描述:" name="remark" value={this.state.remark} width="800" height="250" onChange={this.onChange} validate="require-notempty"/>
					</fieldset>
					<fieldset style={{position:'relative'}}>
						{role == 3? '': <Reactman.FormSubmit onClick={this.onSubmit} />}
						<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" style={{position:'absolute',top:'40px',left:'270px'}} onClick={this.productPreview}>商品预览</a>
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
					<Reactman.FormInput label="库存数量" type="text" name="product_store" value={this.props.product_store} validate="require-int" onChange={this.props.onChange} />
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