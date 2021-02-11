module.exports = {
  publicPath:
    process.env.NODE_ENV === "production"
      ? "https://cdn.jsdelivr.net/gh/V04/ark_toolbox@latest/docs/"
      : "/",
  configureWebpack: {
    devtool: "source-map"
  },
  outputDir: "docs",
  productionSourceMap: false
};
