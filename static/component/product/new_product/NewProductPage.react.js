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
		var reg =/^\d{0,9}\.{0,1}(\d{1,2})?$/;
		var reg_2 = /^[0-9]+(.[0-9]{1,2})?$/;
		var has_limit_time = parseInt(product.has_limit_time[0]);
		if(product.hasOwnProperty('limit_clear_price') && product.limit_clear_price.length>0){
			if(!isNaN(parseInt(product.limit_clear_price.trim())) && !reg.test(product.limit_clear_price.trim())){
				Reactman.PageAction.showHint('error', '限时结算价只能保留两位有效数字,请重新输入!');
				return;
			}
		}
		if(product.hasOwnProperty('product_price') && product.product_price.length>0){
			if(!reg_2.test(product.product_price.trim())){
				Reactman.PageAction.showHint('error', '商品价格是数字且保留两位有效数字,请重新输入!');
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
		console.log(model_values,"----------");
		_.each(model_values, function(model) {
			model['product_price_'+model.modelId] = product['product_price_'+model.modelId]
			model['limit_clear_price_'+model.modelId] = product['limit_clear_price_'+model.modelId]
			model['clear_price_'+model.modelId] = product['clear_price_'+model.modelId]
			model['product_weight_'+model.modelId] = product['product_weight_'+model.modelId]
			model['product_store_'+model.modelId] = product['product_store_'+model.modelId]
			model['product_code_'+model.modelId] = product['product_code_'+model.modelId]
			model['valid_time_from_'+model.modelId] = product['valid_time_from_'+model.modelId]
			model['valid_time_to_'+model.modelId] = product['valid_time_to_'+model.modelId]
		})
		console.log(model_values,"===");
		Action.saveNewProduct(product,JSON.stringify(model_values));
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

var ProductModelInfo = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	addProductModel: function(){
		Reactman.PageAction.showDialog({
			title: "选择商品规格",
			component: AddProductModelDialog,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	deleteModelValue: function(modelId){
		console.log(modelId,this.state.model_values,"======");
		// var customModels = this.state.model_values;
		// var this_customModels = _.filter(customModels, function(customModel) {
		// 	return customModel.modelId !== modelId;
		// });
		// this.setState({
		// 	model_values: this_customModels
		// })
		Action.deleteModelValue(modelId);
		console.log(this.customModels,"++++++");
	},

	setValidataTime: function(modelId){
		console.log(modelId);
		Reactman.PageAction.showDialog({
			title: "设置限时结算价有效期",
			component: SetValidataTimeDialog,
			data: {
				'modelId': modelId
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	render: function() {
		var _this = this;
		var model_type = this.props.Modeltype;
		var disabled = this.props.Disabled;
		var model_values = this.state.model_values;
		var model_names = this.state.model_names;
		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]

		var model_value_tr = model_values.map(function(model,index){
			var td = model.propertyValues.map(function(value,index){
				return(
					<td key={index} style={{paddingTop:'15px'}}>{value.name}</td>
				)
			})

			return(
				<tr key={index} ref={model.modelId}>
					{td}
					<td>
						<Reactman.FormInput label="" type="text" name={"product_price_"+model.modelId} value={_this.state["product_price_"+model.modelId]} onChange={_this.props.onChange} />
					</td>
					<td style={{position:'relative'}}>
						<Reactman.FormInput label="" type="text" name={"limit_clear_price_"+model.modelId} value={_this.state["limit_clear_price_"+model.modelId]} onChange={_this.props.onChange}/>
						<a onClick={_this.setValidataTime.bind(null,model.modelId)} style={{position:'absolute',top:'14px',right:'6px'}}>有效期</a>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"clear_price_"+model.modelId} value={_this.state["clear_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-price"/>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_weight_"+model.modelId} value={_this.state["product_weight_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_store_"+model.modelId} value={_this.state["product_store_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_code_"+model.modelId} value={_this.state["product_code_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
					</td>
					<td className="show-active">
						<a className="btn cursorPointer" onClick={_this.deleteModelValue.bind(_this,model.modelId)}>删除</a>
					</td>
				</tr>
			)

		})

		// var model_value_tr;
		// if(model_values.length>0){
		// 	model_value_tr = JSON.parse(model_values).map(function(model_value,index){
		// 		var td_1,td_2,td_3;
		// 		if(model_value.hasOwnProperty('third')){
		// 			td_1 = <td>{model_value.first}</td>;
		// 			td_2 = <td>{model_value.second}</td>;
		// 			td_3 = <td>{model_value.third}</td>;
		// 		}else if(model_value.hasOwnProperty('second')){
		// 			td_1 = <td>{model_value.first}</td>;
		// 			td_2 = <td>{model_value.second}</td>;
		// 		}else{
		// 			td_1 = <td>{model_value.first}</td>;
		// 		}
		// 		console.log(td_1);
		// 		return(
		// 			<tr key={index}>
		// 				{td_1}
		// 				{td_2}
		// 				{td_3}
		// 				<td>
		// 					<Reactman.FormInput label="" type="text" name="product_price" value={_this.state.product_price} onChange={_this.props.onChange} />
		// 				</td>
		// 				<td>
		// 					<Reactman.FormInput label="" type="text" name="limit_clear_price" value={_this.state.limit_clear_price} onChange={_this.props.onChange}/>
		// 				</td>
		// 				<td>2</td>
		// 				<td>
		// 					<Reactman.FormInput label="" type="text" name="product_weight" value={_this.state.product_weight} onChange={_this.props.onChange} validate="require-float"/>
		// 				</td>
		// 				<td>
		// 					<Reactman.FormInput label="" type="text" name="product_store" value={_this.state.productStore} validate="require-int" onChange={_this.props.onChange} />
		// 				</td>
		// 				<td></td>
		// 				<td className="show-active">
		// 					<a className="btn cursorPointer">删除</a>
		// 				</td>
		// 			</tr>
		// 		)
		// 	})
		// }
		if (model_type == '0'){
			return(
				<div className="product_info_fieldset">
					<Reactman.FormInput label="商品价格:" type="text" readonly={disabled} name="product_price" value={this.state.product_price} onChange={this.props.onChange} />
					<span className="money_note">
						元
					</span>
					<div></div>
					<Reactman.FormInput label="结算价:" type="text" readonly={disabled} name="clear_price" value={this.state.clear_price} onChange={this.props.onChange} validate="require-price"/>
					<span className="money_note">
						元
					</span>
					<div></div>
					<Reactman.FormInput label="限时结算价:" type="text" readonly={disabled} name="limit_clear_price" value={this.state.limit_clear_price} onChange={this.props.onChange}/>
					<span className="limit_money_note">
						元
					</span>
					<Reactman.FormCheckbox label="" name="has_limit_time" value={this.state.has_limit_time} options={optionsForCheckbox} onChange={this.props.onChange} />
					<Reactman.FormDateTimeInput label="有效期:" name="valid_time_from" value={this.state.valid_time_from} readOnly onChange={this.props.onChange} />
					<Reactman.FormDateTimeInput label="至:" name="valid_time_to" value={this.state.valid_time_to} readOnly onChange={this.props.onChange} />
					<span className="limit_money_note_tips">
						(注:如有让利活动推广时,可设置限时结算价,则优惠期间产生的订单按限时结算价统计账单)
					</span>
					<div></div>
					<Reactman.FormInput label="商品重量:" type="text" readonly={disabled} name="product_weight" value={this.state.product_weight} onChange={this.props.onChange} validate="require-float"/>
					<span className="money_note">
						Kg
					</span>
					<Reactman.FormInput label="库存数量" type="text" readonly={disabled} name="product_store" value={this.state.product_store} validate="require-int" onChange={this.props.onChange} />
				</div>
			)
		}else {
			var th = model_names.map(function(name,index){
				return(
					<th key={index}>{name.name}</th>
				)
			})
			return(
				<div>
					<div>
						<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'180px',marginBottom:'10px'}}>
							<thead>
								<tr>
									{th}
									<th>采购价</th>
									<th>限时结算价</th>
									<th>售价</th>
									<th>重量(Kg)</th>
									<th>库存</th>
									<th>商品编码</th>
									<th>操作</th>
								</tr>
							</thead>
							<tbody id="">
							{model_value_tr}
							</tbody>
						</table>
					</div>
					<div style={{paddingLeft:'180px',marginBottom:'10px'}}>
						<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" onClick={this.addProductModel}>添加商品规格</a>
					</div>
				</div>
			)
		}
	}
});
module.exports = NewProductPage;