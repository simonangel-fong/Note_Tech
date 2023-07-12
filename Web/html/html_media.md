# HTML - Meida

[Back](./index.md)

- [HTML - Meida](#html---meida)
  - [`<img>` element](#img-element)
  - [`<video>` element](#video-element)
  - [`<audio>` Element](#audio-element)
  - [Playing a YouTube Video in HTM](#playing-a-youtube-video-in-htm)

---

## `<img>` element

The HTML `<img>` tag is used to embed an **image** in a web page.

Images are not technically <u>inserted</u> into a web page; images are **linked** to web pages. The `<img>` tag creates a **holding space** for the referenced image.

The `<img> `tag is empty, it contains attributes only, and does **not have a closing tag**.

The `<img>` tag has two required attributes:

- `src` - Specifies the **path(URL)** to the image
- `alt` - Specifies an **alternate text** for the image

Other attributes:

- `width` and `height`: size

---

## `<video>` element

- show a video on a web page.

- Syntax:

```html
<video width="320" height="240" controls>
  <source src="movie.mp4" type="video/mp4" />
  <source src="movie.ogg" type="video/ogg" />
  Your browser does not support the video tag.
</video>
```

- Attribute

| Attribute  | Description                  |
| ---------- | ---------------------------- |
| `controls` | adds video controls          |
| `width`    | the width of video controls  |
| `height`   | the height of video controls |
| `autoplay` | start a video automatically  |
| `muted`    | mute the video               |

- `<source>` element:

  - allows to specify alternative video files which the browser may choose from.
  - The browser will use the first recognized format.

- The text between the `<video>` and `</video>` tags will only be displayed in browsers that do not support the `<video>` element.

---

## `<audio>` Element

- play an audio file in HTML

- Syntax:

```html
<audio controls autoplay>
  <source src="horse.ogg" type="audio/ogg" />
  <source src="horse.mp3" type="audio/mpeg" />
  Your browser does not support the audio element.
</audio>
```

- Attribute

| Attribute  | Description                 |
| ---------- | --------------------------- |
| `controls` | adds audio controls         |
| `autoplay` | start a audio automatically |
| `muted`    | mute the audio              |

- `<source>` element:

  - allows to specify alternative audio files which the browser may choose from.
  - The browser will use the first recognized format.

- The text between the `<audio>` and `</audio>` tags will only be displayed in browsers that do not support the `<audio>` element.

---

## Playing a YouTube Video in HTM

- To play your video on a web page, do the following:

  - Upload the video to YouTube
  - Take a note of the video id
  - Define an `<iframe>` element in your web page
  - Let the src attribute point to the video URL
  - Use the width and height attributes to specify the dimension of the player
  - Add any other parameters to the URL (see below)

- Example:

```html
<iframe
  width="420"
  height="315"
  src="https://www.youtube.com/embed/tgbNymZ7vqY"
>
</iframe>

<!-- YouTube Autoplay + Mute -->
<iframe
  width="420"
  height="315"
  src="https://www.youtube.com/embed/tgbNymZ7vqY?autoplay=1&mute=1"
>
</iframe>

<!-- YouTube Playlist + Loop -->
<iframe
  width="420"
  height="315"
  src="https://www.youtube.com/embed/tgbNymZ7vqY?playlist=tgbNymZ7vqY&loop=1"
>
</iframe>

<!-- YouTube not display controls -->
<iframe
  width="420"
  height="315"
  src="https://www.youtube.com/embed/tgbNymZ7vqY?controls=0"
>
</iframe>
```

---

[TOP](#html---meida)
