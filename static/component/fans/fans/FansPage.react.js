/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css')

var CustomerPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	showOrder:function(class_name){
		var display = document.getElementsByClassName(class_name)[0].style.display;
		if (display == 'none'){
			document.getElementsByClassName(class_name)[0].style.display = "block";
		}else{
			document.getElementsByClassName(class_name)[0].style.display = "none";
		}
	},

	rowFormatter: function(field, value, data) {
		if (field === 'expand-row') {
			var order_infos = data['order_infos'];
			var class_name = 'data-' +data['user_id'];
			if(order_infos){
				var products = JSON.parse(order_infos).map(function(order,index){
					var order_id = order['order_id'];
					var src = '/order/customer_order_detail/?id='+order_id;
					return(
							<div style={{marginTop:'5px'}} key={index}>
								<div className="xui-expand-row-info" style={{float: 'left',width:'180px'}}>
									<a href={src} target="_blank">{order.order_id}</a> 
								</div>
								<div className="xui-expand-row-info" style={{float: 'right',width:'100px'}}>{order.status} </div>
								<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>{order.total_order_money}(元)</div>
								<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>{order.purchase_price}(元)/{order.total_count}(件)</div>
								<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'300px'}}>{order.product_name}</div>
								<div style={{clear:'both'}}></div>
							</div>
						)
					});
				return (
					<div className={class_name} style={{display:'none !important',margin:'5px 0px 5px 5px'}}>
						<div>
							<div className="xui-expand-row-info" style={{float: 'left',width:'180px'}}>订单号<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'right',width:'100px'}}>状态<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>总金额<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'right',width:'150px'}}>单价/件数<br></br></div>
							<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'300px'}}>商品名称<br></br></div>
							<div style={{clear:'both'}}></div>
							{products}
						</div>
					</div>
				)
			}
		}else if(field === 'fans'){
			return (
				<div>
					<span><img style={{width:'40px','height':'40px',borderRadius:'20px'}} src={data['fans_pic']}/></span>
					<span style={{marginLeft:'10px'}}>ID:{data['fans_id']}</span>
				</div>
			)
		}else if(field === 'purchase_index'){
			var percentage = data['purchase_index']+'%';
			return (
				<div className="xa-scales-div" title={percentage}>
					<div className="xa-scale-div" style={{width:data['purchase_index']}}>

					</div>
				</div>
			)
		}else if(field === 'diffusion_index'){
			var percentage = data['diffusion_index']+'%';
			return (
				<div className="xa-scales-div" title={percentage}>
					<div className="xa-scale-div" style={{width:data['diffusion_index']}}>

					</div>
				</div>
			)
		}else if(field === 'status'){
			var order_id = data['order_id'];
			var class_name = 'data-' +data['user_id'];
			var src = '';
			if(order_id != ''){
				src = '/order/customer_order_detail/?id='+order_id;
			}
			if(src != ''){
				return (
					<div>
						<a href="javascript:void(0);" onClick={this.showOrder.bind(this,class_name)}>{value}</a>
					</div>
				)
			}else{
				return (
					<div>
						{value}
					</div>
				)
			}
			
		}else{
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	render:function(){
		var productsResource = {
			resource: 'fans.fans',
			data: {
				page: 1
			}
		};
		var optionsForStatus = [{
			text: '全部', value: '-1'
		},{
			text: '已妥投，未阅读', value: '0'
		},{
			text: '已阅读，未分享', value: '1'
		},{
			text: '已阅读，已分享', value: '2'
		},{
			text: '已下单', value: '3'
		},{
			text: '已下单，已推荐', value: '4'
		}];
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormSelect label="状态:" name="status" options={optionsForStatus} match="=" />
						</Reactman.FilterField>
						<Reactman.FilterField></Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="粉丝" field="fans" />
						<Reactman.TableColumn name="购买指数" field="purchase_index" width='150'/>
						<Reactman.TableColumn name="推荐传播指数" field="diffusion_index" width='150'/>
						<Reactman.TableColumn name="状态" field="status" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = CustomerPage;