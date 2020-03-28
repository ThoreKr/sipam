import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import I18n from 'vue-i18n';
import './assets/styles/custom.scss';

import './registerServiceWorker';
import BootstrapVueTreeview from 'bootstrap-vue-treeview';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlusCircle, faMinusCircle, faCog } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import axios from 'axios';
import Language from './components/Language';
import store from './store/store';
import router from './router';
import App from './App.vue';

// Icons
library.add(faPlusCircle, faMinusCircle, faCog);
Vue.component('fai', FontAwesomeIcon);

// Bootstap
Vue.use(BootstrapVue);
Vue.use(I18n);
Vue.use(BootstrapVueTreeview);

Vue.config.productionTip = false;

// Axios Connection Config
// TODO: Move to webpack envs
axios.defaults.baseURL = process.env.VUE_APP_API_URL;
axios.defaults.timeout = 15000;
axios.defaults.headers.accept = 'application/json';

axios.interceptors.response.use(
  response => response, (error) => {
    const originalRequest = error.config;
    const status = error.response ? error.response.status : null;

    if (status === 401 && originalRequest.url === `${axios.baseURL}/jwt/refresh/`) {
      store.dispatch('Auth/DELETE_TOKEN');
      router.push('/login');
      return Promise.reject(error);
    }
    if (status === 401 && !originalRequest.retry) {
      originalRequest.retry = true;
      return store.dispatch('Auth/REFRESH', {
        token: store.getters['Auth/token'],
        callback: () => {
          // eslint-disable-next-line no-param-reassign
          axios.defaults.headers.common.Authorization = `Bearer ${store.getters['Auth/token'].access}`;
          return axios.request(originalRequest);
        },
      });
    }

    return Promise.reject(error);
  },
);

const i18n = new I18n();
Language.init(i18n);

new Vue({
  router,
  store,
  i18n,
  render: h => h(App),
}).$mount('#app');
