/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:customer.statistic_report:OpenStatisticReport');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var Reactman = require('reactman');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var OpenStatisticReport = React.createClass({
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
			resource: 'customer.statistics_report',
			data: {
				user_id: W.user_id
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<div>一、多商品销量</div>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} ref="table">
					<Reactman.TableColumn name="商品" field="product_name" />
					<Reactman.TableColumn name="微众白富美" field="weizoom_baifumei" />
					<Reactman.TableColumn name="微众俱乐部" field="weizoom_club" />
					<Reactman.TableColumn name="微众家" field="weizoom_jia" />
					<Reactman.TableColumn name="微众妈妈" field="weizoom_mama" />
					<Reactman.TableColumn name="微众商城" field="weizoom_shop" />
					<Reactman.TableColumn name="微众学生" field="weizoom_xuesheng" />
				</Reactman.Table>
				<div>二、订单销售趋势</div>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} ref="table">
					<Reactman.TableColumn name="第一周" field="first_week" />
					<Reactman.TableColumn name="第二周" field="second_week" />
					<Reactman.TableColumn name="第三周" field="third_week" />
					<Reactman.TableColumn name="第四周" field="fourth_week" />
				</Reactman.Table>
				<div>三、购买用户数据</div>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} ref="table">
					<Reactman.TableColumn name="总人数" field="all_purchase_number" />
					<Reactman.TableColumn name="一次购买" field="one_time_purchase" />
					<Reactman.TableColumn name="复购用户" field="re_purchase" />
				</Reactman.Table>
				<div>四、体验反馈数据</div>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} ref="table">
					<Reactman.TableColumn name="反馈总人数" field="feedback_all_number" />
					<Reactman.TableColumn name="反馈条数" field="feedback_number" />
				</Reactman.Table>
				<div>五、平台订单数</div>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} ref="table">
					<Reactman.TableColumn name="微众白富美" field="weizoom_baifumei_orders_number" />
					<Reactman.TableColumn name="微众俱乐部" field="weizoom_club_orders_number" />
					<Reactman.TableColumn name="微众家" field="weizoom_jia_orders_number" />
					<Reactman.TableColumn name="微众妈妈" field="weizoom_mama_orders_number" />
					<Reactman.TableColumn name="微众商城" field="weizoom_shop_orders_number" />
					<Reactman.TableColumn name="微众学生" field="weizoom_xuesheng_orders_number" />
				</Reactman.Table>
			</div>
		)
	}
})
module.exports = OpenStatisticReport;