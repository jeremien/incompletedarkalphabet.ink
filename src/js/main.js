window.addEventListener("load", (event) => {

  const chapitreTitles = document.querySelectorAll('.chapitre-title');

  const rightTitle = document.querySelector('.right');

  chapitreTitles.forEach((item, i) => {
      rightTitle.innerHTML += `<li><a href="#${item.innerText}">${item.innerText}</a></li>`
  });


});
