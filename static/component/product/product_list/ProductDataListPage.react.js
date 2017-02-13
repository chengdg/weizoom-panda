/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_list:ProductDataListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var AddProductCategoryDialog = require('./AddProductCategoryDialog.react');
var LookProductModelDetail = require('./LookProductModelDetail.react');
var QQOnlineService = require('../.././qq_online/online/QQOnlineService.react');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var ProductDataListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getFilter();
		this.refs.table.refresh(filterOptions);
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

	lookProductModelDetail: function(product_id,value){
		Action.lookProductModelDetail(product_id);
		Reactman.PageAction.showDialog({
			title: value,
			component: LookProductModelDetail,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	onValidateAddProduct: function(){
		var can_created = W.can_created;

		if (can_created == 'False') {
			Reactman.PageAction.showHint('error', '商品数量已经到达上限!');
		} else {
			Action.ProductCategory();
			Reactman.PageAction.showDialog({
				title: "请选择商品分类",
				component: AddProductCategoryDialog,
				data: {},
				okText:false,
				success: function(inputData, dialogState) {
					console.log("success");
				}
			});
		}
		// W.gotoPage('/product/new_product/?second_level_id='+0);
	},

	plusProductStore: function(product_id, event){
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确定提交?',
			confirm: _.bind(function() {
				Action.plusProductStore(product_id);
			}, this)
		});
	},

	showRejectReason: function(event){
		var rejectReasons = JSON.parse(event.target.getAttribute('data-product-reasons'));
		var content = '';
		var Li = rejectReasons.map(function(rejectReason,index){
			if(rejectReason.created_at!=''){
				content += rejectReason.created_at +'</br>'+rejectReason.reject_reasons +'</br>';
			}else{
				content += rejectReason.reject_reasons;  //待入库且没有驳回记录时，时间为空
			}
		});
		Reactman.PageAction.showPopover({
			target: event.target,
			content: '<span style="color:red">' + content + '</span>'
		});
	},

	hideRejectReason: function(event) {
		Reactman.PageAction.hidePopover();
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			var productStatusValue = data['product_status_value'];
			if(productStatusValue === 3){
				return (
					<div>
						<a className="btn btn-primary" target="_blank" href={'/product/new_product/?id='+data.id}>重新修改提交</a>
					</div>
				)
			}else{
				return (
					<div>
						<a className="btn btn-primary" target="_blank" href={'/product/new_product/?id='+data.id}>编辑</a>
					</div>
				)
			}
		}else if (field === 'product_status') {
			//入库状态
			var productStatusValue = data['product_status_value'];
			if(productStatusValue === 0){//待入库
				return (
					<a style={{marginBottom:'0px'}} href="javascript:void(0);" onMouseOut={this.hideRejectReason} onMouseOver={this.showRejectReason} data-product-reasons={data.reject_reasons}>{value}</a>
				)
			}else if(productStatusValue === 3){//入库驳回
				return (
					<a style={{color:'red',marginBottom:'0px'}} href="javascript:void(0);" onMouseOut={this.hideRejectReason} onMouseOver={this.showRejectReason} data-product-reasons={data.reject_reasons}>{value}</a>
				)
			}else{
				return value;
			}
			
		}else if(field === 'product_name'){
			var _this = this;
			var role = data['role'];
			var product_has_model = data['product_has_model'];
			var img = <img className="product-img" src={data['image_path']} style={{width:'60px',height:'60px',marginRight:'10px'}}></img>
			var isModel = data['is_model'];
			if(role == 3){
				if(product_has_model>0){
					return(
						<span className="product-name">
							{img}
							<a title={value} href={'/product/new_product/?id='+data.id}>{value}</a>
							{isModel==true?<a href='javascript:void(0);' className='product-model-detail' onClick={_this.lookProductModelDetail.bind(_this,data.id,value)}>查看{product_has_model}个规格详情</a>:''} 
						</span>
					)
				}else{
					return(
						<span className="product-name">
							{img}
							<a title={value} href={'/product/new_product/?id='+data.id}>{value}</a>
						</span>
					)
				}
				
			}else{
				if(product_has_model>0){
					return(
						<span className="product-name">
							{img}
							<a title={value} style={{cursor:'default',textDecoration:'none'}}>{value}</a>
							{isModel==true?<a href='javascript:void(0);' className='product-model-detail' onClick={_this.lookProductModelDetail.bind(_this,data.id,value)}>查看{product_has_model}个规格详情</a>:''} 
						</span>
					)
				}else{
					return(
						<span className="product-name">
							{img}
							<a title={value} style={{cursor:'default',textDecoration:'none'}}>{value}</a>
						</span>
					)
				}
				
			}
		} else if (field === 'catalog_name') {
			var name = data['second_level_name'];
			var line =name.length>0?'-':''
			return (
				<div>
					<span>{data['first_level_name']}</span><br></br>
					<span style={{paddingLeft:'10px'}}>{line}{data['second_level_name']}</span>
				</div>
			);
		} else if (field === 'product_store') {
			var store_short = data['store_short'];
			if (store_short){
			    return (
                    <div>
                        <span style={{color: 'red'}}>{data['product_store']}</span><br></br>

                    </div>
                );
			}else{
			    return (
                    <div>
                        <span>{data['product_store']}</span><br></br>
                    </div>
                );
			}

		} else {
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	onExport: function(){
		Action.exportProducts();
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_list',
			data: {
				page: 1
			}
		};
		var optionsForProductStatus = [{text: '全部', value: '0'},{text: '待入库', value: '2'},{text: '已入库', value: '1'},{text: '入库驳回', value: '4'}];
		var serviceTel = W.serviceTel;
		var serviceQQFirst = W.serviceQQFirst;
		var serviceQQSecond = W.serviceQQSecond;
		//返点用户
		if(W.purchaseMethod == '1') {
			return (
				<div className="mt15 xui-product-productListPage">
					<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
						<Reactman.FilterRow>
							<Reactman.FilterField>
								<Reactman.FormInput label="商品名称:" name="product_name_query" match="=" />
							</Reactman.FilterField>
							<Reactman.FilterField>
								<Reactman.FormInput label="商品分类:" name="catalog_query" match='=' />
							</Reactman.FilterField>
							<Reactman.FilterField>
								<Reactman.FormSelect label="入库状态:" name="product_status" options={optionsForProductStatus} match="=" />
							</Reactman.FilterField>
						</Reactman.FilterRow>
					</Reactman.FilterPanel>
					<Reactman.TablePanel>
						<Reactman.TableActionBar>
							<Reactman.TableActionButton text="导出商品" onClick={this.onExport}/>
							<Reactman.TableActionButton text="添加新商品" icon="plus" onClick={this.onValidateAddProduct}/>
						</Reactman.TableActionBar>
						<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
							<Reactman.TableColumn name="商品信息" field="product_name" width="400px"/>
							<Reactman.TableColumn name="分类" field="catalog_name" />
							<Reactman.TableColumn name="售价(元)" field="product_price" />
							<Reactman.TableColumn name="结算价(元)" field="clear_price" />
							<Reactman.TableColumn name="销量" field="sales" />
							<Reactman.TableColumn name="库存" field="product_store" />
							<Reactman.TableColumn name="创建时间" field="created_at" />
							<Reactman.TableColumn name="入库状态" field="product_status" />
							<Reactman.TableColumn name="销售状态" field="status" />
							<Reactman.TableColumn name="操作" field="action" width='100px'/>
						</Reactman.Table>
					</Reactman.TablePanel>
				</div>
			)
		}else{
			return (
				<div className="mt15 xui-product-productListPage">
				
					<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
						<Reactman.FilterRow>
							<Reactman.FilterField>
								<Reactman.FormInput label="商品名称:" name="product_name_query" match="=" />
							</Reactman.FilterField>
							<Reactman.FilterField>
								<Reactman.FormInput label="商品分类:" name="catalog_query" match='=' />
							</Reactman.FilterField>
							<Reactman.FilterField>
								<Reactman.FormSelect label="入库状态:" name="product_status" options={optionsForProductStatus} match="=" />
							</Reactman.FilterField>
						</Reactman.FilterRow>
					</Reactman.FilterPanel>
					<Reactman.TablePanel>
						<Reactman.TableActionBar>
							<Reactman.TableActionButton text="导出商品" onClick={this.onExport}/>
							<Reactman.TableActionButton text="添加新商品" icon="plus" onClick={this.onValidateAddProduct}/>
						</Reactman.TableActionBar>
						<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
							<Reactman.TableColumn name="商品信息" field="product_name" width="400px"/>
							<Reactman.TableColumn name="分类" field="catalog_name" />
							<Reactman.TableColumn name="售价(元)" field="product_price" />
							<Reactman.TableColumn name="销量" field="sales" />
							<Reactman.TableColumn name="库存" field="product_store" />
							<Reactman.TableColumn name="创建时间" field="created_at" />
							<Reactman.TableColumn name="入库状态" field="product_status" />
							<Reactman.TableColumn name="销售状态" field="status" />
							<Reactman.TableColumn name="操作" field="action" width='100px'/>
						</Reactman.Table>
					</Reactman.TablePanel>
				</div>
			)
		}
		
	}
})
module.exports = ProductDataListPage;