import { Previewer, Handler } from './paged.esm.js'


function handlersFunction(previewer){

  previewer.registerHandlers(
    class CustomHandlers extends Handler {

      /* your custom javascript here ----------------------------------------------------- */


      beforeParsed(content){
        console.log("beforeParsed -------------------------- ");
        console.log(content);
      }

      afterParsed(parsed){
        console.log("afterParsed ------------------------ ");
        console.log(parsed);
      }

      beforePageLayout(page){
        console.log("beforePageLayout ------------------------ ");
        console.log(page);
      }

      afterPageLayout(pageElement, page, breakToken){
        console.log(pageElement);
      }


      /* --------------------------------------------------------------------------------- */


    },
  );

}


export { handlersFunction };
