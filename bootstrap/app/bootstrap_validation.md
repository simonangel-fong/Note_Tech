# Bootstrap组件 - validation表单验证

[返回Boostrap首页](../bootstrap_index.md)

## 目录

- [Bootstrap组件 - validation表单验证](#bootstrap组件---validation表单验证)
  - [目录](#目录)
  - [表单验证](#表单验证)

***

## 表单验证

- html代码
  - `<form novalidate></form>`：声明表单存在验证
  - `class="invalid-feedback"`：当验证失败时显示

```html
<form class="needs-validation" novalidate>
  <!-- Input -->
  <input type="text" class="form-control" id="input" required/>
  <div class="invalid-feedback">
    message for invalid
  </div>

  <!-- Textarea -->
  <textarea class="form-control" id="textarea" required></textarea>
  <div class="invalid-feedback">
    message for invalid
  </div>

  <!-- Select -->
  <select class="form-select" id="select" required>
    <option selected disabled value="">Choose...</option>
    <option>...</option>
  </select>
  <div class="invalid-feedback">
    message for invalid
  </div>

  <!-- Checkbox -->
  <div class="form-check">
    <input class="form-check-input" type="checkbox" value="" id="checkbox" required>
    <label class="form-check-label" for="checkbox">
      tips for checkbox
    </label>
    <div class="invalid-feedback">
      message for invalid
    </div>
  </div>

  <!-- file -->
  <input type="file" class="form-control" id="file" required>
  <div class="invalid-feedback">
    message for invalid
  </div>

</form>

```

- Javascript代码: 提交时进行验证

```Javascript
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

```

- 如果要重置表单，则只需移除class`was-validated`
  
```Javascript
$("#form").removeClass("was-validated");
```

[回到目录](#目录)

***

[返回Bootstrap首页](../bootstrap_index.md)
