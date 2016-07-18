/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_model:ProductModelListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var AddProductModelValueDialog = require('./AddProductModelValueDialog.react');
require('./style.css');
var W = Reactman.W;

var ProductModelListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getFilter();
		this.refs.table.refresh(filterOptions);
	},

	onChange:function(value, event){
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	onClickDelete: function(event) {
		var user_has_products = W.user_has_products;
		if(Store.getData().user_has_products){
			user_has_products = Store.getData().user_has_products;
		}
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var title = '彻底删除商品会导致该商品的订单无法同步到当前账号中';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.deleteProduct(productId,user_has_products);
			}, this)
		});
	},

	addProductModelValue: function(){
		Reactman.PageAction.showDialog({
			title: "创建规格值",
			component: AddProductModelValueDialog,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	addProductModel: function(){
		Action.addProductModel();
	},

	editProductModelName: function(id,ref){

		console.log(this.refs.table.refs[ref].value,"----------");
		var name = this.refs.table.refs[ref].value;
		Action.updateProductModel(id,name);
	},

	onMouseOver: function(class_name){
		var div_close = this.refs.table.refs[class_name];
		ReactDOM.findDOMNode(div_close).style.display = "block";
	},

	onMouseOut: function(class_name){
		var div_close = this.refs.table.refs[class_name];
		ReactDOM.findDOMNode(div_close).style.display = "none";
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>删除</a>
				</div>
			);
		}else if(field === 'model_type'){
			var model_type = data['model_type'];
			var text_checked = null;
			var img_checked = null;
			if(model_type==0){
				text_checked = 'checked';
			}else{
				img_checked = 'checked';
			}
			return(
				<div>
					<label className="radio_model_type">
						<input type="radio" className="radio model_type_text" name="model_type" value="0" checked={text_checked} onChange={this.onChange}/>
						<span className="model_type_text_value">文字</span>
					</label>
					<label className="radio_model_type">
						<input type="radio" className="radio model_type_img" name="model_type" value="1" checked={img_checked} onChange={this.onChange}/>
						<span className="model_type_text_value">图片</span>
					</label>
				</div>
			)
		} else if(field === 'model_name'){
			var _this = this;
			var model_name = data['model_name'];
			var model_name_li ='';
			if(model_name){
				model_name_li = JSON.parse(model_name).map(function(model,index){
					var class_name = 'model_' + model['id'];
					return(
						<li data-value-id="1" data-model-name={model['name']} className="model_li" key={index}>
	                        <div className='xa-editModelPropertyValue' onMouseOver={_this.onMouseOver.bind(null,class_name)} onMouseOut={_this.onMouseOut.bind(null,class_name)}>  
	                            <span title={model['name']}>{model["name"]}</span>  
	                        </div>
	                        <button className="xui-close xa-delete" ref={class_name} type="button" style={{display: 'none'}} onMouseOver={_this.onMouseOver.bind(null,class_name)} onMouseOut={_this.onMouseOut.bind(null,class_name)}>
	                            <span>×</span>
	                        </button>
	                    </li>
					)
				})
			}
			return(
				<div>
					<ul className="xui-propertyValueList">
						{model_name_li}
						<li className="model_li">
							<div className='xa-editModelPropertyValue'>  
	                            <a href="javascript:void(0);" onClick={this.addProductModelValue}><img src="/static/img/panda_img/addProduct.png" style={{width:'32px',height:'32px'}}/></a>  
	                        </div>
						</li>
					</ul>
				</div>
			)

		}else if(field === 'product_model_name'){
			var product_model_name = data['product_model_name'];
			var ref = 'product_model_' + data['id'];
			if(product_model_name){
				return(
					<div>
						{product_model_name}
					</div>
				)
			}else{
				return(
					<div>
						<input type="text" ref={ref} className="product-model-name" name="model_name" onBlur={this.editProductModelName.bind(null,data['id'],ref)} style={{border:'1px solid #18a689'}}/>
					</div>
				)
			}
		}else{
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
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加规格" icon="plus" onClick={this.addProductModel}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="规格名" field="product_model_name" width="200px"/>
						<Reactman.TableColumn name="显示样式" field="model_type" width="200px"/>
						<Reactman.TableColumn name="规格值" field="model_name" />
						<Reactman.TableColumn name="操作" field="action" width="100px"/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductModelListPage;