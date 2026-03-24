const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    allowedHosts: "all",
    proxy: {
      '^/api/.*': {
        target: 'https://foxmarchingwarriors.band/',
      },
    }
  },

})
