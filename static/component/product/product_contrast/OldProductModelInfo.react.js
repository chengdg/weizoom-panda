/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:OldProductModelInfo');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./ProductModelInfo.css');

var OldProductModelInfo = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	deleteModelValue: function(modelId){
		Action.deleteModelValue(modelId);
	},

	render: function() {
		var _this = this;
		var model_type = this.props.Modeltype;
		var disabled = this.props.Disabled;
		var model_values = this.state.old_model_values;
		var model_names = this.state.old_model_names;
		console.log(this.state.model_values,model_names);
		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]
		var old_model_value_tr = model_values.map(function(model,index){
			var td = model.propertyValues.map(function(value,index){
				return(
					<td key={index} style={{verticalAlign:'middle',width:'100px',paddingLeft:'6px !important'}}>{value.name}</td>
				)
			})
			// if(W.purchase_method==2){
			// 	var product_price = _this.state["old_product_price_"+model.modelId];
			// 	if(product_price){
			// 		var points = 1-(W.points/100);
			// 		var product_price = parseFloat(product_price);
			// 		_this.state["old_clear_price_"+model.modelId] = (Math.round((points*product_price*100).toFixed(2))/100).toFixed(2);
			// 	}
			// }
			return(
				<tr key={index} className="model-table-tr">
					{td}
					<td>
						{_this.state["old_clear_price_"+model.modelId]}
					</td>
					<td>
						{_this.state["old_product_price_"+model.modelId]}
					</td>
					<td>
						{_this.state["old_product_weight_"+model.modelId]}
					</td>
					<td>
						{_this.state["old_product_store_"+model.modelId]}
					</td>
				</tr>
			)

		})
		if (model_type == '0'){
			if(W.purchase_method==2){
				var product_price = this.state["product_price"];
				if(product_price){
					var points = 1-(W.points/100);
					var product_price = parseFloat(product_price);
					var clear_price = (Math.round((product_price*points*100).toFixed(2))/100).toFixed(2)
					this.state["clear_price"] = clear_price;
				}
			}

			var oldProductPrice = this.state.old_product_price!='None'?this.state.old_product_price: this.state.product_price;
			var oldclearPrice = this.state.old_clear_price!='None'?this.state.old_clear_price: this.state.clear_price;
			var oldProductWeight = this.state.old_product_weight!='0'?this.state.old_product_weight: this.state.product_weight;
			var oldProductStore = parseInt(this.state.old_product_store)!=0?this.state.old_product_store: this.state.product_store;
			
			return(
				<div className="product_info_fieldset">
					<Reactman.FormInput label="商品售价:" type="text" readonly={disabled} name="old_product_price" value={oldProductPrice} onChange={this.props.onChange} />
					<span className="money_note">
						元
					</span>
					<div></div>
					<Reactman.FormInput label="结算价:" type="text" readonly={disabled} name="old_clear_price" value={oldclearPrice} onChange={this.props.onChange} />
					<span className="money_note">
						元
					</span>
					<div></div>
					<Reactman.FormInput label="商品重量:" type="text" readonly={disabled} name="old_product_weight" value={oldProductWeight} onChange={this.props.onChange} />
					<span className="money_note">
						Kg
					</span>
					<Reactman.FormInput label="库存数量" type="text" readonly={disabled} name="old_product_store" value={oldProductStore} onChange={this.props.onChange} />
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
						<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginLeft:'80px',marginBottom:'10px'}}>
							<thead>
								<tr>
									{th}
									<th>结算价格(元)</th>
									<th>商品售价(元)</th>
									<th>重量(Kg)</th>
									<th>库存</th>
								</tr>
							</thead>
							<tbody id="">
							{old_model_value_tr}
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
module.exports = OldProductModelInfo;