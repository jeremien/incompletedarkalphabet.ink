import { Previewer, Handler } from '../js/paged.esm.js';
import { handlersFunction } from '../js/handlers.js';

window.addEventListener('load', () => {
    console.log("script.js loaded");
    printPreview();
});


function printPreview(){
  let bookcontent = document.querySelector("#content");
    let content = bookcontent.innerHTML;
    bookcontent.innerHTML = "";

    let previewer = new Previewer();

    handlersFunction(previewer);

    previewer.preview(
      content,
      ["css/book/style.css"],
      document.querySelector("#renderbook")
    );

}
