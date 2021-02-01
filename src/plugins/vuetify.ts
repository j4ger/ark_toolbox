import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";
import zhHans from "vuetify/src/locale/zh-Hans";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        accent: "#9e9e9e"
      }
    }
  },
  lang: {
    locales: { zhHans },
    current: "zhHans"
  }
});
