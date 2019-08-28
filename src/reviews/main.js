import Vue from 'vue'
import ReviewsPage from './ReviewsPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = {}

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(ReviewsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { ReviewsPage }
}).$mount('#reviews-page');