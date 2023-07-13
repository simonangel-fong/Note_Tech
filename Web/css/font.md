# CSS - Font

[Back](./index.md)

- [CSS - Font](#css---font)
  - [Resource](#resource)
  - [Font Family](#font-family)
  - [Attribute](#attribute)

---

## Resource

- CSS Fonts(check supported OS):

  - https://www.cssfontstack.com/

- Google Fonts(download or embed):
  - https://fonts.google.com/noto/specimen/Noto+Sans+TC?preview.size=28

---

## Font Family

- In CSS there are five generic font families:

  - `Serif` fonts have a small stroke at the edges of each letter. They create a sense of **formality and elegance**.

  - `Sans-serif` fonts have clean lines (no small strokes attached). They create a **modern and minimalistic** look.

  - `Monospace` fonts - here all the letters have the same fixed width. They create a **mechanical look**.

  - `Cursive` fonts imitate **human handwriting**.

  - `Fantasy` fonts are **decorative/playful** fonts.

- All the different font names belong to one of the generic font families.

---

## Attribute

| Attribute      | Common Values               | Description                            |
| -------------- | --------------------------- | -------------------------------------- |
| `font`         |                             | set several font properties            |
| `font-family`  |                             | the font family of a text              |
| `font-style`   | `normal`,`italic`,`oblique` | mostly used to specify italic text     |
| `font-weight`  | `normal`,`bold`             | the weight of a font                   |
| `font-variant` | `normal`,`small-caps`       | whether displayed in a small-caps font |
| `font-size`    | `px`,`em`,`%`               | the size of the text                   |

- `font-size`:
  - Absolute size
  - Relative size
    - An `em` is a unit of measurement, relative to the size of the font;
    - If you do not specify a font size, the default size for normal text, like paragraphs, is 16px (16px=1`em`).
    - fomula: `pixels/16=em`
  - Responsive Font Size
    - `vw`: viewport width
    - Viewport is the browser window size. 1vw = 1% of viewport width. If the viewport is 50cm wide, 1vw is 0.5cm.

---

[TOP](#css---font)
