import Vue from 'vue'
import DepartmentsPage from './DepartmentsPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(DepartmentsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { DepartmentsPage }
}).$mount('#departments-page');