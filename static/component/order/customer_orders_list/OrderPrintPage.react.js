/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var OrderPrintPage = Reactman.createDialog({
	getInitialState: function() {
		return {}
	},

	render:function(){
		var templates = JSON.parse(this.props.templates);

		var orderPage = '';
		if(templates.length>0) {
			orderPage = templates.map(function(template, index){
				return(
					<div style={{marginBottom:'50px'}} key={index} dangerouslySetInnerHTML={{__html: template.template}}></div>	
				)
			})
		}

		return (
			<div className="order-print-page" style={{height: '0px', position: 'absolute', zIndex: '-999999'}}>
				{orderPage}
			</div>
		)
	}
})


module.exports = OrderPrintPage;