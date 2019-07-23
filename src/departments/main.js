import Vue from 'vue'
import DepartmentsPage from './DepartmentsPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(DepartmentsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { DepartmentsPage }
}).$mount('departments-page');