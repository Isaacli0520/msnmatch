import Vue from 'vue'
import CourseInstructorPage from './CourseInstructorPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(CourseInstructorPage),
  vuetify: vuetify,
  components: { CourseInstructorPage }
}).$mount('#course-instructor-page');