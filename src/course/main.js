import Vue from 'vue'
import CoursePage from './CoursePage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(CoursePage),
  vuetify: vuetify,
  components: { CoursePage }
}).$mount('#course-page');