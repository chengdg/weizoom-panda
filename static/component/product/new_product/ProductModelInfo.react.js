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
require('./style.css');

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
			var valid_time_from = _this.state["valid_time_from_"+model.modelId];
			var valid_time_to = _this.state["valid_time_to_"+model.modelId];
			var src = '/static/img/panda_img/icon2.png';
			if((valid_time_from!= undefined && valid_time_from.length> 0) &&(valid_time_to!= undefined && valid_time_to.length> 0)){
				src = '/static/img/panda_img/icon1.png';
			}
			if(W.purchase_method==2){
				var product_price = _this.state["product_price_"+model.modelId];
				if(product_price){
					_this.state["clear_price_"+model.modelId] = ((1-W.points/100)*parseFloat(product_price)).toFixed(2);
				}
			}
			return(
				<tr key={index} ref={model.modelId}>
					{td}
					<td>
						<Reactman.FormInput label="" type="text" name={"clear_price_"+model.modelId} value={_this.state["clear_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
					</td>
					<td style={{position:'relative'}}>
						<Reactman.FormInput label="" type="text" name={"limit_clear_price_"+model.modelId} value={_this.state["limit_clear_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
						<a href="javascript:void(0);" onClick={_this.setValidataTime.bind(null,model.modelId)} style={{position:'absolute',top:'14px',right:'6px'}}>
							<img src={src} style={{width:'22px',height:'22px',marginRight:'10px'}}/>
						</a>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_price_"+model.modelId} value={_this.state["product_price_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_weight_"+model.modelId} value={_this.state["product_weight_"+model.modelId]} onChange={_this.props.onChange} validate="require-float"/>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_store_"+model.modelId} value={_this.state["product_store_"+model.modelId]} validate="require-int" onChange={_this.props.onChange} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name={"product_code_"+model.modelId} value={_this.state["product_code_"+model.modelId]} onChange={_this.props.onChange} />
					</td>
					<td className="show-active">
						<a className="btn cursorPointer" onClick={_this.deleteModelValue.bind(_this,model.modelId)}>删除</a>
					</td>
				</tr>
			)

		})
		if (model_type == '0'){
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
			if(W.purchase_method==2){
				var title='结算价格=商品售价*(1-返点)';
			}
			return(
				<div>
					<div>
						<span style={{marginLeft:'180px'}}>{title}</span>
						<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'180px',marginBottom:'10px'}}>
							<thead>
								<tr>
									{th}
									<th>结算价格(元)</th>
									<th>限时结算价(元)</th>
									<th>商品售价(元)</th>
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
						{W.role==1?<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" onClick={this.addProductModel}>添加商品规格</a>:''}
					</div>
				</div>
			)
		}
	}
});
module.exports = ProductModelInfo;