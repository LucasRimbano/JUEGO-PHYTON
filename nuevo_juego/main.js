const playButton = document.getElementById("play-button");

playButton.addEventListener("click", function () {
  document.body.classList.add("is-loading");
  window.location.href = "game.html";
});
