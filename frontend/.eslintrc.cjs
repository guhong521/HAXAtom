/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/eslint-config-typescript",
  ],
  parserOptions: {
    ecmaVersion: "latest",
  },
  rules: {
    // 允许 v-model 带参数（Vue 3 多个 v-model 语法）
    "vue/no-v-model-argument": "off",
  },
};
