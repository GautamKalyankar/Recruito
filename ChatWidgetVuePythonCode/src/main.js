import '@babel/polyfill'
import 'core-js/stable'
import 'regenerator-runtime/runtime';
import Vue from 'vue'
import App from './App.vue'
import Chat from 'vue-beautiful-chat'
import Vuex from 'vuex'

Vue.config.productionTip = false
Vue.use(Chat, {})
Vue.use(Vuex);




export const store = new Vuex.Store({
    state: {
        userId: "",
        messageId: "",
        sessionAttributes: {},
        clickedRefresh: false,
        messageReceived: false,
        firstInput: ""
    }
})

new Vue({
    render: h => h(App),
    store: store
}).$mount('#app')