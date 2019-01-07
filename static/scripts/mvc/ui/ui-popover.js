define("mvc/ui/ui-popover",["exports","backbone","underscore","utils/utils"],function(t,e,i,s){"use strict";function o(t){if(t&&t.__esModule)return t;var e={};if(null!=t)for(var i in t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i]);return e.default=t,e}Object.defineProperty(t,"__esModule",{value:!0});var n=o(e),l=o(i),p=function(t){return t&&t.__esModule?t:{default:t}}(s),h=n.View.extend({optionsDefault:{with_close:!0,title:null,placement:"top",container:"body",body:null},initialize:function(t){this.setElement(this._template()),this.uid=p.default.uid(),this.options=l.defaults(t||{},this.optionsDefault),this.options.container.parent().append(this.el),this.$title=this.$(".popover-title-label"),this.$close=this.$(".popover-close"),this.$body=this.$(".popover-content"),this.options.body&&this.append(this.options.body);var e=this;$("body").on("mousedown."+this.uid,function(t){!e.visible||$(e.options.container).is(t.target)||$(e.el).is(t.target)||0!==$(e.el).has(t.target).length||e.hide()})},render:function(){this.$title.html(this.options.title),this.$el.removeClass().addClass("ui-popover popover in").addClass(this.options.placement),this.$el.css(this._get_placement(this.options.placement));var t=this;this.options.with_close?this.$close.on("click",function(){t.hide()}).show():this.$close.off().hide()},title:function(t){void 0!==t&&(this.options.title=t,this.$title.html(t))},show:function(){this.render(),this.$el.show(),this.visible=!0},hide:function(){this.$el.hide(),this.visible=!1},append:function(t){this.$body.append(t)},empty:function(){this.$body.empty()},remove:function(){$("body").off("mousedown."+this.uid),this.$el.remove()},_get_placement:function(t){var e,i,s=this._get_width(this.$el),o=this.$el.height(),n=this.options.container,l=this._get_width(n),p=this._get_height(n),h=n.position();if(e=i=0,-1!=["top","bottom"].indexOf(t))switch(i=h.left-s+(l+s)/2,t){case"top":e=h.top-o-5;break;case"bottom":e=h.top+p+5}else switch(e=h.top-o+(p+o)/2,t){case"right":i=h.left+l}return{top:e,left:i}},_get_width:function(t){return t.width()+parseInt(t.css("padding-left"))+parseInt(t.css("margin-left"))+parseInt(t.css("padding-right"))+parseInt(t.css("margin-right"))},_get_height:function(t){return t.height()+parseInt(t.css("padding-top"))+parseInt(t.css("padding-bottom"))},_template:function(t){return'<div class="ui-popover popover fade in"><div class="arrow"/><div class="popover-title"><div class="popover-title-label"/><div class="popover-close fa fa-times-circle"/></div><div class="popover-content"/></div>'}});t.default={View:h}});
//# sourceMappingURL=../../../maps/mvc/ui/ui-popover.js.map