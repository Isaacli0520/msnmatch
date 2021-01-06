import Vue from 'vue'
import HomePage from './HomePage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(HomePage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { HomePage }
  }).$mount('#home-page')
