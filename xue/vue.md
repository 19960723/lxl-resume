# vue

## 组建传值交互
- 父子简单数据传递
- 兄弟s
- 表达双向绑定
- 跨层级组件共享
- 全局在状态
- 非父子组件

## 生命周期
- 

## 自定义指令
- 定义指定对象并注册，通过生命周期钩子操作dom (自动聚焦，权限控制， 输入限制)

## ref & reactive
- ref: 
    - string number boolean object
    - .value去访问  模版中无需.value
    - 响应原理: 内部对象调用reactive.  解构会丢失响应性，用 torefs


- reactive: 
    - array
    - 直接访问属性
    - 响应原理：基于 Proxy 的深层代理. 解构会丢失响应性，用 torefs

## watch watchEffect computed
- computed 缓存机制， 依赖向变动 （减少重复计算开销）
- watch  指定监听原
- watchEffect 监听方法内的所有响应依赖 （依赖向不明确， 多个依赖） 慎重使用
及时清理副作用 onUnmounted,避免内存泄露

## keepAlive 
    组件缓存
## defineAsyncComponent  异步组件
    按需加载，性能优化  动态加载，提升首屏速度

## 新组件&API
    组件
        - Fragment, Teleport, Suspense
        - eventbus => mitt, vue.extend => defineComponent

## 性能优化
    响应系统：proxy => defineProperty
    编译优化
    渲染： v-once v-memo v-show v-if shallowRef markRaw defineAsyncComponent
    组件： 细粒度拆分， 异步组件 懒加载
    路由： 代码分割， 懒加载
    预加载：资源 <link />
    列表渲染： v-for key, v-if v-for computed，虚拟滚动, 避免响应嵌套，减少内容复杂嵌套
    事件处理： 防抖/节流
    架构： 
        - 服务端渲染（SSR）nuxt.js  首屏加载 & SEO
        - 静态站点生成（SSG） vitePress/vuePress 静态页面，内容型网站
        - CDN缓存策略 
    工具链：
        - vite
        - 性能分析工具： chrome devtools & Performance  Lighthouse
    Web Worker

# vueRouter
    路由守卫，懒加载，动态路由（addRoute）， 滚动行为控制


# vuex
    state getter mutation action modules
    持久化

# Pinia

# Nuxt.js

# 安全
 xss csrf cors