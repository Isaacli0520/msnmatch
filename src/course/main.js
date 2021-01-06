import Vue from 'vue'
import CoursePage from './CoursePage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CoursePage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CoursePage }
}).$mount('#course-page');