import Vue from 'vue'
import CategoryPage from './CategoryPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(CategoryPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CategoryPage }
}).$mount('#category-page');