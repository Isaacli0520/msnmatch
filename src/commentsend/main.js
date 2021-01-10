import Vue from 'vue'
import CommentSendPage from './CommentSendPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CommentSendPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentSendPage }
}).$mount('#comment-send-page');