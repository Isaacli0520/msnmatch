import Vue from 'vue'
import ReviewsPage from './ReviewsPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(ReviewsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { ReviewsPage }
}).$mount('#reviews-page');