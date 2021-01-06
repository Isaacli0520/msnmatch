import Vue from 'vue'
import DepartmentPage from './DepartmentPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(DepartmentPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { DepartmentPage }
}).$mount('#department-page');