<template>
  <v-hover>
    <template v-slot:default="{ hover }">
      <v-card
        outlined
        class="mx-auto rounded-lg transition-swing"
        :class="`elevation-${hover ? 10 : 4}`"
        ><v-list-item three-line>
          <v-list-item-avatar size="75"
            ><v-img :src="OperatorInfo.profile"></v-img>
          </v-list-item-avatar>
          <v-list-item-content>
            <div class="overline mb-4">
              {{ OperatorInfo.codename }}
            </div>
            <v-list-item-title class="headline mb-1">
              {{ OperatorInfo.name }}
            </v-list-item-title>
            <v-list-item-subtitle>{{ OperatorInfo.tag }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </template>
  </v-hover>
</template>
//TODO: 星级 tag解析 获取json
<script lang="ts">
import OperatorInfo from "@/OperatorInfo";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class OperatorDisplay extends Vue {
  @Prop()
  OperatorInfo!: OperatorInfo;
}
</script>
