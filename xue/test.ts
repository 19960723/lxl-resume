/**
 * 第 3 周：映射类型与条件类型
 *
 * 学习建议：
 * 1. 先读 test.md 里的概念说明
 * 2. 在本文件中 hover 类型名，观察推导结果
 * 3. 把「练习区」的实现遮住，自己写一遍再对照
 */

// ============================================================
// 一、映射类型基础
// ============================================================

/**
 * [K in keyof T] 在遍历什么？
 * - keyof T：取出 T 所有属性名的联合类型，如 "id" | "name"
 * - [K in ...]：对联合类型中的每一个 K，生成一个属性
 * - T[K]：索引访问类型，取该 key 对应的值类型
 *
 * 伪代码：for (K of keyof T) { 新类型[K] = 改造(T[K]) }
 */

/** 所有属性变可选 */
type MyPartial<T> = {
  [K in keyof T]?: T[K]
}

/** 所有属性变只读 */
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K]
}

/** 所有属性允许 null */
type Nullable<T> = {
  [K in keyof T]: T[K] | null
}

// ============================================================
// 二、DeepPartial：映射 + 条件类型 + 递归
// ============================================================

/**
 * 条件类型：A extends B ? X : Y
 * 读作：如果 A 能赋值给 B，结果是 X，否则是 Y
 *
 * DeepPartial 思路：
 * - 遍历每个属性 K
 * - 若 T[K] 是 object，则递归 DeepPartial
 * - 否则保持原类型
 * - 外层加 ? 表示可选
 */
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K]
}

// ============================================================
// 三、PickByType：Key Remapping（as 重映射）
// ============================================================

/**
 * [K in keyof T as 新Key] 可以改写映射产生的 key
 *
 * T[K] extends ValueType ? K : never 的含义：
 * - 值类型匹配 → 保留 key
 * - 不匹配 → never → 该属性不会出现在结果中（被"删除"）
 */
type PickByType<T, ValueType> = {
  [K in keyof T as T[K] extends ValueType ? K : never]: T[K]
}

// ============================================================
// 四、RequiredByKeys：指定 key 变必填
// ============================================================

/**
 * 思路：遍历每个属性 P
 * - 若 P 在指定列表 K 中 → 用 NonNullable 去掉 undefined
 * - 否则保持原样
 *
 * 另一种写法（组合工具类型）：
 * type RequiredByKeys<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>
 */
type RequiredByKeys<T, K extends keyof T> = {
  [P in keyof T]: P extends K ? NonNullable<T[P]> : T[P]
}

// ============================================================
// 五、分布式条件类型
// ============================================================

/** 裸类型参数 + 联合类型 → 会分布（拆开逐个判断） */
type IsString<T> = T extends string ? true : false
type DistExample = IsString<string | number> // true | false

/** 用 [T] 包裹 → 阻止分布，整体判断 */
type IsStringNoDist<T> = [T] extends [string] ? true : false
type NoDistExample = IsStringNoDist<string | number> // false

// ============================================================
// 测试用例 — hover 查看推导结果
// ============================================================

interface User {
  id?: number
  name?: string
  phone?: string
  age?: number
}

interface Config {
  server: {
    host: string
    port: number
  }
  debug: boolean
}

// --- 映射类型基础 ---
type _PartialUser = MyPartial<User>
// { id?: number; name?: string; phone?: string; age?: number }

type _ReadonlyUser = MyReadonly<User>
// 所有属性 readonly

type _NullableUser = Nullable<User>
// 每个属性类型 | null

// --- DeepPartial ---
type _DeepConfig = DeepPartial<Config>
// { server?: { host?: string; port?: number }; debug?: boolean }

// --- PickByType ---
type _StringFields = PickByType<User, string>
// { name: string; phone: string }

type _NumberFields = PickByType<User, number>
// { id: number; age: number }

// --- RequiredByKeys ---
type _RequiredNamePhone = RequiredByKeys<User, 'name' | 'phone'>
// { id?: number; name: string; phone: string; age?: number }

// ============================================================
// 练习区 — 遮住上方答案，自己实现后再对照
// ============================================================

// type MyPartial<T> = ???
// type DeepPartial<T> = ???
// type PickByType<T, ValueType> = ???
// type RequiredByKeys<T, K extends keyof T> = ???
