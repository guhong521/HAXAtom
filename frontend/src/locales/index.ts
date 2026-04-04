import { computed } from "vue";
import { currentLanguage } from "../stores/settings";
import zhCN from "./zh-CN";
import enUS from "./en-US";
import zhTW from "./zh-TW";
import jaJP from "./ja-JP";
import koKR from "./ko-KR";
import ruRU from "./ru-RU";

const messages = {
  "zh-CN": zhCN,
  en: enUS,
  "zh-TW": zhTW,
  ja: jaJP,
  ko: koKR,
  ru: ruRU,
};

// 翻译函数
export const t = (key: string): string => {
  const keys = key.split(".");
  const currentMessages =
    messages[currentLanguage.value as keyof typeof messages] || zhCN;

  let result: any = currentMessages;
  for (const k of keys) {
    if (result && typeof result === "object" && k in result) {
      result = result[k];
    } else {
      return key; // 找不到翻译，返回原 key
    }
  }

  return typeof result === "string" ? result : key;
};

// 响应式翻译（用于模板中）
export const useI18n = () => {
  return {
    t: computed(() => t),
  };
};
