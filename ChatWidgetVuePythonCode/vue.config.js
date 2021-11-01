module.exports = {
    configureWebpack: {
        optimization: {
            splitChunks: false
        },
        devtool: 'source-map'
    },
    css: {
        extract: false,
    },
    transpileDependencies: ["msgdown", "vuetify", "vue", "vuex", "escape-goat", "vue-beautiful-chat"]
}