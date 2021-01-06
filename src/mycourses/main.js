import Vue from 'vue'
import MyCoursesPage from './MyCoursesPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(MyCoursesPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { MyCoursesPage }
}).$mount('#my-courses-page');