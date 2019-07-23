import Vue from 'vue'
import CoursePage from './CoursePage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(CoursePage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CoursePage }
}).$mount('#course-page');