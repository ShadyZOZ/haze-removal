webpackJsonp([1],{11:function(e,t,n){"use strict";var o=[{path:"/",meta:{title:""},component:function(e){return n.e(0).then(function(){var t=[n(39)];e.apply(null,t)}.bind(this)).catch(n.oe)}}];t.a=o},12:function(e,t){},13:function(e,t,n){var o=n(14)(n(32),n(36),null,null);o.options.__file="/home/shady/Workspace/haze-removal-ui/src/app.vue",o.esModule&&Object.keys(o.esModule).some(function(e){return"default"!==e&&"__esModule"!==e})&&console.error("named exports are not supported in *.vue files."),o.options.functional&&console.error("[vue-loader] app.vue: functional components are not supported with templates, they should use render functions."),e.exports=o.exports},14:function(e,t){e.exports=function(e,t,n,o){var r,u=e=e||{},a=typeof e.default;"object"!==a&&"function"!==a||(r=e,u=e.default);var s="function"==typeof u?u.options:u;if(t&&(s.render=t.render,s.staticRenderFns=t.staticRenderFns),n&&(s._scopeId=n),o){var i=Object.create(s.computed||null);Object.keys(o).forEach(function(e){var t=o[e];i[e]=function(){return t}}),s.computed=i}return{esModule:r,exports:u,options:s}}},32:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={data:function(){return{}},mounted:function(){},beforeDestroy:function(){},methods:{}}},33:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=n(1),r=n(2),u=n.n(r),a=n(3),s=n(11),i=n(13),c=n.n(i),f=n(12);n.n(f);o.default.use(a.a),o.default.use(u.a);var d={mode:"history",routes:s.a},l=new a.a(d);l.beforeEach(function(e,t,n){u.a.LoadingBar.start(),n()}),l.afterEach(function(){u.a.LoadingBar.finish(),window.scrollTo(0,0)}),new o.default({el:"#app",router:l,render:function(e){return e(c.a)}})},36:function(e,t,n){e.exports={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("router-view")],1)},staticRenderFns:[]},e.exports.render._withStripped=!0}},[33]);