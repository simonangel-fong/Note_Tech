"use strict";

// #region global variable
/**
 * Whether the current piece is black.
 * black=true, white=false
 */
var blackPiece = true; // black=true, white=false

// nodes
const btn_restart = document.querySelector("button");
const td_list = document.querySelectorAll("td");
// #endregion

// #region Supporting function
/**
 *  The value of current chess
 * @param {*} isBlack, whether the current piece is black
 * @returns Returns string X when it is black; Otherwise, returns O
 */
const chess = (isBlack) => {
  if (isBlack) {
    return "X";
  } else {
    return "O";
  }
};

// #endregion

// #region td nodes function and event

/**
 * Preview piece
 * @param {*} node, current td node
 * @param {*} isBlack, whether current piece is black
 */
const preview = (node, isBlack) => {
  node.style.backgroundColor = "#b4b4b4";
  node.textContent = chess(isBlack);
};

/**
 * Ends preview
 * @param {*} node, current td node.
 */
const endPreview = (node) => {
  node.textContent = "";
  node.removeAttribute("style");
};

/**
 * Pieces a chess on the table
 * @param {*} node, current td node.
 * @param {*} isBlack, whether current piece is black.
 */
const piece = (node, isBlack) => {
  endPreview(node);
  node.textContent = chess(isBlack);
  node.dataset.piece = true;
};

/**
 * Adds event listener to each td tag
 */
td_list.forEach((element) => {
  // Mouse over event: if current td is not pieced, call preview().
  element.addEventListener("mouseover", function () {
    // check the current td is pieced already
    if (this.dataset.piece == undefined) {
      preview(this, blackPiece);
    }
  });

  // Mouse out event: if current td is not pieced, call endPreview().
  element.addEventListener("mouseout", function () {
    if (this.dataset.piece == undefined) {
      endPreview(this);
    }
  });

  // Double click event: if current td is not pieced, call piece()
  element.addEventListener("dblclick", function () {
    if (this.dataset.piece == undefined) {
      piece(this, blackPiece);
      blackPiece = !blackPiece; // opposite the current piece
    }
  });
});

// #endregion

// #region #restart button function and events

/**
 * Resets the game.
 */
const restart = () => {
  // reset all td
  for (let ele of td_list) {
    ele.textContent = "";
    ele.removeAttribute("data-piece");
  }
  // reset global variable
  blackPiece = true;
};

/**
 * Adds event listener to restart button
 */
btn_restart.addEventListener("click", restart);
// #endregion
