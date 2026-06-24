# 第 3 周：映射类型与条件类型

> 代码练习见 [test.ts](./test.ts)，在 IDE 中 hover 类型名可查看推导结果。

---

## 一、整体脉络

| 概念 | 作用 |
|------|------|
| **映射类型** | 遍历 `T` 的每个 key，逐个改造属性 |
| **条件类型** | `A extends B ? X : Y`，按类型关系做分支 |
| **Key Remapping (`as`)** | 遍历时可以改 key，甚至"删掉"某些 key |
| **分布式条件类型** | 联合类型进入 `extends` 时会拆开逐个判断 |

---

## 二、映射类型基础

### 必须自己实现的工具类型

```typescript
type MyPartial<T> = {
  [K in keyof T]?: T[K]
}

type MyReadonly<T> = {
  readonly [K in keyof T]: T[K]
}

type Nullable<T> = {
  [K in keyof T]: T[K] | null
}
```

### `[K in keyof T]` 在遍历什么？

- `keyof T`：取出 `T` 所有属性名的**联合类型**
  - 例：`User` → `"id" | "name" | "phone" | "age"`
- `[K in ...]`：对联合里的**每一个** key 生成一个属性
- `T[K]`：**索引访问类型**，取该 key 对应的值类型

伪代码理解：

```typescript
for (K of keyof T) {
  新类型[K] = T[K] 的某种改造
}
```

---

## 三、DeepPartial：映射 + 条件 + 递归

```typescript
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object
    ? DeepPartial<T[K]>
    : T[K]
}
```

### 执行过程示例

```typescript
interface Config {
  server: { host: string; port: number }
  debug: boolean
}
```

| 属性 | 判断 | 结果 |
|------|------|------|
| `server` | `{ host, port } extends object` → 是 | 递归 `DeepPartial<...>` |
| `host` / `port` | 内层遍历，变可选 | `host?: string` |
| `debug` | `boolean extends object` → 否 | 保持 `boolean`，外层加 `?` |

最终：

```typescript
{
  server?: { host?: string; port?: number }
  debug?: boolean
}
```

---

## 四、PickByType：按值类型筛选属性

```typescript
type PickByType<T, ValueType> = {
  [K in keyof T as T[K] extends ValueType ? K : never]: T[K]
}
```

### 示例

```typescript
interface User {
  id: number
  name: string
  phone: string
  age: number
}

type StringFields = PickByType<User, string>
// → { name: string; phone: string }
```

### 走一遍推导

| K | `T[K] extends string?` | 新 key |
|---|------------------------|--------|
| id | 否 | `never`（丢弃） |
| name | 是 | `"name"` |
| phone | 是 | `"phone"` |
| age | 否 | `never`（丢弃） |

---

## 五、RequiredByKeys：指定 key 变必填

```typescript
type RequiredByKeys<T, K extends keyof T> = {
  [P in keyof T]: P extends K ? NonNullable<T[P]> : T[P]
}
```

### 示例

```typescript
interface User {
  id?: number
  name?: string
  phone?: string
  age?: number
}

type Result = RequiredByKeys<User, 'name' | 'phone'>
// → { id?: number; name: string; phone: string; age?: number }
```

- `P extends K`：当前属性是否在"要变必填"的列表里
- `NonNullable<T[P]>`：去掉 `undefined`（可选属性本质是 `T[P] | undefined`）

---

## 六、分布式条件类型

### 什么时候会"分布"？

泛型参数是**裸类型参数**（没有被 `[]` 包起来）且是**联合类型**时：

```typescript
type IsString<T> = T extends string ? true : false

type A = IsString<string | number>
// 等价于 IsString<string> | IsString<number>
// = true | false
```

### 什么时候不会分布？

用 `[T]` 包裹，阻止分布：

```typescript
type NoDistribute<T> = [T] extends [string] ? true : false

type B = NoDistribute<string | number>  // false（整体判断，不拆开）
```

### 和 PickByType 的关系

`PickByType` 里 `T[K] extends ValueType` 的 `T[K]` **不是裸泛型 `T`**，所以不会发生分布式——每个 key 单独判断，这正是我们想要的。

---

## 七、验收自测（能解释才算会）

1. **`[K in keyof T]` 在遍历什么？**
   → 遍历 `T` 所有属性名的联合类型；每个 `K` 生成一个属性，值为 `T[K]` 的改造结果。

2. **`as` 为什么能重新映射属性？**
   → `as` 可以改写映射产生的 key；配合条件类型，实现筛选、重命名或过滤。

3. **为什么 `never` 可以删除属性？**
   → 映射类型中 key 为 `never` 的项不会出现在结果类型里。

4. **条件类型什么时候会发生分布？**
   → 当条件类型左侧是**裸类型参数**且该参数为**联合类型**时，会拆成多个条件类型再取联合；用 `[T]` 等方式可阻止分布。

---

## 八、练习建议

1. 打开 `test.ts`，hover `_StringFields`、`_DeepConfig` 等类型，观察推导
2. 遮住文件顶部的实现，在「练习区」自己写一遍
3. 对照验收自测四题，用自己的话讲一遍
