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

	onChangeModelType:function(model_id,model_type){
		// var property = event.target.getAttribute('name');
		Action.updateProductModelType(model_id,model_type);
		console.log(model_id,model_type);
	},

	deleteProductModel: function(model_id,event) {
		console.log(model_id);
		var title = '确定删除么?';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.deleteProductModel(model_id);
			}, this)
		});
	},

	addProductModelValue: function(model_id,model_type){
		Action.clearProductModelValue();
		Reactman.PageAction.showDialog({
			title: "添加规格值",
			component: AddProductModelValueDialog,
			data: {
				'model_id':model_id,
				'model_type':model_type
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	addProductModel: function(){
		Action.addProductModel();
	},

	editProductModelName: function(id,ref){
		var name = this.refs.table.refs[ref].value;
		if(name.trim().length==0){
			Reactman.PageAction.showHint('error', '请输入规格名');
			return;
		}
		Action.updateProductModel(id,name);
	},

	deleteProductModelValue: function(value_id){
		Action.deleteProductModelValue(value_id);
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
					<a className="btn btn-link btn-xs" onClick={this.deleteProductModel.bind(this,data['id'])} data-product-id={data.id}>删除</a>
				</div>
			);
		}else if(field === 'model_type'){
			var model_type = parseInt(data['model_type']);
			var name = 'model_type_'+data['id'];
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
						<input type="radio" className="radio model_type_text" name={name} value="0" checked={text_checked} onChange={this.onChangeModelType.bind(this,data['id'],0)}/>
						<span className="model_type_text_value">文本</span>
					</label>
					<label className="radio_model_type">
						<input type="radio" className="radio model_type_img" name={name} value="1" checked={img_checked} onChange={this.onChangeModelType.bind(this,data['id'],1)}/>
						<span className="model_type_text_value">图片</span>
					</label>
				</div>
			)
		} else if(field === 'product_model_value'){
			var _this = this;
			var model_name = data['model_name'];
			var model_type = parseInt(data['model_type']);
			var model_name_li ='';
			if(model_name){
				model_name_li = JSON.parse(model_name).map(function(model,index){
					var class_name = 'model_' + model['id'];
					var pic_url = model_type==1?model['pic_url']:''
					if(model_type==1){
						var show_img_or_text = <img src={pic_url} style={{width:'33px',height:'38px'}}></img>;
					}else{
						var show_img_or_text = <span title={model['name']}>{model["name"]}</span>;
					}
					return(
						<li data-model-name={model['name']} className="model_li" key={index}>
	                        <div className='xa-editModelPropertyValue' onMouseOver={_this.onMouseOver.bind(null,class_name)} onMouseOut={_this.onMouseOut.bind(null,class_name)}>  
	                            {show_img_or_text}  
	                        </div>
	                        <button className="xui-close xa-delete" ref={class_name} type="button" style={{display: 'none'}} onMouseOver={_this.onMouseOver.bind(null,class_name)} onMouseOut={_this.onMouseOut.bind(null,class_name)}>
	                            <span onClick={_this.deleteProductModelValue.bind(_this,model['id'])}>×</span>
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
	                            <a href="javascript:void(0);" onClick={this.addProductModelValue.bind(this,data['id'],data['model_type'])}><img src="/static/img/panda_img/addProduct.png" style={{width:'32px',height:'32px'}}/></a>  
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
					<div style={{lineHeight:'30px'}}>
						<input type="text" ref={ref} className="product-model-name" name="model_name" onBlur={this.editProductModelName.bind(null,data['id'],ref)} style={{border:'1px solid #18a689'}} placeholder="请输入规格名"/>
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
						<Reactman.TableColumn name="规格值" field="product_model_value" />
						<Reactman.TableColumn name="操作" field="action" width="100px"/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductModelListPage;