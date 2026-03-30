const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,

  publicPath: process.env.NODE_ENV === 'production'
    ? 'https://storage.googleapis.com/foxmarchingwarriors-static/'
    : '/',

  devServer: {
    allowedHosts: "all",
    proxy: {
      '^/api/.*': {
        target: 'https://foxmarchingwarriors.band',
      },
    }
  },

  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({ process: 'process/browser' }),
    ],
    resolve: {
      fallback: {
        crypto: require.resolve("crypto-browserify"),
        stream: require.resolve("stream-browserify"),
        util: require.resolve("util/"),
        vm: require.resolve("vm-browserify"),
      },
    },
  },
})
