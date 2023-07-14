# Bootstrap - Modal

[Back](../index.md)

- [Bootstrap - Modal](#bootstrap---modal)
  - [基本组件和触发: HTML 代码](#基本组件和触发-html-代码)
  - [触发事件](#触发事件)
    - [触发事件 - Javascript](#触发事件---javascript)
    - [触发事件 - jQuery](#触发事件---jquery)
  - [定义事件](#定义事件)
    - [定义事件 - JavaScript](#定义事件---javascript)
    - [定义事件 - jQuery](#定义事件---jquery)

---

## 基本组件和触发: HTML 代码

- 使用基本 html 代码即可触发 modal

```html
<!-- Button trigger modal -->
<button
  type="button"
  class="btn btn-primary"
  data-bs-toggle="modal"
  data-bs-target="#exampleModal"
>
  Launch demo modal
</button>

<!-- Modal -->
<div id="exampleModal" class="modal" tabindex="-1">
  <div class="modal-dialog">
    <!-- content 用于摆放内容 -->
    <div class="modal-content">
      <!-- header 通常用于显示标题 -->
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>

      <!-- body 用于显示主要内容 -->
      <div class="modal-body">
        <p>Modal body text goes here.</p>
      </div>

      <!-- footer 用于显示按钮 -->
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Close
        </button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
```

> **代码说明：**
>
> - 效果：按钮触发 modal
> - 按钮属性
>
> 1.  `data-bs-toggle="modal"`: 设定切换的类型是 modal。设定后，bootstrap 会触发 modal 的 toggle 方法
> 2.  `data-bs-target="#exampleModal"`: 设定切换的对象。
>
> - Modal
>
> 1.  `class="modal"`:引用 bootstrap 的 modal 的 css;
> 2.  `tabindex`: 设置 tab 的自序，对显示无影响；
> 3.  `data-bs-dismiss="modal"`: 设定取消的类型是 modal。通常用于 modal 中的'取消'按钮，用于隐藏 modal

- modal 组件常用属性：
  | 属性 | 默认值 | 效果 | 说明 |
  | ---- | ---- | ---- | ---- |
  | `data-bs-backdrop` | true | 设置背景 | `true`: 显示半透明的背景; `false`: 不显示背景; `static`: 背景是静止,点击背景不会关闭. |

[回到目录](#目录)

---

## 触发事件

### 触发事件 - Javascript

| 代码        | 事件 | 说明 |
| ----------- | ---- | ---- |
| `.toggle()` | 切换 |      |
| `.show()`   | 显示 |      |
| `.hide()`   | 隐藏 |      |

- html 代码

```html
<!-- Button trigger modal -->
<button
  id="btn"
  type="button"
  class="btn btn-primary"
  data-bs-toggle="modal"
  data-bs-target="#exampleModal"
>
  Launch demo modal
</button>

<!-- Modal -->
<div id="exampleModal" class="modal" tabindex="-1">
  <div class="modal-dialog">
    <!-- content 用于摆放内容 -->
    <div class="modal-content">
      <!-- header 通常用于显示标题 -->
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>

      <!-- body 用于显示主要内容 -->
      <div class="modal-body">
        <p>Modal body text goes here.</p>
      </div>

      <!-- footer 用于显示按钮 -->
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Close
        </button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
```

- Javascript 代码(非 jQuery)

```javascript
//JavaScript代码(非jQuery)：
var button = document.getElementById("btn");
var modal = new bootstrap.Modal(document.getElementById("modal"), {});

button.addEventListener("click", function () {
  modal.toggle(); //切换modal
});
```

> **代码说明：**
>
> 1. 以上代码是纯 js 代码，不引用 jQuery 库;
> 2. `new bootstrap.Modal()`是创建新的 modal 实例。
>
> - 包含两个参数：
>   - HTML DOM, 引用的 html 对象;
>   - 字典类型, 新建对象的参数,如`{keyboard: false}`.
>
> 3. `.addEventListener("click",function(){}`:添加事件到按钮;
> 4. `modal.toggle()`: 触发 modal 切换事件.

> **注意:**
>
> - js 下必须使用`new bootstrap.Modal()`创建 modal 实例, 不能直接引用：
>
> ```javascript
> var modal = document.getElementById("modal");
> modal.toggle(); //或报错：Uncaught TypeError: modal.toggle is not a function
> ```
>
> - `.toggle()`是 js 代码有效. 如果是 jquery,该方法无效,需要使用`modal("toggle")`

[回到目录](#目录)

---

### 触发事件 - jQuery

| 代码               | 事件 | 说明 |
| ------------------ | ---- | ---- |
| `.modal("toggle")` | 切换 |      |
| `.modal("show")`   | 显示 |      |
| `.modal("hide")`   | 隐藏 |      |

- Javascript 代码(jQuery)

```javascript
//JavaScript代码(jQuery)：
$("#btn").click(function () {
  $("#modal").modal("toggle");
});
```

> 代码说明：
>
> 1. 以上引用 jQuery 库;
> 2. `.modal('toggle')`触发 toggle 事件.可以直接使用 jquery 捕获现有的 html DOM 对象

[回到目录](#目录)

---

## 定义事件

### 定义事件 - JavaScript

| 代码              | 事件 | 说明 |
| ----------------- | ---- | ---- |
| `"show.bs.modal"` | 显示 |      |
| `"hide.bs.modal"` | 隐藏 |      |

- html 代码:

```html
<!-- Button trigger modal -->
<button
  id="btn"
  type="button"
  class="btn btn-primary"
  data-bs-toggle="modal"
  data-bs-target="#modal"
  data-bs-whatever="@mdo"
>
  Launch demo modal
</button>

<!-- Modal -->
<div id="modal" class="modal" tabindex="-1">
  <div class="modal-dialog">
    <!-- content 用于摆放内容 -->
    <div class="modal-content">
      <!-- header 通常用于显示标题 -->
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>

      <!-- body 用于显示主要内容 -->
      <div class="modal-body">
        <p>Modal body text goes here.</p>
      </div>

      <!-- footer 用于显示按钮 -->
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Close
        </button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
```

- JavaScript

```javascript
var button = document.getElementById("btn");
var modal = document.getElementById("modal");

var myModal = new bootstrap.Modal(modal, {});

button.addEventListener("click", function () {
  myModal.toggle(); //切换modal
});

// 绑定事件到modal
modal.addEventListener("show.bs.modal", function (event) {
  var btn = event.relatedTarget;

  // Extract info from data-bs-* attributes
  var data = btn.getAttribute("data-bs-whatever");
  alert(data);
});
```

> **代码说明:**
>
> 1. html 代码中的`data-bs-**`属性用于存放待传输的数据;
> 2. `.addEventListener('show.bs.modal', function(event){})`: 设定 model 显示时执行的代码;
> 3. `event.relatedTarget`: 用来进行引用触发的对象。注意:该方法仅适用于使用 html`data-bs-toggle="modal"`属性触发的切换; 如果是使用 js`.toggle()`触发的，将返回`undefined`;
> 4. `.getAttribute()`: 用来获取目标元素的属性值.

[回到目录](#目录)

---

### 定义事件 - jQuery

- html 代码同上

- js 代码(jQuery)

```javascript
$("#btn").click(function () {
  $("#modal").modal("toggle");
});

$("#modal").on("show.bs.modal", function (event) {
  var data = $("#btn").attr("data-bs-whatever");
  alert(data);
});
```

> **代码说明：**
>
> 1. `.on("show.bs.modal", function (event) {}`: 使用`on`方法定义事件
> 2. `.attr("")`: 直接使用`attr`方法获取属性的值；注意：也可以使用`event.relatedTarget`,但不能使用 jQuery 语法。

---

[TOP](#bootstrap---modal)
