<template>
  <v-expansion-panels inset>
    <v-expand-transition
      v-for="(group, index) in sortedMatchedOperators"
      :key="index"
    >
      <v-expansion-panel @change="resetSlideSelected">
        <v-expansion-panel-header>
          <v-col cols="6" sm="10">
            <v-chip-group>
              <v-chip
                label
                :ripple="false"
                v-for="(tag, index) in group.tags"
                :key="index"
                :color="tagColor(tag)"
              >
                {{ tag }}
              </v-chip>
            </v-chip-group>
          </v-col>
          <v-col cols="2" sm="2">
            <v-rating
              :value="group.minRareness"
              :length="group.minRareness"
              readonly
              dense
              color="yellow darken-3"
              size="10"
            ></v-rating>
          </v-col>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-slide-group
            class="pa-1"
            center-active
            show-arrows
            v-model="slideSelected"
          >
            <v-slide-item
              v-for="(operator, index) in group.operators"
              v-slot="{ active, toggle }"
              :key="index"
            >
              <v-card
                outlined
                class="rounded-lg transition-swing ma-2 pa-2"
                @click="toggle"
                height="110"
                width="150"
                :color="active ? operatorColor[operator.rareness - 1] : ''"
              >
                <v-badge
                  bordered
                  bottom
                  :color="operatorColor[operator.rareness - 1]"
                  overlap
                  offset-x="10"
                  offset-y="10"
                  dot
                >
                  <v-avatar
                    size="50"
                    class="rounded-lg"
                    :color="$vuetify.theme.dark ? 'grey darken-4' : 'white'"
                  >
                    <v-img :src="operator.profile"></v-img>
                  </v-avatar>
                </v-badge>
                <div class="h4 font-weight-bold mt-1">
                  {{ operator.name }}
                </div>
                <div class="overline subtitle-2 mt-n2">
                  {{ operator.codename }}
                </div>
              </v-card>
            </v-slide-item>
          </v-slide-group>
          <v-expand-transition>
            <v-sheet v-if="slideSelected != null" height="200" tile>
              <v-card outlined>
                <v-list-item three-line>
                  <v-list-item-content>
                    <div class="overline mb-n4">
                      {{ group.operators[slideSelected].codename }}
                    </div>
                    <v-rating
                      color="yellow darken-2"
                      :value="group.operators[slideSelected].rareness"
                      :length="group.operators[slideSelected].rareness"
                      size="10"
                      readonly
                      dense
                    ></v-rating>
                    <v-list-item-title class="headline">
                      {{ group.operators[slideSelected].name }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="d-inline-block text-truncate">
                      {{
                        resolveTagsFromCode(
                          group.operators[slideSelected].tag
                        ).join(" ")
                      }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-avatar size="120">
                    <v-img
                      :src="group.operators[slideSelected].profile"
                    ></v-img>
                  </v-list-item-avatar>
                </v-list-item>
                <v-card-actions>
                  <v-btn
                    outlined
                    rounded
                    text
                    link
                    :href="
                      'http://prts.wiki/w/' +
                        group.operators[slideSelected].name
                    "
                  >
                    Wiki页面
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-sheet>
          </v-expand-transition>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expand-transition>
  </v-expansion-panels>
</template>

<script lang="ts">
import { MatchedOperators, resolveTagsFromCode } from "../OperatorInfo";
import { Component, Prop, Vue } from "vue-property-decorator";
import _ from "lodash";

@Component
export default class OperatorDisplay extends Vue {
  @Prop()
  matchedOperators!: MatchedOperators[];
  @Prop({ default: false })
  sortByMaxRareness!: boolean;

  slideSelected = null;

  resolveTagsFromCode = resolveTagsFromCode;

  get sortedMatchedOperators() {
    if (this.sortByMaxRareness) {
      return _.sortBy(this.matchedOperators, group => 7 - group.maxRareness);
    } else {
      return _.sortBy(this.matchedOperators, group => 7 - group.minRareness);
    }
  }

  operatorColor = [
    "grey lighten-1",
    "grey darken-2",
    "blue lighten-2",
    "deep-purple accent-2",
    "yellow darken-2",
    "orange"
  ];

  tagColor(tag: string): string {
    if (tag == "资深干员") return "yellow darken-2";
    else if (tag == "高级资深干员") return "orange";
    else return "accent";
  }

  resetSlideSelected(): void {
    this.slideSelected = null;
  }
}
</script>
