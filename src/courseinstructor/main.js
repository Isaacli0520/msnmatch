import Vue from 'vue'
import CourseInstructorPage from './CourseInstructorPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
}

new Vue({
  render: h => h(CourseInstructorPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CourseInstructorPage }
}).$mount('#course-instructor-page');