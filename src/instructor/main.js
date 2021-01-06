import Vue from 'vue'
import InstructorPage from './InstructorPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(InstructorPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { InstructorPage }
  }).$mount('#instructor-page')
