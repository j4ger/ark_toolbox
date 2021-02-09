module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/ark_toolbox/" : "/",
  configureWebpack: {
    devtool: "source-map"
  },
  outputDir: "docs",
  productionSourceMap: false
};
