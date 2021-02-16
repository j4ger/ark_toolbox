module.exports = {
  publicPath:
    process.env.NODE_ENV === "production"
      ? "https://cdn.jsdelivr.net/gh/V04/ark_toolbox@latest/docs/"
      : "/",
  configureWebpack: {
    devtool: "source-map",
    optimization: {
      runtimeChunk: "single",
      splitChunks: {
        chunks: "all",
        maxInitialRequests: Infinity,
        cacheGroups: {
          vueVendor: {
            test: /[\\/]node_modules[\\/](vue|vuex|vue-meta|vue-property-decorator|vue-class-component)[\\/]/,
            name: "vuevendor"
          },
          utilsVendor: {
            test: /[\\/]node_modules[\\/](axios|lodash|lodashCombinations|)[\\/]/,
            name: "utilsvendor"
          }
        }
      },
      minimize: true,
      sideEffects: false
    }
  },
  outputDir: "docs",
  productionSourceMap: false
};
