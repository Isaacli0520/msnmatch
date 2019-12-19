import Vue from 'vue'
import CommentSendPage from './CommentSendPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(CommentSendPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentSendPage }
}).$mount('#comment-send-page');