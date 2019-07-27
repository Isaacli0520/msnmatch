import Vue from 'vue'
import MyCoursesPage from './MyCoursesPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(MyCoursesPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { MyCoursesPage }
}).$mount('#my-courses-page');