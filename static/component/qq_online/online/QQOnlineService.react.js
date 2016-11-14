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
require('./style.css');
var W = Reactman.W;

var QQOnlineService = React.createClass({
	onHandleClickClose: function() {
		$('.xui-open').animate({'width': '0'}, function() {
			$('.xui-open').css({'display': 'none'});
			$('.xui-close').css({'display': 'inline-block'});
		});	
	},

	onHandleClickOpen: function() {
		$('.xui-close').css({'display': 'none'});
		$('.xui-open').css({'display': 'inline-block'});
		$('.xui-open').animate({'width': '120px'})
	},

	render:function(){
		var serviceQQFirst = this.props.serviceQQFirst;
		var serviceQQSecond = this.props.serviceQQSecond;
		var serviceTel = this.props.serviceTel;
		serviceQQFirst = serviceQQFirst? serviceQQFirst: serviceQQSecond;
		var qqOneContact = "http://wpa.qq.com/msgrd?V=1&exe=qq&Site=qq&menu=yes&uin="+ serviceQQFirst;
		var qqTwoContact = "http://wpa.qq.com/msgrd?V=1&exe=qq&Site=qq&menu=yes&uin="+ serviceQQSecond;
		if(!serviceQQFirst && !serviceQQSecond && !serviceTel){
			return(
				<div></div>
			)
		}
		return (
			<div className="xui-contact-box">
				<a href="javescript:void(0)" onClick={this.onHandleClickOpen} className="xui-close" style={{display:'inline-block'}}>
					<p className="xui-close-text">联系客服</p>
					<p className="xui-close-icon"></p>
				</a>
				<div className="xui-open">
					<div className="xui-header-box">
						<p className="xui-title">客服咨询</p>
					</div>
					<a href={qqOneContact} target="_blank" className="xui-qq xui-qq1">
						<p className="xui-qq-box"><i className="xui-qq-img"></i></p>
						<p className="xui-qq-text">QQ咨询1</p>
					</a>
					<a style={{display:'none'}} href={qqTwoContact} target="_blank" className="xui-qq xui-qq2">
						<p className="xui-qq-box"><i className="xui-qq-img"></i></p>
						<p className="xui-qq-text">QQ咨询2</p>
					</a>
					<div>
						<p className="xui-phone">{serviceTel}</p>
						<p className="xui-phone-text"><i></i>客服电话</p>
					</div>
					<a href="javescript:void(0)" onClick={this.onHandleClickClose} className="xui-open-icon"></a>
				</div>
			</div>
		)
	}
})
module.exports = QQOnlineService;