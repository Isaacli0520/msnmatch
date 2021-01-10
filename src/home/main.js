import Vue from 'vue'
import HomePage from './HomePage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(HomePage),
    vuetify: vuetify,
    components: { HomePage }
  }).$mount('#home-page')
