import Vue from 'vue'
import CoursesAdminPage from './CoursesAdminPage.vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify);

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(CoursesAdminPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CoursesAdminPage }
}).$mount('#courses-admin-page');