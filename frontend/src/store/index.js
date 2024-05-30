import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import global from './global';

export default createStore({
  plugins: [
    createPersistedState({
      key: 'my-app',
      paths: ['user', 'token'],
    }),
  ],
  modules: {
    global,
  },
});
