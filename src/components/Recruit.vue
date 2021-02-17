<template>
  <v-container>
    <v-col cols="12" sm="8" offset-sm="2">
      <v-sheet
        :color="$vuetify.theme.dark ? 'grey darken-4' : 'white'"
        class="pt-4"
      >
        <v-expand-transition>
          <div v-show="showTags">
            <v-container class="d-inline-flex flex-column">
              <v-row
                v-for="(group, name, index) in tags"
                :key="index"
                cols="12"
              >
                <v-sheet
                  class="pa-4"
                  id="groups"
                  :color="$vuetify.theme.dark ? 'grey darken-4' : 'white'"
                >
                  <h3 class="medium-text-weight text-left mx-2">{{ name }}</h3>
                  <v-chip-group
                    v-model="selected[name]"
                    multiple
                    column
                    justify="space-around"
                  >
                    <v-chip
                      v-for="(value, tag) in group"
                      :key="value"
                      :value="value"
                      :disabled="tagsDisabled"
                      filter
                      label
                      :color="tagColor(tag)"
                      >{{ tag }}</v-chip
                    >
                  </v-chip-group>
                  <v-divider></v-divider>
                </v-sheet>
              </v-row>
            </v-container>
          </div>
        </v-expand-transition>
        <v-row class="mt-2 mx-0">
          <operator-display
            :matchedOperators="matchedOperators"
            :sortByMaxRareness="sortByMaxRareness"
            ref="operatorDisplay"
          ></operator-display>
        </v-row>

        <v-snackbar v-model="showSnackBar" :timeout="5000">
          兄啊，选太多标签了
          <template v-slot:action="{ attrs }">
            <v-btn color="blue" text v-bind="attrs" @click="resetTags">
              重置
            </v-btn>
            <v-btn
              color="pink"
              text
              v-bind="attrs"
              @click="showSnackBar = false"
            >
              日恁毛
            </v-btn>
          </template>
        </v-snackbar>

        <v-bottom-sheet v-model="bottomSheet" inset>
          <v-list>
            <v-subheader>功能菜单</v-subheader>
            <v-list-item
              @click="
                $vuetify.theme.dark = !$vuetify.theme.dark;
                bottomSheet = false;
                updateLocalStorage();
              "
            >
              <v-list-item-avatar>
                <v-icon v-if="$vuetify.theme.dark"
                  >mdi-white-balance-sunny</v-icon
                >
                <v-icon v-else>mdi-moon-waning-crescent</v-icon>
              </v-list-item-avatar>
              <v-list-item-title>{{
                $vuetify.theme.dark ? "关闭黑暗模式" : "切换至黑暗模式"
              }}</v-list-item-title>
            </v-list-item>
            <v-list-item
              @click="
                resetTags();
                bottomSheet = false;
              "
            >
              <v-list-item-avatar>
                <v-icon>mdi-autorenew</v-icon>
              </v-list-item-avatar>
              <v-list-item-title>重置标签组</v-list-item-title>
            </v-list-item>
            <v-list-item
              @click="
                showTags = !showTags;
                bottomSheet = false;
              "
            >
              <v-list-item-avatar>
                <v-icon v-if="showTags">mdi-unfold-less-horizontal</v-icon>
                <v-icon v-else>mdi-unfold-more-horizontal</v-icon>
              </v-list-item-avatar>
              <v-list-item-title>{{
                showTags ? "折叠标签组" : "展开标签组"
              }}</v-list-item-title>
            </v-list-item>
            <v-list-item
              @click="
                sortByMaxRareness = !sortByMaxRareness;
                bottomSheet = false;
              "
            >
              <v-list-item-avatar>
                <v-icon v-if="sortByMaxRareness"
                  >mdi-chevron-triple-down</v-icon
                >
                <v-icon v-else>mdi-chevron-triple-up</v-icon>
              </v-list-item-avatar>
              <v-list-item-title>{{
                sortByMaxRareness
                  ? "根据可能的最高稀有度排序"
                  : "根据保底的最低稀有度排序"
              }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-bottom-sheet>
      </v-sheet>
    </v-col>
    <v-overlay v-model="showOverlay" opacity="0.75">
      <v-avatar size="60" v-if="overlayError">
        <v-icon x-large>mdi-cloud-question</v-icon>
      </v-avatar>
      <v-progress-circular
        indeterminate
        color="primary"
        :value="fetchProgress"
        v-else
        size="30"
        class="mb-4"
      ></v-progress-circular>
      <div class="h1">{{ overlayCaption }}</div>
      <div class="subtitle-2" v-if="overlayError">
        {{ overlayErrorMessage }}
      </div>
    </v-overlay>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, Watch, Ref } from "vue-property-decorator";
import { concat, pull, flatMap, sortBy, has } from "lodash";
import axios from "axios";
import lodashCombinations from "../lodashCombinations";
import {
  tagsGrouped,
  TagsSelected,
  MatchedOperators,
  OperatorInfo,
  getMatchedOperators
} from "../OperatorInfo";
const OperatorDisplay = () =>
  import(
    /* webpackChunkName: "/OperatorDisplay" */
    "./OperatorDisplay.vue"
  );

@Component({ components: { OperatorDisplay } })
export default class Recruit extends Vue {
  @Ref()
  operatorDisplay!: any;

  tags = tagsGrouped;

  bottomSheet = false;
  showTags = true;
  sortByMaxRareness = false;
  showSnackBar = false;
  tagsDisabled = false;
  showOverlay = false;
  overlayCaption = "获取资源中……";
  overlayError = false;
  overlayErrorMessage = "";
  fetchProgress = 0;
  fab = false;
  selected: TagsSelected = { 获得途径: [1] };

  operators: OperatorInfo[] = [];

  mounted() {
    this.showOverlay = true;
    axios
      .request<OperatorInfo[]>({
        url:
          "https://cdn.jsdelivr.net/gh/j4ger/ark_toolbox@latest/scraper/operators.json",
        onDownloadProgress: progressEvent => {
          if (progressEvent.lengthComputable) {
            this.fetchProgress =
              (100 * progressEvent.loaded) / progressEvent.total;
          }
        }
      })
      .then(response => {
        const { data } = response;
        this.operators = data;
        this.showOverlay = false;
      })
      .catch(error => {
        this.overlayCaption = "出错了！请尝试刷新";
        this.overlayErrorMessage = error.message;
        this.overlayError = true;
      });
  }

  get matchedOperators(): MatchedOperators[] {
    const baseElements: number[][] = [
      this.selected.获得途径?.length == 1 ? [1] : [0],
      concat(this.selected.职业 ?? [], [0]),
      concat(this.selected.部署位 ?? [], [0]),
      concat(this.selected.性别 ?? [], [0]),

      [0]
    ];

    if (has(this.selected, "一般标签")) {
      baseElements[4] = concat(
        [0],
        flatMap(this.selected.一般标签, (v, i, a) =>
          lodashCombinations(a, i + 1).map(each =>
            each.reduce((sum, element) => sum + element)
          )
        )
      );
    }

    const finalCombinations: number[] = [];

    baseElements[0].forEach(element1 => {
      baseElements[1].forEach(element2 => {
        baseElements[2].forEach(element3 => {
          baseElements[3].forEach(element4 => {
            baseElements[4].forEach(element5 => {
              finalCombinations.push(
                element1 + element2 + element3 + element4 + element5
              );
            });
          });
        });
      });
    });
    pull(finalCombinations, 0);
    pull(finalCombinations, 1);

    const result: MatchedOperators[] = [];
    finalCombinations.forEach(element => {
      const matches = getMatchedOperators(this.operators, element);
      if (matches != null) {
        result.push(matches);
      }
    });
    return sortBy(result, group => 10 - group.tags.length);
  }

  tagColor(tag: string): string {
    if (tag == "资深干员") return "yellow darken-2";
    else if (tag == "高级资深干员") return "orange";
    else return "accent";
  }

  resetTags(): void {
    this.selected = { 获得途径: [1] };
    this.tagsDisabled = false;
  }

  updateLocalStorage(): void {
    localStorage.darkMode = this.$vuetify.theme.dark;
  }

  @Watch("selected", { deep: true })
  onSelectedChanged(newValue: TagsSelected): void {
    let total = 0;
    for (const members of Object.values(newValue)) {
      total += members.length;
    }
    if (total == 7) {
      this.showSnackBar = true;
      this.tagsDisabled = true;
    }
  }

  openBottomSheet() {
    this.bottomSheet = true;
  }
}
</script>
<style>
#groups .v-slide-group__wrapper {
  touch-action: auto;
}
</style>
