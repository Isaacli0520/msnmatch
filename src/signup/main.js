import Vue from 'vue'
import SignUpPage from './SignUpPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(SignUpPage),
    vuetify: vuetify,
    components: { SignUpPage }
  }).$mount('#signup-page')
