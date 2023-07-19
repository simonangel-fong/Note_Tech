# Javascript - Modules

[Back](../index.md)

- [Javascript - Modules](#javascript---modules)
  - [Modules](#modules)
  - [Export](#export)
    - [Named Exports](#named-exports)
    - [Default Exports](#default-exports)

---

## Modules

- `Modules`

  - allow to break up code into separate **files**, making it easier to maintain a code-base.
  - imported from **external** files with the import statement.
  - rely on `type="module"` in the `<script>` tag.

- `Modules` only work with the `HTTP(s)` protocol.

```js
<script type="module">import message from "./message.js";</script>
```

---

## Export

- Modules with `functions` or `variables` can be stored in any **external file**.

- There are two types of exports:

  - `Named Exports`
  - `Default Exports`.

---

### Named Exports

- **person.js**

```js
// person.js
const name = "Jesse";
const age = 40;

export { name, age };
```

- **html file**

```html
<script type="module">
  import { name, age } from "/person.js";
  console.log(name); //"Jesse"
</script>
```

---

### Default Exports

- **message.js**

```js
const message = () => {
  const name = "Jesse";
  const age = 40;
  return name + " is " + age + "years old.";
};

export default message;
```

- **html file**

```html
<script type="module">
  import message from "./message.js";
  console.log(message); // Jesse is 40 years old.
</script>
```

---

[Top](#javascript---modules)
