# Bootstrap - Box Model

[Back](./index.md)

- [Bootstrap - Box Model](#bootstrap---box-model)
  - [Backgroud \& Opacity](#backgroud--opacity)
  - [Width \& Height](#width--height)
  - [Padding \& Margin](#padding--margin)
  - [Border](#border)
  - [Border Radius](#border-radius)
  - [Shadow](#shadow)

---

## Backgroud & Opacity

| Class             | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `bg-{color}`      | background colors                                    |
| `text-bg-{color}` | background colors,text color is handle automatically |
| `opacity-{value}` | Set the opacity of an element                        |

- color:
  - `primary`, `success`, `info`, `warning`, `danger`, `secondary`, `dark` and `light`.

## Width & Height

| Class           | Description                                           |
| --------------- | ----------------------------------------------------- |
| `w-{size}`      | the **width** of an element                           |
| `mw-{size}`     | the max width of an element                           |
| `vw-{size}`     | the width of an element, relative to the viewpor      |
| `min-vw-{size}` | the min width of an element, relative to the viewpor  |
| `h-{size}`      | the **height** of an element                          |
| `mh-{size}`     | the max height of an element                          |
| `vh-{size}`     | the height of an element, relative to the viewpor     |
| `min-vh-{size}` | the min height of an element, relative to the viewpor |

- size: size **relative to the parent**
  - `25`: 25% width
  - `50`:50% width
  - `75`:75% width
  - `100`: 100% width
  - `auto`: auto width

---

## Padding & Margin

| Class                         | Description                                 |
| ----------------------------- | ------------------------------------------- |
| `p-{size}`                    | set all side **padding** with size          |
| `p{side}-{size}`              | set padding with side and size              |
| `p{side}-{breakpoint}-{size}` | set padding with side, breakpoint, and size |
| `m-{size}`                    | set all side **margin** with size           |
| `m{side}-{size}`              | set margin with side and size               |
| `m{side}-{breakpoint}-{size}` | set margin with side, breakpoint, and size  |

- side:

  - `t`: top
  - `b`: bottom
  - `s`: start(left)
  - `e`: end(right)
  - `x`: left and right
  - `y`: top and bottom

- breakpoint:

  - `sm`, `md`, `lg`, `xl` and `xxl`

- size:
  - `0`-`5`
  - `auto`: auto margin(align center)

---

## Border

| Class                          | Description                |
| ------------------------------ | -------------------------- |
| `border`                       | all side border            |
| `border-{side}`                | side border                |
| `border border-0`              | all side **no** border     |
| `border border-{width}`        | all side border with width |
| `border border-{side}-{width}` | side border with width     |
| `border border-{color}`        | side border with color     |

- side: `top`, `bottom`, `start`, and `end`
- width: `0`~`5`
- color:
  - `primary`, `secondary`,`success`,`danger`,`warning`,`info`,`light`, `dark`, `white`

---

## Border Radius

| Class                                      | Description                     |
| ------------------------------------------ | ------------------------------- |
| `rounded`                                  | all side rounded border         |
| `rounded-{side}`                           | side rounded border             |
| `rounded-circle`                           | a circle                        |
| `class="rounded-pill" style="width:130px"` | a hemi-circle border with width |
| `rounded-{size}`                           | rounded border with size        |

- side: `top`, `bottom`, `start`, and `end`
- width: `0`~`5`

---

## Shadow

| Class         | Description           |
| ------------- | --------------------- |
| `shadow-none` | No shadow(default)    |
| `shadow`      | Show shadow           |
| `shadow-sm`   | Show shadow with size |
| `shadow-lg`   | Show shadow with size |

---

[TOP](#bootstrap---box-model)
