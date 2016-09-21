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
		var data = this.props.info;
		
		return {
            data: data
		}
	},

	render: function() {
        var text = this.props.info.map(function(model, index){
            return(
                <div>{model.province}:{model.cities}</div>
            )
        });

		return (
			<div>
				{text}
			</div>
		)
	}
})
module.exports = LimitZoneText;