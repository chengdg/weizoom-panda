/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:NewProductPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

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

	onSubmit: function(){
		console.log(Store.getData(),"==========");
		Action.saveNewProduct(Store.getData());
	},

	render:function(){
		var optionsForStore = [{text: '无限', value: '0'}, {text: '有限', value: '1'}];
		return (
			<div className="xui-outlineData-page xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<legend className="pl10 pt10 pb10">基本信息</legend>
						<Reactman.FormInput label="商品名称:" type="text" name="product_name" value={this.state.product_name} onChange={this.onChange} placeholder="最多30个字" />
						<Reactman.FormInput label="促销标题:" type="text" name="promotion_title" value={this.state.promotion_title} placeholder="最多30个字" onChange={this.onChange} />
						<Reactman.FormInput label="商品价格:" type="text" name="product_price" value={this.state.product_price} onChange={this.onChange} />
						<Reactman.FormInput label="结算价:" type="text" name="clear_price" value={this.state.clear_price} onChange={this.onChange} />
						<Reactman.FormInput label="商品重量:" type="text" name="product_weight" value={this.state.product_weight} onChange={this.onChange} />
						<Reactman.FormRadio label="商品库存:" type="text" name="product_store" value={this.state.product_store} options={optionsForStore} onChange={this.onChange} />
						<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} onChange={this.onChange}/>
						<Reactman.FormRichTextInput label="备注:" name="remark" value={this.state.remark} width="800" height="250" onChange={this.onChange} />
					</fieldset>
					<fieldset>
						<Reactman.FormSubmit onClick={this.onSubmit} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = NewProductPage;