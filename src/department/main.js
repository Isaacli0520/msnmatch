import Vue from 'vue'
import DepartmentPage from './DepartmentPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(DepartmentPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { DepartmentPage }
}).$mount('#department-page');