import Vue from 'vue'
import SkillsPage from './SkillsPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(SkillsPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { SkillsPage }
  }).$mount('#skills-page')
