const header = document.querySelector("h1");

const randomColorCode = () => {
  let hexaChar = "0123456789ABCDEF";
  let colorCode = "#";
  for (let i = 0; i < 6; i++) {
    colorCode += hexaChar[Math.floor(Math.random() * 16)];
  }
  return colorCode;
};

setInterval(() => {
  header.style.color = randomColorCode();
}, 500);
