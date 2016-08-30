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

	componentDidMount: function(){
		var _this = this;
		var oldHasProductModel = parseInt(this.state.old_has_product_model);
		var hasProductModel = parseInt(this.state.has_product_model);
		if(this.state.old_product_name){
			document.getElementById('product_name').parentNode.parentNode.firstChild.style.color='red';
		}
		if(this.state.old_promotion_title!=null){
			document.getElementById('promotion_title').parentNode.parentNode.firstChild.style.color='red';
		}
		if(this.state.old_remark){
			document.getElementsByTagName('textarea')[1].parentNode.parentNode.firstChild.style.color='red';
		}
		if(hasProductModel==0 && this.state.old_product_price!='None'){
			document.getElementById('product_price').parentNode.parentNode.firstChild.style.color='red';
		}
		if(hasProductModel==0 && this.state.old_clear_price!='None'){
			document.getElementById('clear_price').parentNode.parentNode.firstChild.style.color='red';
		}
		if(hasProductModel==0 && this.state.old_product_weight!='0'){
			document.getElementById('product_weight').parentNode.parentNode.firstChild.style.color='red';
		}
		if(hasProductModel==0 && parseInt(this.state.old_product_store)!=0){
			document.getElementById('product_store').parentNode.parentNode.firstChild.style.color='red';
		}
		if(this.state.old_images.length!=0){
			document.getElementsByClassName('col-sm-5 xui-form-imageUploader clearfix')[1].parentNode.firstChild.style.color='red';
		}
		var oldModelValues = this.state.old_model_values;
		var modelValues = this.state.model_values;
		if(oldHasProductModel!=-1 && (hasProductModel!=oldHasProductModel)){
			document.getElementsByClassName('radio-inline')[2].parentNode.parentNode.parentNode.firstChild.style.color='red';
		}
		//判断规格值是否相等
		if((hasProductModel==1) && oldModelValues.length!=modelValues.length){
			document.getElementsByClassName('radio-inline')[2].parentNode.parentNode.parentNode.firstChild.style.color='red';
		}

		if(oldHasProductModel==-1 && hasProductModel==1){
			var clearPrices =[];
			var productPrices = [];
			var productWeights = [];
			var productStore = [];
			modelValues.map(function(model,index){
				clearPrices.push(_this.state["clear_price_"+model.modelId]);
				productPrices.push(_this.state["product_price_"+model.modelId]);
				productWeights.push(_this.state["product_weight_"+model.modelId]);
				productStore.push(_this.state["product_store_"+model.modelId]);
			})

			var oldClearPrices =[];
			var oldProductPrices = [];
			var oldProductWeights = [];
			var oldProductStore = [];
			oldModelValues.map(function(oldModel,index){
				oldClearPrices.push(_this.state["old_clear_price_"+oldModel.modelId]);
				oldProductPrices.push(_this.state["old_product_price_"+oldModel.modelId]);
				oldProductWeights.push(_this.state["old_product_weight_"+oldModel.modelId]);
				oldProductStore.push(_this.state["old_product_store_"+oldModel.modelId]);
			})

			if(clearPrices.sort().toString() != oldClearPrices.sort().toString()){
				document.getElementById('model_clear_price').style.color='red';
			}
			if(productPrices.sort().toString() != oldProductPrices.sort().toString()){
				document.getElementById('model_product_price').style.color='red';
			}
			if(productWeights.sort().toString() != oldProductWeights.sort().toString()){
				document.getElementById('model_product_weight').style.color='red';
			}
			if(productStore.sort().toString() != oldProductStore.sort().toString()){
				document.getElementById('model_product_store').style.color='red';
			}

			if((clearPrices.sort().toString() != oldClearPrices.sort().toString())||
				(productPrices.sort().toString() != oldProductPrices.sort().toString()) ||
				(productWeights.sort().toString() != oldProductWeights.sort().toString()) ||
				(productStore.sort().toString() != oldProductStore.sort().toString())
			){
				document.getElementsByClassName('radio-inline')[2].parentNode.parentNode.parentNode.firstChild.style.color='red';
			}
		}

		if(oldHasProductModel!=-1 && hasProductModel==0){
			document.getElementById('product_price').parentNode.parentNode.firstChild.style.color='red';
			document.getElementById('clear_price').parentNode.parentNode.firstChild.style.color='red';
			document.getElementById('product_weight').parentNode.parentNode.firstChild.style.color='red';
			document.getElementById('product_store').parentNode.parentNode.firstChild.style.color='red';
		}
	},

	render:function(){
		var catalogName = '';
		if(this.state.catalog_name.length>0){
			catalogName = this.state.catalog_name;
		}

		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]
		var role = W.role;
		var disabled = role == 3 ? 'disabled' : '';

		var oldCatalogNameStyle ={}
		var oldSecondId = this.state.old_second_catalog_id;
		var secondId = this.state.second_catalog_id;
		
		if(oldSecondId >=0 && (oldSecondId != secondId)){
			oldCatalogNameStyle = {color:'red'}
		}

		return (
			<div className="xui-newProduct-page xui-formPage">
				<OldProduct />
				<form className="form-horizontal mt15">
					<fieldset>
						<legend className="pl10 pt10 pb10">修改后信息</legend>
						<span className="form-group ml15">
							<label className="col-sm-2 control-label pr0" style={oldCatalogNameStyle}>商品类目:</label>
							<span className="xui-catalog-name">{catalogName}</span>
						</span>
						<Reactman.FormInput label="商品名称:" type="text" readonly={disabled} name="product_name" value={this.state.product_name} />
						<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="promotion_title" value={this.state.promotion_title} />
						<Reactman.FormRadio label="多规格商品:" type="text" name="has_product_model" value={this.state.has_product_model} options={optionsForModel} />
						<div> <ProductModelInfo Disabled={disabled} onChange={this.onChange} Modeltype={this.state.has_product_model}/> </div>	
						<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} />
						<Reactman.FormRichTextInput label="商品描述:" name="remark" value={this.state.remark} width="500" height="250" />
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
		var oldCatalogName = this.state.old_second_catalog_id!=-1? this.state.old_catalog_name:this.state.catalog_name;

		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]
		var role = W.role;
		var disabled = role == 3 ? 'disabled' : '';

		var oldProductName = this.state.old_product_name?this.state.old_product_name: this.state.product_name;
		var oldPromotionTitle = this.state.old_promotion_title!=null?this.state.old_promotion_title: this.state.promotion_title;
		var oldRemark = this.state.old_remark.length>0?this.state.old_remark: this.state.remark;
		var oldImages = this.state.old_images.length>0?this.state.old_images: this.state.images;
		var hasProductModel = parseInt(this.state.old_has_product_model)==-1?this.state.has_product_model:this.state.old_has_product_model;
		hasProductModel = String(hasProductModel);
		return (
			<form className="form-horizontal mt15">
				<fieldset>
					<legend className="pl10 pt10 pb10">修改前信息</legend>
					<span className="form-group ml15">
						<label className="col-sm-2 control-label pr0">商品类目:</label>
						<span className="xui-catalog-name">{oldCatalogName}</span>
					</span>
					<Reactman.FormInput label="商品名称:" type="text" readonly={disabled} name="old_product_name" value={oldProductName} />
					<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="old_promotion_title" value={oldPromotionTitle}  />
					<Reactman.FormRadio label="多规格商品:" type="text" name="old_has_product_model" value={hasProductModel} options={optionsForModel} />
					<div> <OldProductModelInfo Disabled={disabled} Modeltype={hasProductModel}/> </div>	
					<Reactman.FormImageUploader label="商品图片:" name="old_images" value={oldImages}/>
					<Reactman.FormRichTextInput label="商品描述:" name="old_remark" value={oldRemark} width="500" height="250" />
				</fieldset>
			</form>
		)
	}
})

module.exports = ProductContrastPage;