import Vue from 'vue'
import CoursesPage from './CoursesPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(CoursesPage),
  vuetify: vuetify,
  components: { CoursesPage }
}).$mount('#courses-page');