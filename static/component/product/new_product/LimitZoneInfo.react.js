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


//        var data = Store.getData();
//        var limit_zone_type = data.limit_zone_type;
//        var limit_zone_info = data.limit_zone_info;
//        console.log(limit_zone_type, limit_zone_info)
		return Store.getData();
	},

	onChangeStore: function(){

		this.setState(Store.getData());
	},

	render: function() {

//        console.log('==================================2')
////
//	    console.log(this.state.limit_zone_type=='1' || this.state.limit_zone_type=='2')
	    if(this.state.limit_zone_type=='1' || this.state.limit_zone_type=='2'){
	        return (
	            <div>
                    <div>
                        <Reactman.FormSelect name='limit_zone_id' value={this.state.limit_zone_id}
                                label="地区限制:"
                                options={this.state.limit_zone_info } validate="require" onChange={this.props.onChange}/>
                    </div>
                    <div style={{paddingLeft:'180px',marginBottom:'10px'}}>
                        <a  className="btn btn-success mr40 xa-submit xui-fontBold" href="/limit_zone/template_list" >配置模板</a>
                    </div>
                </div>
	        )

	    }else{
	        return (
	            <div></div>
	        )
	    }

	}
});
module.exports = LimitZoneInfo;