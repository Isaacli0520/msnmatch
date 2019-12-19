import Vue from 'vue'
import CommentFilterPage from './CommentFilterPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(CommentFilterPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentFilterPage }
}).$mount('#comment-filter-page');