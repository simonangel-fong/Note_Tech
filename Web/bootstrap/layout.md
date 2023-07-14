# Bootstrap - Layout

[back](./index.md)

- [Bootstrap - Layout](#bootstrap---layout)
  - [Position](#position)
  - [Float](#float)
  - [Horizontal \& Vertical Layout](#horizontal--vertical-layout)
  - [Flexbox](#flexbox)

---

## Position

| Class           | Description                                                                          |
| --------------- | ------------------------------------------------------------------------------------ |
| `fixed-top`     | at the top of the viewport, from edge to edge.                                       |
| `fixed-bottom`  | at the bottom of the viewport, from edge to edge.                                    |
| `sticky-top`    | at the top of the viewport, from edge to edge, but only after you scroll past it.    |
| `sticky-bottom` | at the bottom of the viewport, from edge to edge, but only after you scroll past it. |

---

## Float

| Class         | Description                                       |
| ------------- | ------------------------------------------------- |
| `float-none`  | disable floating                                  |
| `float-start` | float an element to the left                      |
| `float-end`   | float an element to the right                     |
| `clearfix `   | clear floated content within the parent container |

---

## Horizontal & Vertical Layout

| Class    | Description              |
| -------- | ------------------------ |
| `hstack` | horizontal layouts       |
| `vstack` | create vertical layouts. |

- `hstack`:

  - Stacked items are vertically **centered** by default and only take up their **necessary width**.

- `vstack`
  - Stacked items are **full-width** by default.
  - Use `gap-*` utilities to add space between items.

---

## Flexbox

- Apply `display` utilities to create a flexbox container and transform direct children elements into flex items.

| Class                    | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| `d-flex`                 | create a flexbox container, 100% width               |
| `d-inline-flex`          | create an inline flexbox container, neccessary width |
| `flex-row`               | set a horizontal direction                           |
| `flex-row-reverse`       | set a horizontal direction from the opposite side    |
| `flex-column`            | set a vertical direction                             |
| `flex-column-reverse`    | set a vertical direction from the opposite side      |
| `ms-auto`                | push items to the right                              |
| `me-auto`                | push items to the left                               |
| `mb-auto`                | push items to the top                                |
| `mt-auto`                | push items to the bottom                             |
| `justify-content-{side}` | change the alignment of flex items                   |
| `align-content-{side}`   | Align **gathered items**                             |
| `align-items-{side}`     | Align **single rows of items**                       |
| `align-self-{side}`      | Align **a flex item**                                |
| `flex-fill`              | force items into equal width                         |
| `flex-grow-0`            | item does not grow on different screens              |
| `flex-grow-1`            | take up the rest of the space                        |
| `flex-nowrap`            | default,text should not wrap until the end           |
| `flex-wrap`              | text wrap                                            |
| `flex-wrap-reverse`      | reverse text wrap                                    |

- `justify-content-{side}`:

  - `start` (default), `end`, `center`, `between` or `around`

- `align-content-{side}`

  - `start` (default), `end`, `center`, `between`, `around` and `stretch`.

- `align-items-{side}`

  - `start`, `end`, `center`, `baseline`, and `stretch`(default).

- `align-self-{side}`
  - `start`, `end`, `center`, `baseline`, and `stretch`(default).

---

[TOP](#bootstrap---layout)
