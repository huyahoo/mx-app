import { getField, updateField } from 'vuex-map-fields';

const SET_LOCALE = 'SET_LOCALE';
const SET_CONFIGURATION = 'SET_CONFIGURATION';

export default {
  namespaced: true,
  state: {
    formData: {
      objectName: '',
      saveDestination: process.env.S3_BUCKET_NAME,
      model: 'Dust3r',
      removeBackground: false,
    },
  },
  getters: {
    getField,
  },
  actions: {
    setConfiguration({ commit }, payload) {
      commit(SET_LOCALE, payload);
    },
  },
  mutations: {
    updateField,
    SET_CONFIGURATION(state, payload) {
      state.formData = payload;
    },
  },
};
