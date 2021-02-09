<template>
  <v-container>
    <v-row>
      <v-expansion-panels accordion>
        <v-expand-transition
          v-for="(group, index) in sortedMatchedOperators"
          :key="index"
        >
          <v-expansion-panel>
            <v-expansion-panel-header
              :color="$vuetify.theme.dark ? 'grey darken-4' : 'white'"
            >
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
              <v-col cols="2">
                <v-badge
                  color="grey"
                  inline
                  icon="mdi-robot"
                  v-if="group.robot"
                >
                  <v-rating
                    :value="group.minRareness"
                    :length="group.minRareness"
                    readonly
                    dense
                    color="yellow darken-3"
                    size="10"
                  ></v-rating>
                </v-badge>
                <v-rating
                  v-else
                  :value="group.minRareness"
                  :length="group.minRareness"
                  readonly
                  dense
                  color="yellow darken-3"
                  size="10"
                ></v-rating>
              </v-col>
            </v-expansion-panel-header>
            <v-expansion-panel-content
              :color="$vuetify.theme.dark ? 'grey darken-4' : 'white'"
            >
              <v-item-group v-model="selected">
                <v-row>
                  <v-col
                    v-for="operator in group.operators"
                    :key="operator.name"
                    cols="4"
                    sm="2"
                  >
                    <v-item v-slot="{ active, toggle }" :value="operator">
                      <v-card
                        outlined
                        class="rounded-lg ma-0 pt-2"
                        @click.stop="
                          toggle();
                          showDialog = true;
                        "
                        height="110"
                        width="135"
                        :color="
                          active ? operatorColor[operator.rareness - 1] : ''
                        "
                      >
                        <v-badge
                          bordered
                          bottom
                          :color="operatorColor[operator.rareness - 1]"
                          offset-x="10"
                          offset-y="10"
                          dot
                        >
                          <v-avatar
                            size="60"
                            class="rounded-lg"
                            :color="
                              $vuetify.theme.dark ? 'grey darken-4' : 'white'
                            "
                          >
                            <v-img :src="operator.profile"></v-img>
                          </v-avatar>
                        </v-badge>
                        <div class="h4 font-weight-bold mt-1">
                          {{ operator.name }}
                        </div>
                      </v-card>
                    </v-item>
                  </v-col>
                </v-row>
              </v-item-group>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expand-transition>
      </v-expansion-panels>
    </v-row>
    <v-row>
      <v-dialog v-if="selected != null" v-model="showDialog" max-width="600">
        <v-card outlined>
          <v-list-item three-line>
            <v-list-item-content>
              <div class="overline mb-n4">
                {{ selected.codename }}
              </div>
              <v-rating
                color="yellow darken-2"
                :value="selected.rareness"
                :length="selected.rareness"
                size="10"
                readonly
                dense
              ></v-rating>
              <v-list-item-title class="headline mb-4">
                {{ selected.name }}
              </v-list-item-title>
              <v-list-item-subtitle
                v-for="(tag, index) in resolveTagsFromCode(selected.tag)"
                :key="index"
              >
                {{ tag }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-avatar size="120">
              <v-img :src="selected.profile"></v-img>
            </v-list-item-avatar>
          </v-list-item>
          <v-card-actions class="mb-3">
            <v-btn
              outlined
              rounded
              text
              link
              :href="'http://prts.wiki/w/' + selected.name"
            >
              Wiki页面
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {
  MatchedOperators,
  OperatorInfo,
  resolveTagsFromCode
} from "../OperatorInfo";
import { Component, Prop, Vue } from "vue-property-decorator";
import _ from "lodash";

@Component
export default class OperatorDisplay extends Vue {
  @Prop()
  matchedOperators!: MatchedOperators[];
  @Prop({ default: false })
  sortByMaxRareness!: boolean;

  selected: OperatorInfo | null = null;

  showDialog = false;

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
}
</script>
