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
  // 浅色模式下，根据透明度调整文字颜色
  // 透明度越低（背景越透明），文字需要越亮（白色）才能在背景图片上可见
  if (!isDarkMode.value) {
    // opacity 0-0.3: 背景透明，背景图片明显，需要白色文字
    if (opacity <= 0.3) {
      document.documentElement.style.setProperty("--text-primary", "#ffffff");
      document.documentElement.style.setProperty("--text-secondary", "#e0e0e0");
      document.documentElement.style.setProperty("--text-tertiary", "#c0c0c0");
    }
    // opacity 0.3-1: 背景较实，使用黑色文字
    else {
      document.documentElement.style.setProperty("--text-primary", "#303133");
      document.documentElement.style.setProperty("--text-secondary", "#606266");
      document.documentElement.style.setProperty("--text-tertiary", "#909399");
    }
  } else {
    // 深色模式下恢复默认文字颜色
    document.documentElement.style.setProperty("--text-primary", "#e0e0e0");
    document.documentElement.style.setProperty("--text-secondary", "#b0b0b0");
    document.documentElement.style.setProperty("--text-tertiary", "#808080");
  }
};

// 初始化
export const initSettings = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark");
  }
  updateBgOpacity(bgOpacity.value);
};
