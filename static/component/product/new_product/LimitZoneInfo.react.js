/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:ProductModelInfo');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var AddProductModelDialog = require('./AddProductModelDialog.react');
var SetValidataTimeDialog = require('./SetValidataTimeDialog.react');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./ProductModelInfo.css');

var LimitZoneInfo = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);


        var data = Store.getData();
        var limit_zone_type = data.limit_zone_type;
        var limit_zone_info = data.limit_zone_info;
        console.log(limit_zone_type, limit_zone_info)
		return Store.getData();
	},

	onChangeStore: function(){

		this.setState(Store.getData());
	},

	render: function() {
	    var limit_zone_info = '';
	    var button = '';
        console.log('==================================2')
	    console.log(this.state.limit_zone_type)
	    if(this.state.limit_zone_type!=0){
            limit_zone_info = <Reactman.FormSelect name='limit_zone_info'
                label="地区限制:"
                options={this.state.limit_zone_info }  />
            button = <div style={{paddingLeft:'180px',marginBottom:'10px'}}><a  className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" >配置模板</a></div>
	    }
        return (
                <div>
                    <div>{limit_zone_info}</div>
                        {button}
                </div>
            )
	}
});
module.exports = LimitZoneInfo;