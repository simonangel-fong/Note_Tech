# CSS - Box Model

[Back](./index.md)

- [CSS - Box Model](#css---box-model)
  - [Box Model](#box-model)
  - [Content](#content)
  - [Padding](#padding)
  - [Border](#border)
  - [Margin](#margin)
  - [Outline](#outline)

---

## Box Model

- The CSS box model is essentially **a box that wraps around every HTML element**.

![box model](./pic/box-model.gif)

- `Content`: The content of the box, where text and images appear
- `Padding`: Clears an area around the content. The padding is transparent
- `Border`: A border that goes around the padding and content
- `Margin`: Clears an area outside the border. The margin is transparent

---

## Content

- When you set the width and height properties of an element with CSS, you just set the width and height of the content area.
- To calculate the full size of an element, you must also add padding, borders and margins.

- **Common Attributes**

| Attribute    | Description                      |
| ------------ | -------------------------------- |
| `width`      | the width of element             |
| `min-width`  | the minimum width of an element  |
| `max-width`  | the maximum width of an element  |
| `height`     | the height of element            |
| `min-height` | the minimum height of an element |
| `max-height` | the maximum height of an element |

---

## Padding

- `Padding`
  - the space around an element's content, inside of any defined borders.

| Attribute         | Description                                |
| ----------------- | ------------------------------------------ |
| `padding`         | generate space around an element's content |
| `padding-top`     | the top space                              |
| `ppadding-right`  | the right space                            |
| `ppadding-bottom` | the bottom space                           |
| `ppadding-left`   | the left space                             |

- `padding`:

  - 1 values: top=bottom=right=left
  - 2 values: top and bottom, right and left
  - 3 values: top, right and left, bottom
  - 4 values: top, right, bottom, left

- values:
  - length - specifies a padding in px, pt, cm, etc.
  - % - specifies a padding in % of the width of the containing element
  - inherit - specifies that the padding should be inherited from the parent element

---

## Border

- `Border`
  - specify the style, width, and color of an element's border.

| Attribute                    | Description                           |
| ---------------------------- | ------------------------------------- |
| `border`                     | **border**                            |
| `border-top`                 | top border                            |
| `border-right`               | right border                          |
| `border-bottom`              | bottom border                         |
| `border-left`                | left border                           |
| `border-style`               | **the style of border**               |
| `border-top-style`           | the style of top border               |
| `border-right-style`         | the style of right border             |
| `border-bottom-style`        | the style of bottom border            |
| `border-left-style`          | the style of left border              |
| `border-width`               | **the width of borders**              |
| `border-top-width`           | the width of top border               |
| `border-right-width`         | the width of right border             |
| `border-bottom-width`        | the width of bottom border            |
| `border-left-width`          | the width of left border              |
| `border-color`               | **the color of borders**              |
| `border-top-color`           | the color of top border               |
| `border-right-color`         | the color of right border             |
| `border-bottom-color`        | the color of bottom border            |
| `border-left-color`          | the color of left border              |
| `border-radius`              | **add rounded borders to an element** |
| `border-top-left-radius`     | rounded top left borders              |
| `border-top-right-radius`    | rounded top right borders             |
| `border-bottom-left-radius`  | rounded bottom left borders           |
| `border-bottom-right-radius` | rounded bottom right borders          |

- `border`

  - values: border-width, border-style, border-color

- `border-style`

  - 1 values: top=bottom=right=left
  - 4 values: top, right, bottom, left
  - values

    - `dotted`: a dotted border
    - `dashed`: a dashed border
    - `solid`: a solid border
    - `double`: a double border
    - `groove`: a 3D grooved border. The effect depends on the border-color value
    - `ridge`: a 3D ridged border. The effect depends on the border-color value
    - `inset`: a 3D inset border. The effect depends on the border-color value
    - `outset`: a 3D outset border. The effect depends on the border-color value
    - `none`: no border
    - `hidden`: a hidden border

- `border-width`

  - 1 values: top=bottom=right=left
  - 2 values: top and bottom, side
  - 4 values: top, right, bottom, left

- `border-color`
  - 1 values: top=bottom=right=left
  - 4 values: top, right, bottom, left

---

## Margin

- space around elements, **outside of any defined borders**.

| Attribute       | Description                     |
| --------------- | ------------------------------- |
| `margin`        | the margin of an element        |
| `margin-top`    | the top margin of an element    |
| `margin-right`  | the right margin of an element  |
| `margin-bottom` | the bottom margin of an element |
| `margin-left`   | the left margin of an element   |

- `margin`

  - 1 values: top=bottom=right=left
  - 2 values: top and bottom, right and left
  - 3 values: top, right and left, bottom
  - 4 values: top, right, bottom, left

  - value:
    - `auto`: split equally between the left and right margins

- Margin Collapse
  - Top and bottom margins of elements are sometimes collapsed into a single margin that is equal to **the largest of the two margins**.
  - Only happens on top and bottom margins. This does not happen on left and right margins!

---

## Outline

- An outline is a **line** that is drawn around elements, **OUTSIDE the borders**, to make the element "stand out".
  - 注意: margin 和 outling 都是在 border 外, 但是 margin 是透明的, outline 则是可以设置的.
  - 单纯设置 outline, 其效果与 border 相似.

| Attribute        | Description                                  |
| ---------------- | -------------------------------------------- |
| `outline`        | the margin of an element                     |
| `outline-style`  | the style of the outline                     |
| `outline-width`  | the width of the outline                     |
| `outline-color`  | the color of the outline                     |
| `outline-offset` | space between an outline and the edge/border |

- `outline`:

  - values: outline-width, outline-style, outline-color

- `outline-style`

  - style:
    - `dotted`:Defines a dotted outline
    - `dashed`:Defines a dashed outline
    - `solid`:Defines a solid outline
    - `double`:Defines a double outline
    - `groove`:Defines a 3D grooved outline
    - `ridge`:Defines a 3D ridged outline
    - `inset`:Defines a 3D inset outline
    - `outset`:Defines a 3D outset outline
    - `none`:Defines no outline
    - `hidden`:Defines a hidden outline

- `outline-width`:
  - thin (typically 1px)
  - medium (typically 3px)
  - thick (typically 5px)
  - A specific size (in px, pt, cm, em, etc)

---

[TOP](#css---box-model)
