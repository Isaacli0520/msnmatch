import Vue from 'vue'
import SkillPage from './SkillPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(SkillPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { SkillPage }
  }).$mount('#skill-page')
