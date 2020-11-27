import Vue from 'vue'
import MyCoursesPage from './MyCoursesPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(MyCoursesPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { MyCoursesPage }
}).$mount('#my-courses-page');