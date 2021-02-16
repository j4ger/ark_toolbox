import { invert, sortBy, without } from "lodash";

export interface OperatorInfo {
  profile: string;
  name: string;
  codename: string;
  rareness: number;
  tag: number;
}

export interface TagsSelected {
  获得途径?: number[];
  职业?: number[];
  部署位?: number[];
  性别?: number[];
  一般标签?: number[];
}

export interface MatchedOperators {
  tags: string[];
  operators: OperatorInfo[];
  maxRareness: number;
  minRareness: number;
  robot: boolean;
}

export const tags = {
  公招可见: 1,
  先锋: 2,
  近卫: 4,
  狙击: 8,
  重装: 16,
  医疗: 32,
  辅助: 64,
  术师: 128,
  特种: 256,
  近战位: 512,
  远程位: 1024,
  男性干员: 2048,
  女性干员: 4096,
  断罪性干员: 8192,
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
  新手: 536870912,
  资深干员: 1073741824,
  高级资深干员: 2147483648
};

export const tagsGrouped = {
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
    新手: 536870912,
    资深干员: 1073741824,
    高级资深干员: 2147483648
  }
};

export function resolveTagsFromCode(code: number): string[] {
  const separatedTagCodes: number[] = [];
  let i = 0;
  while (Math.floor(code) != 0) {
    if (code % 2 == 1) {
      separatedTagCodes.push(Math.pow(2, i));
    }
    i++;
    code = Math.floor(code / 2);
  }
  return separatedTagCodes.map(eachTag => invert(tags)[eachTag]);
}

export function getMatchedOperators(
  operators: OperatorInfo[],
  tags: number
): MatchedOperators | null {
  const matches: OperatorInfo[] = [];
  let maxRareness = 1;
  let minRareness = 7;
  let robot = false;
  operators.forEach(each => {
    if ((each.tag & tags) >>> 0 == tags) {
      matches.push(each);
      if (each.rareness == 1) {
        robot = true;
      } else {
        if (each.rareness > maxRareness) {
          maxRareness = each.rareness;
        }
        if (each.rareness < minRareness) {
          minRareness = each.rareness;
        }
      }
    }
  });
  if (robot && minRareness == 7) {
    minRareness = 1;
  }
  return matches.length == 0
    ? null
    : {
        tags: without(resolveTagsFromCode(tags), "公招可见"),
        operators: sortBy(matches, operator => 7 - operator.rareness),
        maxRareness,
        minRareness,
        robot
      };
}
