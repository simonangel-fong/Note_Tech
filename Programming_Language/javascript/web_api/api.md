# Javascript - Web APIs

[Back](../index.md)

- [Javascript - Web APIs](#javascript---web-apis)
  - [Web API](#web-api)
  - [Fetch API](#fetch-api)
    - [HTTP Structure](#http-structure)
    - [XMLHTTPRequest](#xmlhttprequest)
    - [`fetch()`](#fetch)
    - [Example](#example)

---

## Web API

- `API`

  - stands for `Application Programming Interface`.

- `Web API`

  - an application programming interface for the Web.

- A `Browser API` can extend the functionality of a web browser.

- A `Server API` can extend the functionality of a web server.

---

## Fetch API

- The **Fetch API** interface allows web browser to make HTTP requests to web servers.

---

### HTTP Structure

- `Hypertext Transfer Protocol (HTTP)`: an application-level protocol.

  - It provides a standardized way for computers to communicate with each other.
  - `HTTP` specification specifies how clients' request data will be **constructed** and sent to the **server**, and how the servers **respond** to these requests.

- The `HTTP protocol`: a request/response protocol based on the `client/server-based architecture` where web browsers, robots and search engines, etc. act like **HTTP clients**, and the Web server acts as a **server**.

- `HTTP client` sends a request to the server in the form of a request method, URI, and protocol version, followed by a MIME-like message containing request modifiers, client information, and possible body content over a TCP/IP connection.

- `HTTP server` responds with a status line, including the message's protocol version and a success or error code, followed by a MIME-like message containing server information, entity meta information, and possible entity-body content.

- **HTTP Request types** – GET, POST, PUT, DELETE
  - `GET`: **retrieving, or getting, information** from some source (usually a website).
  - `POST`: **sending, or posting, information** to a source that will process
    the information and send it back.
  - `PUT`: **updating** already existing data
  - `DELETE`: **deleting data**

---

### XMLHTTPRequest

- `XMLHttpRequest(XHR)` objects are used to interact with servers. You can retrieve data from a URL without having to do a full-page refresh.

  - This enables a Web page to update just part of a page without disrupting what the user is doing.

- Promise

---

### `fetch()`

- `Fetch API` is an interface for fetching resources. It is built-in browser JS function
- The `fetch()` function:

  - Creates a request object that contains relevant information that an API needs.
  - Sends that request object to the API endpoint provided.
  - **Returns a promise** that ultimately resolves to a response object, which contains the status of the promise with information the API sent back.

- **Syntax**:

```js
// syntax
fetch(resource).then();
fetch(resource, options).then();

// common use
// define an async function
async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

// call the async function
postData("https://example.com/answer", { answer: 42 }).then((data) => {
  console.log(data); // JSON data parsed by `data.json()` call
});
```

- **Parameters**:

  - `resource`:the resource to fetch
    - `string`: URL string
    - `Request` object.
  - `options`: Optional
    - any custom settings to apply to the request.

- **Return**:

  - A **Promise** that resolves to a **Response object**.

- **Example: Get Json file**

```html
<script>
  // promise
  const JSON_URL = "books.json";

  console.log("Json:Fecth promise");

  fetch(JSON_URL)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw Error(response.statusText);
      }
    })
    .then((json_data) => console.log("Json promise:", json_data))
    .catch((err) => console.log("Error", err));

  // async
  console.log("Json:Fecth async");

  const main_fetch_async = async (url) => {
    const json_data = await fetch(url).then((response) => response.json());
    console.log("Json Async:", json_data);
  };
  main_fetch_async(JSON_URL);
</script>
```

### Example

```js
console.log("\n-------- fetch(): Example --------\n");

const CLIENT_ID = "910e59ec1184482d8932ab9e1bc3ff8d";
const CLIENT_SECRET = "02f3d3633013444f86f33305092dcfb5";

const URL_TOKEN = "https://accounts.spotify.com/api/token";
const URL_GENREUS = "https://api.spotify.com/v1/browse/categories?locale=sv_US";
("https://api.spotify.com/v1/browse/categories/{category_ID}/playlists");

// define an async function to get token.
const getToken = async (urlToken, clientID, clientSecret) => {
  const response = await fetch(urlToken, {
    method: "POST",
    headers: {
      Authorization: `Basic ${btoa(clientID + ":" + clientSecret)}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
  });

  const data = await response.json();
  return data.access_token;
};

// define an async function to get genre list.
const getGenreList = async (urlGenre, token, genreLimit = 10) => {
  const reponse = await fetch(urlGenre + "&limit=" + genreLimit, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  const data = await reponse.json();
  return data.categories.items;
};

// define a main funciont to display genre names.
const main = async () => {
  let token = await getToken(URL_TOKEN, CLIENT_ID, CLIENT_SECRET);
  let genreList = await getGenreList(URL_GENREUS, token);

  for (let obj of genreList) {
    console.log(obj["name"]);
  }
};

// call main function
main();
// Topplistor
// Hiphop
// Pop
// Sommar
// Country
// Rock
// Humör
// Träning
// Chill
// R&B
```

---

[TOP](#javascript---web-apis)
