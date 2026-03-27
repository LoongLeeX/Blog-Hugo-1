---
blog_cover: null
categories: null
date: 2024-01-18
tags:
- Web分析
- React.js
- Vue.js
title: 如何分析一个网页使用了Recat.js 还是 Vue.js
---

## 如何分析一个网页使用了React.js还是Vue.js

### 1. 查看页面源码
打开浏览器，右键点击页面并选择“查看页面源码”（View Page Source）或按 `Ctrl + U`。在源码中查找以下关键字：

- **React.js**:
  - 查找`react`或`ReactDOM`关键字。
  - 检查是否有以 `jsx` 为扩展名的文件。
  
- **Vue.js**:
  - 查找`vue`关键字。
  - 检查是否有以 `vue` 为扩展名的文件。

### 2. 使用浏览器开发者工具
按 `F12` 或右键点击页面并选择“检查”（Inspect），打开开发者工具。

- **React.js**:
  - 在“元素”标签（Elements tab）中，查找是否有包含`data-reactroot`属性的HTML元素。
  - 在“控制台”标签（Console tab）中输入 `React` 或 `ReactDOM`，看是否返回一个对象而不是 `undefined`。
  
- **Vue.js**:
  - 在“元素”标签中，查找是否有包含`data-v-`属性的HTML元素。
  - 在“控制台”标签中输入 `Vue`，看是否返回一个对象而不是 `undefined`。

### 3. 使用浏览器扩展
一些浏览器扩展可以帮助你识别网页是否使用了特定的框架：

- **React Developer Tools**: 可以在页面上显示React组件结构。
- **Vue.js devtools**: 可以在页面上显示Vue组件结构。

### 4. 使用在线工具
一些在线工具可以分析网页并告诉你其使用的技术栈，例如：

- [Wappalyzer](https://www.wappalyzer.com/): 可以识别网页使用的各种技术，包括React.js和Vue.js。
- [BuiltWith](https://builtwith.com/): 提供关于网页技术栈的详细信息。

通过上述方法，你可以很容易地判断一个网页是使用了React.js还是Vue.js。


![](/bi/logo_demo_1.png)