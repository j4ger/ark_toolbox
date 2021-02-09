<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
      <v-toolbar-title>公开招募计算器</v-toolbar-title>
      <v-spacer> </v-spacer>
      <v-btn icon @click="openBottomSheetClicked">
        <v-icon>mdi-menu-open</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer temporary v-model="drawer" app>
      <v-list-item>
        <v-list-item two-line link href="https://ak.rua.best/">
          <v-list-item-avatar tile size="40">
            <v-img src="./assets/favicon.png"></v-img>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>明日方舟工具箱</v-list-item-title>
            <v-list-item-subtitle>ak.rua.best</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav shaped>
        <v-list-item v-for="(item, index) in navItems" :key="index" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content href="item.href">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="pt-0">
      <recruit :openBottomSheet="openBottomSheet" ref="recruit"></recruit>
    </v-main>
    <v-footer padless class="pt-4">
      <v-col cols="12" sm="8" offset-sm="2">
        <v-row class="justify-center">
          <strong class="subheading">Built with ❤ by Void04</strong>
        </v-row>
        <v-row class="d-flex justify-center">
          <v-btn link icon href="https://github.com/hx64/ark_toolbox">
            <v-icon size="24">mdi-github</v-icon>
          </v-btn>
          <v-btn link icon href="https://space.bilibili.com/26888199">
            <v-icon size="24">mdi-television-classic</v-icon>
          </v-btn>
        </v-row>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue, Ref, Watch } from "vue-property-decorator";
import Recruit from "./components/Recruit.vue";

@Component({
  components: { Recruit }
})
export default class App extends Vue {
  @Ref()
  recruit!: Recruit;

  openBottomSheet = false;
  drawer = false;

  darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)").matches;

  navItems = [
    {
      title: "公开招募计算器",
      icon: "mdi-magnify",
      href: "https://ak.rua.best/recruit"
    }
  ];

  openBottomSheetClicked(): void {
    this.recruit.openBottomSheet();
  }

  mounted(): void {
    if (this.darkThemeMq) {
      this.$vuetify.theme.dark = true;
    } else if (localStorage.darkMode) {
      this.$vuetify.theme.dark = localStorage.darkMode;
    }
  }

  @Watch("darkThemeMq")
  onDarkModeChanged(): void {
    this.$vuetify.theme.dark = this.darkThemeMq;
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}
</style>
