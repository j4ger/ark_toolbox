// Modified from https://github.com/SeregPie/lodash.combinations

import _ from "lodash";

function recur<T>(array: T[], n: number): T[][] {
  if (--n < 0) {
    return [[]];
  }
  const combinations: T[][] = [];
  array = array.slice();
  while (array.length - n) {
    const value = array.shift();
    recur(array, n).forEach(combination => {
      if (value !== undefined) {
        combination.unshift(value);
        combinations.push(combination);
      }
    });
  }
  return combinations;
}

export default function lodashCombinations<T>(
  collection: _.List<T>,
  n: number
) {
  const array = _.values(collection);
  if (array.length < n) {
    return [];
  }
  return recur(array, n);
}
