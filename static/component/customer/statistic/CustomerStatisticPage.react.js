/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:customer.customer:CustomerStatisticPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var CustomerStatisticPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return({})
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getFilter();
		this.refs.table.refresh(filterOptions);
	},

	showProduct:function(class_name){
		var display = document.getElementsByClassName(class_name)[0].style.display;
		if (display == 'none'){
			document.getElementsByClassName(class_name)[0].style.display = "block";
		}else{
			document.getElementsByClassName(class_name)[0].style.display = "none";
		}

	},

	rowFormatter: function(field, value, data) {
		if (field === 'expand-row') {
			var class_name = 'data-' +data['user_id'];
			var product_infos = JSON.parse(data['product_infos'])
			if(product_infos.length>0){
				var products = product_infos.map(function(product,index){
				return(
						<div style={{backgroundColor: '#EFEFEF',height: '22px'}} key={index}>
							<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'15px'}}>{product.name} </div>
							<div className="xui-expand-row-info" style={{float: 'right',paddingRight:'200px'}}>上架时间:{product.time}</div>
							<div className="xui-expand-row-info" style={{float: 'right',paddingRight:'100px'}}>销量:{product.sales} </div>
						</div>
					)
				});
				return (
					<div className={class_name} style={{display:'none'}}>{products}</div>
				)
			}else{
				return (
					<div className={class_name} style={{backgroundColor: '#EFEFEF',height: '22px',display:'none'}}>
						<div style={{float: 'left',paddingLeft:'15px'}}>暂无商品</div>
					</div>
				)
			}
		}else if(field === 'customer_name'){
			var class_name = 'data-' +data['user_id'];
			return (
				<a href="javascript:void(0);" onClick={this.showProduct.bind(this,class_name)}>{value}</a>
			)
		}else if(field === 'feedback'){
			return (
				<a href="javascript:void(0);">{value}</a>
			)
		}else{
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	onExport: function(){
		Action.exportOrders();
	},

	render:function(){
		var productsResource = {
			resource: 'customer.statistics',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="客户名称:" name="customer_name_query" match='=' />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="导出" onClick={this.onExport}/>	
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="客户名称" field="customer_name" />
						<Reactman.TableColumn name="开始推广时间" field="brand_time" />
						<Reactman.TableColumn name="总销量" field="total_sales" />
						<Reactman.TableColumn name="订单数" field="total_order_number" />
						<Reactman.TableColumn name="总金额" field="total_order_money" />
						<Reactman.TableColumn name="现金" field="total_final_price" />
						<Reactman.TableColumn name="微众卡" field="total_weizoom_card_money" />
						<Reactman.TableColumn name="优惠券" field="total_coupon_money" />
						<Reactman.TableColumn name="体验反馈" field="feedback" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = CustomerStatisticPage;