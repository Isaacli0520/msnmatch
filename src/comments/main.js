import Vue from 'vue'
import CommentsPage from './CommentsPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(CommentsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentsPage }
}).$mount('#comments-page');