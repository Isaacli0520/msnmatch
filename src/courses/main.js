import Vue from 'vue'
import CoursesPage from './CoursesPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CoursesPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CoursesPage }
}).$mount('#courses-page');