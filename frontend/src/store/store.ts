import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import VuexPersist from 'vuex-persist';
import { vuexOidcCreateStoreModule, VuexOidcStoreListeners } from 'vuex-oidc';
import { User } from 'oidc-client';
import Pool from '@/store/modules/Pool';
import Auth from '@/store/modules/Auth';
import CIDR from '@/store/modules/CIDR';
import Search from '@/store/modules/Search';
import Token from '@/store/modules/Token';
import { RootState } from '@/types/store';
import { SIPAMConfiguration } from '@/config';
import { Api } from '@/types/api';

export default function storeFactory(config: SIPAMConfiguration, SIPAM: Api) {
  Vue.use(Vuex);

  const listeners: VuexOidcStoreListeners = {
    userLoaded: (user: User) => SIPAM.setSecurityData(user.access_token),
    userUnloaded: () => SIPAM.setSecurityData(null),
  };

  const AuthOIDC = vuexOidcCreateStoreModule(config.oidcSettings, { namespaced: true }, listeners);

  const vuexLocalStorage = new VuexPersist({
    key: 'vuex', // The key to store the state on in the storage provider.
    storage: window.localStorage, // or window.sessionStorage or localStorage
    // Function that passes the state and returns the state with only the objects you want to store.
    reducer: (state: any) => ({
      Auth: state.Auth,
    }),
  });

  const storeOptions: StoreOptions<RootState> = {
    state: {
      version: '1.0.0', // a simple property
      config,
      api: SIPAM,
    },
    modules: {
      CIDR,
      Pool,
      Search,
      Auth,
      Token,
      AuthOIDC,
    },
    plugins: [vuexLocalStorage.plugin],
    strict: import.meta.env.DEV,
  };
  return new Vuex.Store<RootState>(storeOptions);
}
