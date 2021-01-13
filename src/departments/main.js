import Vue from 'vue'
import DepartmentsPage from './DepartmentsPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(DepartmentsPage),
  vuetify: vuetify,
  components: { DepartmentsPage }
}).$mount('#departments-page');