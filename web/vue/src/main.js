import Vue from "vue";
import App from "./App.vue";
import axios from "axios";

import router from "./router";
import store from "./store";

import Spinner from "./components/Spinner";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

Vue.config.productionTip = false;

Vue.component('spinner', Spinner);

new Vue({
  store,
  router,
  render: (h) => h(App)
}).$mount("#thejumpoff");
