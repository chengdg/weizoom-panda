/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_limit_zone.LimitZoneText');
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css')

var LimitZoneText = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var data = this.props.info;
//		console.log('+++++++++++++++++++++++++++++++=');
//		console.log(data)
		return {
            data: data
		}
	},

	onChange: function(value, event) {

	},

	onChangeStore: function() {
		this.setState({
			selectLabels: Store.getData().selectLabels,
			selectCatalogLabels: Store.getData().selectCatalogLabels
		});
	},

	render: function() {
          var text = this.state.data.map(function(model, index){
//            console.log('+++++++++++++++++++++++++++++++=')
//            console.log(model)
            return(
                <div>{model.province}:{model.cities}</div>
            )
          });
//        for(var i=0; i < this.state.data.length; i++){
//            text += <div>this.state.data[i].province  ':'  this.state.data[i].cities</div>
//        }
		return (
			<div>
			{text}
			</div>
		)
	}
})
module.exports = LimitZoneText;