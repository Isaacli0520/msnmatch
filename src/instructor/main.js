import Vue from 'vue'
import InstructorPage from './InstructorPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(InstructorPage),
    vuetify: vuetify,
    components: { InstructorPage }
  }).$mount('#instructor-page')
