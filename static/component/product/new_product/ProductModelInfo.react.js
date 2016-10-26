/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:ProductModelInfo');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var AddProductModelDialog = require('./AddProductModelDialog.react');
var SetValidataTimeDialog = require('./SetValidataTimeDialog.react');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./ProductModelInfo.css');

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
		Action.deleteModelValue(modelId);
	},

	setValidataTime: function(modelId){
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
					<td key={index} style={{verticalAlign:'middle',width:'100px',paddingLeft:'6px !important'}}>{value.name}</td>
				)
			})
			// var valid_time_from = _this.state["valid_time_from_"+model.modelId];
			// var valid_time_to = _this.state["valid_time_to_"+model.modelId];
			// var src = '/static/img/panda_img/icon2.png';
			// if((valid_time_from!= undefined && valid_time_from.length> 0) &&(valid_time_to!= undefined && valid_time_to.length> 0)){
			// 	src = '/static/img/panda_img/icon1.png';
			// }
			if(W.purchase_method==1){
				if(W.role==1){
					return(
						<tr key={index} ref={model.modelId} className="model-table-tr">
							{td}
							<td>
								<Reactman.FormInput label="" type="text" name={"clear_price_"+model.modelId} value={_this.state["clear_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name={"product_weight_"+model.modelId} value={_this.state["product_weight_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name={"product_store_"+model.modelId} value={_this.state["product_store_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
							</td>
							<td className="show-active" style={{width:'80px'}}>
								<a className="btn cursorPointer" onClick={_this.deleteModelValue.bind(_this,model.modelId)}>删除</a>
							</td>
						</tr>
					)
				}else{
					return(
						<tr key={index} ref={model.modelId} className="model-table-tr">
							{td}
							<td>
								<Reactman.FormInput label="" type="text" name={"product_price_"+model.modelId} value={_this.state["product_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"clear_price_"+model.modelId} value={_this.state["clear_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_weight_"+model.modelId} value={_this.state["product_weight_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_store_"+model.modelId} value={_this.state["product_store_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
							</td>
							<td className="show-active" style={{width:'80px'}}>
							</td>
						</tr>
					)
				}
			}else{
				if(W.role==1){
					return(
						<tr key={index} ref={model.modelId} className="model-table-tr">
							{td}
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_price_"+model.modelId} value={_this.state["product_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_weight_"+model.modelId} value={_this.state["product_weight_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_store_"+model.modelId} value={_this.state["product_store_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
							</td>
							<td className="show-active" style={{width:'80px'}}>
								<a className="btn cursorPointer" onClick={_this.deleteModelValue.bind(_this,model.modelId)}>删除</a>
							</td>
						</tr>
					)
				}else{
					return(
						<tr key={index} ref={model.modelId} className="model-table-tr">
							{td}
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_price_"+model.modelId} value={_this.state["product_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"clear_price_"+model.modelId} value={_this.state["clear_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_weight_"+model.modelId} value={_this.state["product_weight_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
							</td>
							<td>
								<Reactman.FormInput label="" type="text" readonly={disabled} name={"product_store_"+model.modelId} value={_this.state["product_store_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
							</td>
							<td className="show-active" style={{width:'80px'}}>
								<a className="btn cursorPointer" onClick={_this.deleteModelValue.bind(_this,model.modelId)}>删除</a>
							</td>
						</tr>
					)
				}
			}
		})
		if (model_type == '0' || model_type==''){
			if(W.purchase_method==1){
				if(W.role==1){
					return(
						<div className="product_info_fieldset">
							<div style={{paddingLeft:'180px', color:'rgba(138, 43, 43, 0.82)'}}>提示：结算价为商品与微众的结算价格，如无扣点约定，可与售价相同</div>
							<Reactman.FormInput label="结算价(元):" type="text" readonly={disabled} name="clear_price" value={this.state.clear_price} onChange={this.props.onChange} validate="require-float"/>
							
							<Reactman.FormInput label="物流重量(Kg):" type="text" readonly={disabled} name="product_weight" value={this.state.product_weight} onChange={this.props.onChange} validate="require-float"/>
							<Reactman.FormInput label="库存数量" type="text" readonly={disabled} name="product_store" value={this.state.product_store} validate="require-int" onChange={this.props.onChange} />
						</div>
					)
				}else{
					return(
						<div className="product_info_fieldset">
							<Reactman.FormInput label="商品售价:" type="text" name="product_price" value={this.state.product_price} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								元
							</span>
							<div></div>
							<Reactman.FormInput label="结算价:" type="text" readonly={disabled} name="clear_price" value={this.state.clear_price} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								元
							</span>
							<div></div>
							<Reactman.FormInput label="物流重量:" type="text" readonly={disabled} name="product_weight" value={this.state.product_weight} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								Kg
							</span>
							<Reactman.FormInput label="库存数量" type="text" readonly={disabled} name="product_store" value={this.state.product_store} validate="require-int" onChange={this.props.onChange} />
						</div>
					)
				}
			}else{
				if(W.role==1){
					return(
						<div className="product_info_fieldset">
							<Reactman.FormInput label="商品售价:" type="text" readonly={disabled} name="product_price" value={this.state.product_price} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								元
							</span>
							<div></div>
							<Reactman.FormInput label="商品重量:" type="text" readonly={disabled} name="product_weight" value={this.state.product_weight} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								Kg
							</span>
							<Reactman.FormInput label="库存数量" type="text" readonly={disabled} name="product_store" value={this.state.product_store} validate="require-int" onChange={this.props.onChange} />
						</div>
					)
				}else{
					return(
						<div className="product_info_fieldset">
							<Reactman.FormInput label="商品售价:" type="text" readonly={disabled} name="product_price" value={this.state.product_price} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								元
							</span>
							<div></div>
							<Reactman.FormInput label="结算价:" type="text" readonly={disabled} name="clear_price" value={this.state.clear_price} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								元
							</span>
							<div></div>
							<Reactman.FormInput label="商品重量:" type="text" readonly={disabled} name="product_weight" value={this.state.product_weight} onChange={this.props.onChange} validate="require-float"/>
							<span className="money_note">
								Kg
							</span>
							<Reactman.FormInput label="库存数量" type="text" readonly={disabled} name="product_store" value={this.state.product_store} validate="require-int" onChange={this.props.onChange} />
						</div>
					)
				}
			}
		}else {
			var th = model_names.map(function(name,index){
				return(
					<th key={index}>{name.name}</th>
				)
			})
			if(W.purchase_method==1){
				if(W.role==1){
					return(
						<div>
							<div>
								<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'180px',marginBottom:'10px'}}>
									<thead>
										<tr>
											{th}
											<th>结算价格(元)</th>
											<th>重量(Kg)</th>
											<th>库存</th>
											<th>操作</th>
										</tr>
									</thead>
									<tbody id="">
									{model_value_tr}
									</tbody>
								</table>
							</div>
							<div style={{paddingLeft:'180px',marginBottom:'10px'}}>
								{W.role==1?<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" onClick={this.addProductModel}>添加商品规格</a>:''}
							</div>
						</div>
					)
				}else{
					return(
						<div>
							<div>
								<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'180px',marginBottom:'10px'}}>
									<thead>
										<tr>
											{th}
											<th>商品售价(元)</th>
											<th>结算价格(元)</th>
											<th>重量(Kg)</th>
											<th>库存</th>
											<th>操作</th>
										</tr>
									</thead>
									<tbody id="">
									{model_value_tr}
									</tbody>
								</table>
							</div>
							<div style={{paddingLeft:'180px',marginBottom:'10px'}}>
								{W.role==1?<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" onClick={this.addProductModel}>添加商品规格</a>:''}
							</div>
						</div>
					)
				}
			}else{
				if(W.role==1){
					return(
						<div>
							<div>
								<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'180px',marginBottom:'10px'}}>
									<thead>
										<tr>
											{th}
											<th>商品售价(元)</th>
											<th>重量(Kg)</th>
											<th>库存</th>
											<th>操作</th>
										</tr>
									</thead>
									<tbody id="">
									{model_value_tr}
									</tbody>
								</table>
							</div>
							<div style={{paddingLeft:'180px',marginBottom:'10px'}}>
								{W.role==1?<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" onClick={this.addProductModel}>添加商品规格</a>:''}
							</div>
						</div>
					)
				}else{
					return(
						<div>
							<div>
								<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'180px',marginBottom:'10px'}}>
									<thead>
										<tr>
											{th}
											<th>商品售价(元)</th>
											<th>结算价格(元)</th>
											<th>重量(Kg)</th>
											<th>库存</th>
											<th>操作</th>
										</tr>
									</thead>
									<tbody id="">
									{model_value_tr}
									</tbody>
								</table>
							</div>
							<div style={{paddingLeft:'180px',marginBottom:'10px'}}>
								{W.role==1?<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" onClick={this.addProductModel}>添加商品规格</a>:''}
							</div>
						</div>
					)
				}
			}
		}
	}
});
module.exports = ProductModelInfo;