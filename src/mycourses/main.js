import Vue from 'vue'
import MyCoursesPage from './MyCoursesPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(MyCoursesPage),
  vuetify: vuetify,
  components: { MyCoursesPage }
}).$mount('#my-courses-page');