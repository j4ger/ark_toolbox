<template>
  <v-container>
    <v-slide-y-transition>
      <v-col cols="12" sm="8" offset-sm="2" v-show="showTags">
        <v-row v-for="(group, name, index) in tags" :key="index" cols="12">
          <v-sheet class="my-2">
            <h3 class="medium-text-weight text-left">{{ name }}</h3>
            <v-chip-group
              v-model="selected"
              multiple
              column
              justify="space-around"
            >
              <v-chip
                v-for="(value, tag) in group"
                :key="value"
                :value="value"
                filter
                >{{ tag }}</v-chip
              >
            </v-chip-group>
            <v-divider></v-divider>
          </v-sheet>
        </v-row>
      </v-col>
    </v-slide-y-transition>
    <v-col cols="12" sm="8" offset-sm="2">
      <v-row
        v-for="Operator in OperatorInfos"
        :key="Operator.rareness"
        class="d-sm-flex flex-sm-column"
      >
        <operator-display :operator-info="Operator"></operator-display>
      </v-row>
    </v-col>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import OperatorInfo from "../OperatorInfo";
import OperatorDisplay from "./OperatorDisplay.vue";

@Component({ components: { OperatorDisplay } })
export default class Recruit extends Vue {
  @Prop({ default: true })
  showTags!: boolean;
  selected = [1];
  tags = {
    获得途径: { 公招可见: 1 },
    职业: {
      先锋: 2,
      近卫: 4,
      狙击: 8,
      重装: 16,
      医疗: 32,
      辅助: 64,
      术师: 128,
      特种: 256
    },
    部署位: { 近战位: 512, 远程位: 1024 },
    性别: { 男性干员: 2048, 女性干员: 4096, 断罪性干员: 8192 },
    一般标签: {
      治疗: 16384,
      支援: 32768,
      输出: 65536,
      群攻: 131072,
      减速: 262144,
      生存: 524288,
      防护: 1048576,
      削弱: 2097152,
      位移: 4194304,
      控场: 8388608,
      爆发: 16777216,
      召唤: 33554432,
      快速复活: 67108864,
      费用回复: 134217728,
      支援机械: 268435456,
      新手: 536870912
    }
  };
  OperatorInfos: OperatorInfo[] = [
    {
      profile: "https://i.loli.net/2021/01/23/cLBC8qba9uAtkVG.png",
      name: "\u84dd\u6bd2",
      codename: "Blue Poison",
      rareness: 5,
      tag: 70665
    }
  ];
  resetTags(): void {
    this.selected = [1];
  }
  created(): void {
    this.$emit("reset-tags-handler", this.resetTags);
  }
}
</script>
