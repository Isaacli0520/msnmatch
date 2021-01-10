import Vue from 'vue'
import DepartmentPage from './DepartmentPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(DepartmentPage),
  vuetify: vuetify,
  components: { DepartmentPage }
}).$mount('#department-page');