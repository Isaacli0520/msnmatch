import Vue from 'vue'
import CourseInstructorPage from './CourseInstructorPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CourseInstructorPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CourseInstructorPage }
}).$mount('#course-instructor-page');