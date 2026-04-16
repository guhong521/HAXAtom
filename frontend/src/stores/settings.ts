import { ref, watch } from "vue";

// 语言设置
export const currentLanguage = ref(localStorage.getItem("language") || "zh-CN");

export const setLanguage = (lang: string) => {
  currentLanguage.value = lang;
};

watch(currentLanguage, (newVal) => {
  localStorage.setItem("language", newVal);
});

// 深色模式设置
export const isDarkMode = ref(localStorage.getItem("darkMode") === "true");

export const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
};

watch(isDarkMode, (newVal) => {
  localStorage.setItem("darkMode", String(newVal));
  if (newVal) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
  // 切换模式时重新计算文字颜色
  updateBgOpacity(bgOpacity.value);
});

// 背景透明度设置 (0-1, 默认0.3)
export const bgOpacity = ref(Number(localStorage.getItem("bgOpacity")) || 0.3);

export const setBgOpacity = (opacity: number) => {
  bgOpacity.value = opacity;
};

watch(bgOpacity, (newVal) => {
  localStorage.setItem("bgOpacity", String(newVal));
  updateBgOpacity(newVal);
});

const updateBgOpacity = (opacity: number) => {
  document.documentElement.style.setProperty("--bg-opacity", String(opacity));
  // 不再通过内联样式覆盖文字颜色
  // 文字颜色由 theme.css 中的 CSS 变量自然控制
};

// 初始化
export const initSettings = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark");
  }
  updateBgOpacity(bgOpacity.value);
};
