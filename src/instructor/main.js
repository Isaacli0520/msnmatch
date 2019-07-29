import Vue from 'vue'
import InstructorPage from './InstructorPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

Vue.config.productionTip = false

new Vue({
    render: h => h(InstructorPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { InstructorPage }
  }).$mount('#instructor-page')
