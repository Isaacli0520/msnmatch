import Vue from 'vue'
import DepartmentPage from './DepartmentPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(DepartmentPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { DepartmentPage }
}).$mount('#department-page');