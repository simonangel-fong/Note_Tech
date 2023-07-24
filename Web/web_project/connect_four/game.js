"use strict";

// #region Global Variable
var currentPiece = "blue"; //"blue": current piece is blue; Otherwise, it is red. "": End game.
var chessRec = []; //Chess record for computing whether either side wins the game.
var userBlue = ""; //user name for blue.
var userRed = ""; //user name for red.
const chessBoard = $("table div"); // div node list

// #endregion

// #region Render Function: using glabal var

/**
 * Input and bind user names.
 */
const inputUserName = () => {
  userBlue = prompt("Input your Name(Blue). \nPress ENTER to ignore.");
  $("#userBlue").text(userBlue);
  userRed = prompt("Input your Name(Blue). \nPress ENTER to ignore.");
  $("#userRed").text(userRed);
};

/**
 * Initialize chess record array, which is a two dimension array.
 */
const initRec = () => {
  for (let i = 0; i < 6; i++) {
    chessRec[i] = [];
    for (let j = 0; j < 7; j++) {
      chessRec[i][j] = null;
    }
  }
};

/**
 * Finds the last available chip with the current node.
 * @param {*} node, the node where cursor is placed.
 * @returns Each column's available chip node to be chessed.
 */
const getLast = (node) => {
  let col = chessBoard.index(node) % 7;
  let last = 5;
  while (-1 < last && chessRec[last][col] !== null) {
    last--;
  }
  // when current collumn is full.
  if (last === -1) {
    return { row: last, col: col, node: null };
  }
  return { row: last, col: col, node: $("tr").eq(last).find("div").eq(col) };
};

/**
 *  Previews the available chip.
 * @param {*} node, the available chip
 */
const preview = (node) => {
  if (currentPiece == "blue") {
    node.addClass("bg-info bg-opacity-50");
  } else {
    node.addClass("bg-danger bg-opacity-50");
  }
};

/**
 * Reset the available chip.
 * @param {*} node, the available chip
 */
const resetPrview = (node) => {
  node.removeClass("bg-opacity-50 bg-info bg-danger");
};

/**
 * Chess a chip and update record.
 * @param {*} node, the available chip
 * @param {*} row, the row # of the the available chip
 * @param {*} col, the col # of the the available chip
 */
const chess = (node, row, col) => {
  if (node.hasClass("bg-opacity-50")) {
    node.removeClass("bg-opacity-50");
  }
  if (currentPiece === "blue") {
    node.addClass("bg-info");
  } else {
    node.addClass("bg-danger");
  }
  chessRec[row][col] = currentPiece; // update chess record
};
// #endregion

// #region Event binding

/**
 * When document is ready: Initialize gloabl variables and page elements.
 */
$(document).ready(function () {
  inputUserName();
  initRec();
});

/**
 * When restart button is clicked: reset the game.
 */
$("#restart").on("click", function () {
  // reset all chips' color.
  $("table div").removeClass("bg-danger");
  $("table div").removeClass("bg-info");
  // reset chess record
  initRec();
  currentPiece = "blue";
});

/**
 *  Bind event to each chess.
 */
$("table div.chess").on({
  /**
   * When mouser over chess, find the last available node of each column and preview chess.
   */
  mouseover: function () {
    //if the game is not ended(currentPiece=="").
    if (currentPiece) {
      let lastNode = getLast(this);
      // if last node is available.
      if (lastNode["node"] !== null) {
        preview(lastNode["node"]);
      }
    }
  },
  /**
   * When mouser out chess, find the last available node of each column and reset chess.
   */
  mouseout: function () {
    //if the game is not ended(currentPiece=="").
    if (currentPiece) {
      let lastNode = getLast(this);
      // if last node is available.
      if (lastNode["node"] !== null) {
        resetPrview(lastNode["node"]);
      }
    }
  },
  /**
   * When double click a chess, find the last available node of each column, chess a piece, and check whether either side wins.
   * When the game is won, set currentPiece = "" to stop the game. Otherwise, switch the color of current piece.
   */
  dblclick: function () {
    //if the game is not ended(currentPiece=="").
    if (currentPiece) {
      let lastNode = getLast(this);

      // if last node is available.
      if (lastNode["node"] !== null) {
        chess(lastNode["node"], lastNode["row"], lastNode["col"]);
        // check if win
        if (isFour(lastNode["row"], lastNode["col"], chessRec)) {
          alert(
            `${
              currentPiece === "blue" ? userBlue : userRed
            } won! \nPress [Resart] button for a new game.`
          ); //show winner
          currentPiece = "";
          // check if tie game
        } else if (isDraw(chessRec)) {
          alert("Tie game! \nPress [Resart] button for a new game.");
          currentPiece = "";
        } else {
          currentPiece = currentPiece === "blue" ? "red" : "blue";
        }
      }
    }
  },
});

// #endregion

// #region Supportive Function
/**
 * Check whether the latest chess connects four chips.
 * @param {*} row,  the row # of the latest chess.
 * @param {*} col,  the column # of the latest chess.
 * @param {*} arr,  the chess record
 * @returns True, if a continued four chips is made. Otherwise, False.
 */
const isFour = (row, col, arr) => {
  // check a horizontal-4 is available
  const isHor = (col) => {
    let len = 1;
    let down = col;
    let up = col;
    while (0 < down && arr[row][down] == arr[row][down - 1]) {
      len++;
      down--;
    }
    while (up < arr.length - 1 && arr[row][up] == arr[row][up + 1]) {
      len++;
      up++;
    }
    return len >= 4;
  };

  // check a vertical-4 is available
  const isVer = (row) => {
    let len = 1;
    let down = row;
    let up = row;
    while (0 < down && arr[down][col] == arr[down - 1][col]) {
      len++;
      down--;
    }
    while (up < arr.length - 1 && arr[up][col] == arr[up + 1][col]) {
      len++;
      up++;
    }
    return len >= 4;
  };

  // check a back-diagonal-4 is available:\
  const isDiaBack = (row, col) => {
    let len = 1;
    let down_row = row;
    let down_col = col;
    let up_row = row;
    let up_col = col;
    while (
      0 < down_row &&
      0 < down_col &&
      arr[down_row][down_col] == arr[down_row - 1][down_col - 1]
    ) {
      len++;
      down_row--;
      down_col--;
    }
    while (
      up_row < arr.length - 1 &&
      up_col < arr[up_row].length - 1 &&
      arr[up_row][up_col] == arr[up_row + 1][up_col + 1]
    ) {
      len++;
      up_row++;
      up_col++;
    }
    return len >= 4;
  };

  // check a forward-diagonal-4 is available:/
  const isDiaForward = (row, col) => {
    let len = 1;
    let down_row = row;
    let down_col = col;
    let up_row = row;
    let up_col = col;
    while (
      down_row < arr.length - 1 &&
      0 < down_col &&
      arr[down_row][down_col] == arr[down_row + 1][down_col - 1]
    ) {
      len++;
      down_row++;
      down_col--;
    }
    while (
      0 < up_row &&
      up_col < arr[up_row].length - 1 &&
      arr[up_row][up_col] == arr[up_row - 1][up_col + 1]
    ) {
      len++;
      up_row--;
      up_col++;
    }
    return len >= 4;
  };
  // True, if either one available. Otherwise, False.
  return (
    isHor(col) || isVer(row) || isDiaBack(row, col) || isDiaForward(row, col)
  );
};

/**
 *  Check whether the lastest chess cause a tie game.
 * @param {*} arr,  the chess record
 * @returns True, if it is a tie game; Otherwise, False.
 */
const isDraw = (arr) => !arr.flat().includes(null);

// #endregion
