## 核心类型
    - any unknown never void 
    - declare type interface as
    - 类型推动 & 类型断言
    - 泛型 T
        - 类型参数推导（infer）
        - 工具类型，类型编程
            - partial<T>   所有属性变为可选
            - Required<T>  所有属性变为必填
            - Readonly<T>  所有属性变为只读
            - Pick<T,K>    选取T中指定属性K
            - Omit<T,K>    排除T中指定属性K
            - Record<K,T>  创建键为K类型，值为T类型的对象	
            - Exclude<T,U> 从联合类型T中排除U类型
            - Extract<T,U> 从联合类型T中提取U类型
        - 类型守卫，类型收窄
## 面向对象 & 设计
    - 类与继承
        - 修饰符
            - public 公开访问
            - protected 仅类及子类可访问
            - private 仅类内部访问
            - readonly 初始化后不可修改
        - 抽象类 & 抽象方法
            - abstract
        - 静态成员 & 静态块
            - static
        - 接口（interface） vs 类型别名(type)
            - 需要声明合并或implements时用interface
            - 需要联合类型时、元组或映射类型时用type 其他场景根据团队规范保持一致即可
    - 装饰器
        - 增强类/方法/属性的行为

## 模块与工程化
    - ES Module， CommonJS
    - tsconfig
        - 常用 tsconfig 配置项：
            - target              // 编译后JS的目标版本
            - module              // 生成的模块系统类型
            - moduleResolution    // 模块解析方式
            - strict              // 启用所有严格类型检查
            - noImplicitAny       // 禁止隐式any类型
            - strictNullChecks    // 严格的null检查
            - declaration         // 生成声明文件（.d.ts）
            - sourceMap           // 生成sourceMap映射
            - outDir              // 输出目录
            - esModuleInterop     // 兼容CommonJS与ESModule
            - skipLibCheck        // 跳过库文件类型检查

 ## 工程实践与高级特性
    - 声明文件（.d.ts)
    - declare, declare global, declare module
    - 异步与并发
        - Promise<T>
        - async/await 类型推断
## 实用技巧
    - keyof 与索引访问类型（T[K]）
    - this 类型与链式调用
    - satisfies 操作符 as
    - const 泛型参数 ` as const `
