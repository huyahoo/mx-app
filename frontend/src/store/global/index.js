import { getField, updateField } from 'vuex-map-fields';

const SET_LOCALE = 'SET_LOCALE';
const SET_CONFIGURATION = 'SET_CONFIGURATION';

export default {
  namespaced: true,
  state: {
    formData: {
      objectName: 'astronaut',
      saveDestination: 'visualize-3d-object-vr-dev',
      model: 'Dust3r'
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
