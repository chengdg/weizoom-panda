/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:AddProductModelDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./modelDialogStyle.css');

var AddProductModelDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'value_ids': Store.getData().value_ids
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData().value_ids);
	},

	chooseProductModelValue: function(value_id){
		console.log(value_id,"==========");
		Action.addProductModelValue(value_id);
	},

	saveModelValue: function(){
		Action.saveModelValue(this.state.value_ids);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<input type='checkbox' onChange={this.onChange}/>
				</div>
			);
		}else if(field === 'product_model_value'){
			console.log(this.state.value_ids,"------");
			var _this = this;
			var value_ids = this.state.value_ids;
			var model_name = data['model_name'];
			var model_name_li ='';
			if(model_name){
				model_name_li = JSON.parse(model_name).map(function(model,index){
					var value_id = model['id'];
					var checked = value_ids.indexOf(value_id)!=-1?'checked':null;
					return(
						<li data-model-name={model['name']} className="model_li" key={index}>
	                        <input type="checkbox" checked={checked} onChange={_this.chooseProductModelValue.bind(null,model['id'])}/><span style={{verticalAlign: 'top'}}>{model["name"]}</span>
	                    </li>
					)
				})
			}
			return(
				<div>
					<ul className="xui-propertyValueList">
						{model_name_li}
					</ul>
				</div>
			)
		} else {
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_model',
			data: {
				page: 1
			}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} ref="table">
						<Reactman.TableColumn name="规格名" field="product_model_name" width="100px"/>
						<Reactman.TableColumn name="规格值" field="product_model_value" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="确定" onClick={this.saveModelValue}/>
					</Reactman.TableActionBar>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = AddProductModelDialog;