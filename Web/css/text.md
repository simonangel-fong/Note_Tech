# CSS - Text

[Back](./index.md)

- [CSS - Text](#css---text)
  - [Attributes](#attributes)

---

## Attributes

| Attribute                   | Description                           |
| --------------------------- | ------------------------------------- |
| `text-align`                | the horizontal alignment              |
| `text-align-last`           | how to align the last line            |
| `vertical-align`            | the vertical alignment                |
| `direction`                 | the text direction                    |
| `text-decoration`           | the decoration line to text           |
| `text-decoration-line`      | position of a decoration line to text |
| `text-decoration-color`     | the color of the decoration line      |
| `text-decoration-style`     | the style of the decoration line      |
| `text-decoration-thickness` | the thickness of the decoration line  |
| `text-transform`            | transform letters in a text           |
| `line-height`               | the space between lines               |
| `text-indent`               | the indentation of the first line     |
| `letter-spacing`            | the space between the characters      |
| `word-spacing`              | the space between the words           |
| `white-space`               | how to handle white-space             |
| `text-shadow`               | shadow of text                        |

- `text-align`:

  - `left`(default), `center`, `right`
  - `justify`: each line is stretched so that every line has equal width, and the left and right margins are straight. 两边靠边对齐, 每行文字平均分布.

- `vertical-align`:

  - `baseline`(default)
  - `text-top`
  - `text-bottom`
  - `sub`
  - `super`

- `text-decoration`:

  - 1 value: line
  - 2 value: line color
  - 3 value: line color style
  - 4 value: line color style thickness
  - `none`: remove the underline

- `text-decoration-line`:

  - `overline`
  - `line-through`
  - `underline`
  - 可以是以上多个

- `text-transform`:

  - `uppercase`, `lowercase`, `capitalize`

- `text-shadow`:

  - 2 values: horizontal vertical
  - 3 values: horizontal vertical color
  - 3 values: horizontal vertical blur color
  - 可以有多个 example:

  ```html
  <style>
    h1 {
      color: white;
      text-shadow: 1px 1px 2px black, 0 0 25px blue, 0 0 5px darkblue;
    }
  </style>

  <h1>Text-shadow effect!</h1>
  ```

---

[TOP](#css---text)
