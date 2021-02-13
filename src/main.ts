import Vue from "vue";
import App from "./App.vue";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueMeta from "vue-meta";
import "@babel/polyfill";

Vue.config.productionTip = false;

Vue.use(VueMeta);

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
