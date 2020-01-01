import Vue from 'vue'
import CommentCreatePage from './CommentCreatePage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(CommentCreatePage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentCreatePage }
}).$mount('#comment-create-page');