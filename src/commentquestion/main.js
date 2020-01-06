import Vue from 'vue'
import CommentQuestionPage from './CommentQuestionPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(CommentQuestionPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentQuestionPage }
}).$mount('#comment-question-page');